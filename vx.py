
def CreateContext():
    return Context()


def CreateImage(context, width, height, color):
    return Image(context, width, height, color, None, False)


def CreateGraph(context):
    return Graph(context)


def CreateVirtualImage(graph, width, height, color):
    return Image(graph.context, width, height, color, None, True, graph)


def VerifyGraph(graph):
    return graph.verify()


def ProcessGraph(graph):
    return graph.process()


class FOURCC_VIRT:
    pass


class FOURCC_RGB:
    name = "ImageRGB"
    base_type = "uint8_t"
    items = 3
    typecode = "B"


class FOURCC_UYVY:
    name = "ImageUYVY"
    base_type = "uint8_t"
    items = 2
    typecode = "B"


class FOURCC_U8:
    name = "ImageU8"
    base_type = "uint8_t"
    items = 1
    typecode = "B"


class CHANNEL_0: pass
class CHANNEL_1: pass
class CHANNEL_2: pass
class CHANNEL_3: pass
class CHANNEL_Y: pass


class BORDER_MODE_UNDEFINED: pass
class BORDER_MODE_CONSTANT: pass
class BORDER_MODE_REPLICATE: pass

class Context(object):
    pass


from cffi import FFI
from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator

base_ffi = FFI()

class Image(object):

    def __init__(self, context, width, height, color,
                 data=None, virtual=False, graph=None):
        self.context = context
        self.width = width
        self.height = height
        self.color = color
        self.virtual = virtual
        self.graph = graph
        self.producer = None
        if data is not None:
            self.set_data_pointer(data)
        else:
            self.data = None

    def set_data_pointer(self, data):
        if hasattr(data, 'typecode'):
            assert data.typecode == self.color.typecode
        if hasattr(data, 'to_cffi'):
            self.data = data.to_cffi(base_ffi)
        elif hasattr(data, 'buffer_info'):
            addr, l = data.buffer_info()
            assert l == self.width * self.height * self.color.items
            self.data = base_ffi.cast(self.color.base_type + ' *', addr)
        else:
            raise NotImplementedError("Dont know how to convert %r to a cffi buffer" % data)
        self._keep_alive_original_data = data

    def force(self, data=None):
        if data is not None:
            self.set_data_pointer(data)
        self.virtual = False

    def ensure_shape(self, width_or_image, height=None):
        if height is None:
            width, height = width_or_image.width, width_or_image.height
        else:
            width = width_or_image
        if self.width == 0:
            self.width = width
        if self.height == 0:
            self.height = height
        if self.width != width or self.height != height:
            raise InvalidFormatError

    def ensure_color(self, color):
        self.suggest_color(color)
        if  self.color != color:
            raise InvalidFormatError            

    def suggest_color(self, color):
        if self.color == FOURCC_VIRT:
            self.color = color

    def ensure_similar(self, image):
        self.ensure_shape(image)
        self.suggest_color(image.color)
        if self.color.items != image.color.items:
            raise InvalidFormatError

    def alloc(self):
        if self.data is None:
            items = self.width * self.height * self.color.items
            self.data = base_ffi.new(self.color.base_type + '[]', items)
        addr = base_ffi.cast('long', self.data)
        self.csym = "((%s *) 0x%x)" % (self.color.base_type, addr)
        self.ctype = self.color.base_type + " *"

    def getitem(self, node, name, x, y):
        if node.border_mode == BORDER_MODE_UNDEFINED:
            l = self.width * self.height - 1
            return "%s[clamp((%s) * %d + (%s), 0, %d)]" % (name, y, self.width, x, l)
        elif node.border_mode == BORDER_MODE_REPLICATE:
            return "%s[clamp(%s, 0, %d) * %d + clamp(%s, 0, %d)]" % (
                   name, y, self.height-1, self.width, x, self.width-1)
        else:
            raise NotImplementedError

    def getattr(self, node, name, attr):
        if attr == "width":
            return str(self.width)
        elif attr == "height":
            return str(self.height)
        elif attr == "data":
            return name
        else:
            raise AttributeError


class Graph(object):

    def __init__(self, context, early_verify=True):
        self.context = context
        self.nodes = []
        self.data_objects = set()
        self.early_verify = early_verify

    def _add_node(self, node):
        self.nodes.append(node)
        for d in node.inputs + node.outputs + node.inouts:
            self.data_objects.add(d)

    def verify(self):
        self.nodes = self.schedule()

        for node in self.nodes:
            node.do_verify()

        # Virtual data produced
        for d in self.data_objects:
            if d.virtual and d.producer is None:
                raise InvalidGraphError("Virtual data never produced.")
            if d.color == FOURCC_VIRT:
                raise InvalidFormatError("FOURCC_VIRT not resolved into specific type.")

        self.compile()

    def schedule(self):
        for d in self.data_objects:
            d.present = not d.virtual
        for n in self.nodes:
            for d in n.outputs + n.inouts:
                d.present = False
        worklist = self.nodes[:]
        inorder = []
        while worklist:
            remaining = []
            for n in worklist:
                if all(d.present for d in n.inputs):
                    inorder.append(n)
                    for d in n.outputs:
                        d.present = True
                else:
                    remaining.append(n)
            if len(worklist) == len(remaining):
                raise InvalidGraphError("Loops not allowed in the graph.")
            worklist = remaining
        return inorder

    def compile(self):
        for d in self.data_objects:
            d.alloc()
        code = Code('''
                    long clamp(long val, long min_val, long max_val) {
                        if (val < min_val) return min_val;
                        if (val > max_val) return max_val;
                        return val;
                    }
                    ''')
        for n in self.nodes:
            n.compile(code)
        ffi = FFI()
        ffi.cdef("void func(void);")
        #print str(code)
        lib = ffi.verify("void func(void) {" + str(code) + "}",
                         extra_compile_args=["-O3", "-march=native"])
        self.compiled_func = lib.func

    def process(self):
        self.compiled_func()

def cparse(code):
    parser = c_parser.CParser()
    ast = parser.parse("void f() {" + code + "}")
    func = ast.ext[0]
    assert func.decl.name == 'f'
    return func.body

class MagicCGenerator(CGenerator):
    def __init__(self, cxnode, magic_vars):
        CGenerator.__init__(self)
        self.cxnode = cxnode
        self.magic_vars = magic_vars

    def visit_StructRef(self, node):
        assert isinstance(node.name, c_ast.ID)
        assert isinstance(node.field, c_ast.ID)
        if node.name.name in self.magic_vars:
            var = self.magic_vars[node.name.name]
            return var.getattr(self.cxnode, node.name.name, node.field.name)
        return CGenerator.visit_StructRef(self, node)

    def visit_ArrayRef(self, node):
        if not isinstance(node.name, c_ast.ID):
            return CGenerator.visit_ArrayRef(self, node)
        assert isinstance(node.subscript, c_ast.ExprList)
        if node.name.name in self.magic_vars:
            x, y = node.subscript.exprs
            var = self.magic_vars[node.name.name]
            return var.getitem(self.cxnode, node.name.name, self.visit(x), self.visit(y))
        return CGenerator.visit_ArrayRef(self, node)

class Code(object):
    
    def __init__(self, code=''):
        self.code = code
        self.open_block = False


    def new_block(self, **kwargs):
        if self.open_block:
            self.code += '}\n'
        self.open_block = True
        self.magic_vars = {}
        self.code += '{\n'
        for var, val in kwargs.items():
            if isinstance(val, int):
                self.code += '  long %s = %d;\n' % (var, val)
            else:
                self.code += '  %s %s = %s;\n' % (val.ctype, var, val.csym)
            if isinstance(val, Image):
                self.magic_vars[var] = val

    def push_code(self, cxnode, code):
        ast = cparse(code)
        #ast.show()
        generator = MagicCGenerator(cxnode, self.magic_vars)
        generator.indent_level = 2
        self.code += ''.join(generator._generate_stmt(stmt) 
                             for stmt in ast.block_items)

    def __str__(self):
        if self.open_block:
            return self.code + '}'
        return self.code

class MultipleWritersError(Exception):
    pass


class InvalidGraphError(Exception):
    pass


class InvalidValueError(Exception):
    pass


class InvalidFormatError(Exception):
    pass


class Node(object):

    def __init__(self, graph, *args, **kwargs):
        self.graph = graph
        self.inputs, self.outputs, self.inouts = [], [], []
        for i, v in enumerate(self.signature.split(',')):
            v = v.strip().split(' ')
            direction, name = v[0], v[-1]
            if i < len(args):
                val = args[i]
                if name in kwargs:
                    raise TypeError("Got multiple values for keyword argument '%s'" % name)
            elif name in kwargs:
                val = kwargs[name]
            else:
                raise TypeError("Required argument missing")
            if direction == 'in':
                self.inputs.append(val)
            elif direction == 'out':
                self.outputs.append(val)
            elif direction == 'inout':
                self.inouts.append(val)
            else:
                raise TypeError("Bad direction '%s' of argument '%s'" % (direction, name))
            setattr(self, name, val)
        self.setup()

    def setup(self):
        self.graph._add_node(self)
        self.border_mode = BORDER_MODE_UNDEFINED
        self.border_mode_value = 0
        for d in self.outputs + self.inouts:
            if d.producer is None:
                d.producer = self
        if self.graph.early_verify:
            self.do_verify()

    def do_verify(self):
        # Signle writer
        for d in self.outputs + self.inouts:
            if d.producer is not self:
                raise MultipleWritersError

        # Bidirection data not virtual
        for d in self.inouts:
            if d.virtual:
                raise InvalidGraphError("Bidirection data cant be virtual.")

        for d in self.inputs:
            if not d.width or not d.height:
                raise InvalidFormatError
        self.verify()

    def ensure(self, condition):
        if not condition:
            raise InvalidFormatError


class ChannelExtractNode(Node):
    signature = "in input, in channel, out output"

    def verify(self):
        if self.input.color == FOURCC_UYVY and self.channel == CHANNEL_Y:
            pass
        else:
            raise InvalidFormatError(
                'Cant extract channel %s from %s image.' % (self.channel,
                                                            i.color))
        self.output.ensure_similar(self.input)


class Gaussian3x3Node(Node):
    signature = "in input, out output"

    def verify(self):
        self.ensure(self.input.color.items == 1)
        self.output.ensure_similar(self.input)

    def compile(self, code):
        code.new_block(img=self.input,
                       res=self.output,
                       x=0, y=0)
        code.push_code(self, """
            for (y = 0; y < img.height; y++) {
                for (x = 0; x < img.width; x++) {
                    res[x, y] = (1*img[x-1, y-1] + 2*img[x, y-1] + 1*img[x+1, y-1] +
                                 2*img[x-1, y]   + 4*img[x, y]   + 2*img[x+1, y]   +
                                 1*img[x-1, y+1] + 2*img[x, y+1] + 1*img[x+1, y+1]) / 16;
                }
            }
        """)


class Sobel3x3Node(Node):
    signature = 'in input, out output_x, out output_y'

    def verify(self):
        self.ensure(self.input.color.items == 1)
        self.output_x.ensure_similar(self.input)
        self.output_y.ensure_similar(self.input)

class MagnitudeNode(Node):
    signature = 'in grad_x, in grad_y, out mag'

    def verify(self):
        self.ensure(self.grad_x.color.items == 1)
        self.ensure(self.grad_y.color.items == 1)
        self.mag.ensure_similar(self.input)

class PhaseNode(Node):
    signature = 'in grad_x, in grad_y, out orientation'

    def verify(self):
        self.ensure(self.grad_x.color.items == 1)
        self.ensure(self.grad_y.color.items == 1)
        self.orientation.ensure_similar(self.input)

class AccumulateImageNode(Node):
    signature = 'in input, inout accum'

    def verify(self):
        pass
