
def CreateContext():
    return Context()


def CreateImage(context, width, height, color):
    return Image(context, width, height, color, False)


def CreateGraph(context):
    return Graph(context)


def CreateVirtualImage(graph, width, height, color):
    return Image(graph.context, width, height, color, True, graph)


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


class FOURCC_UYVY:
    name = "ImageUYVY"
    base_type = "uint8_t"
    items = 2


class FOURCC_U8:
    name = "ImageU8"
    base_type = "uint8_t"
    items = 1


class CHANNEL_0:
    pass


class CHANNEL_1:
    pass


class CHANNEL_2:
    pass


class CHANNEL_3:
    pass


class CHANNEL_Y:
    pass


class Context(object):
    pass


from cffi import FFI
from weakref import WeakKeyDictionary
from collections import defaultdict

keepalive = WeakKeyDictionary()

base_ffi = FFI()
for t in [FOURCC_RGB, FOURCC_UYVY, FOURCC_U8]:
    base_ffi.cdef("""
                  typedef struct {
                    %s * data;
                    int dim_x, dim_y, stride_x, stride_y;
                  } %s;
                  """ % (t.base_type, t.name))


class Image(object):

    def __init__(self, context, width, height, color,
                 virtual=False, graph=None):
        self.context = context
        self.width = width
        self.height = height
        self.color = color
        self.virtual = virtual
        self.graph = graph
        self.producer = None
        self.cdata = None

    def force(self):
        self.virtual = False

    def ensure(self, width, height, color):
        if self.width == 0:
            self.width = width
        if self.height == 0:
            self.height = height
        if self.color == FOURCC_VIRT:
            self.color = color
        if self.width != width or self.height != height or self.color != color:
            raise InvalidFormatError

    def alloc(self):
        if self.cdata is not None:
            return
        cdata = self.cdata = base_ffi.new(self.color.name + '*')
        cdata.dim_x = self.width
        cdata.dim_y = self.height
        cdata.stride_x = self.color.items
        cdata.stride_y = self.width * self.color.items
        items = self.width * self.height * self.color.items
        buf = base_ffi.new(self.color.base_type + '[]', items)
        keepalive[cdata] = buf
        cdata.data = buf
        addr = base_ffi.cast('long', cdata)
        self.csym = "((%s *) 0x%x)" % (self.color.name, addr)
        self.ctype = self.color.name + " *"


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
        code = Code()
        for n in self.nodes:
            n.compile(code)
        print code

    def process(self):
        pass

class Code(object):
    var_count = defaultdict(int)
    
    def __init__(self):
        self.code = ''
        self.open_block = False


    def new_block(self, **kwargs):
        if self.open_block:
            self.code += '}\n'
        self.open_block = True
        self.code += '{\n'
        for var, val in kwargs.items():
            #self.var_count[var] += 1
            #var += str(self.var_count[var])
            if isinstance(val, int):
                self.code += '            long %s = %d;\n' % (var, val)
            else:
                self.code += '            %s %s = %s;\n' % (val.ctype, var, val.csym)

    #     
    #     self.name = name + str(self.count[name])
    def push_code(self, code):
        self.code += code+"\n";

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

    def setup(self):
        self.graph._add_node(self)
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


class ChannelExtractNode(Node):

    def __init__(self, graph, input, channel, output):
        self.graph = graph
        self.channel = channel
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        if i.color == FOURCC_UYVY and self.channel == CHANNEL_Y:
            pass
        else:
            raise InvalidFormatError(
                'Cant extract channel %s from %s image.' % (self.channel,
                                                            i.color))
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class Gaussian3x3Node(Node):

    def __init__(self, graph, input, output):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)

    def compile(self, code):
        code.new_block(img=self.inputs[0],
                       res=self.outputs[0],
                       x=0, y=0)
        code.push_code("""
            for (y = 1; y < img.dim_y-1; y++) {
                for (x = 1; x < img.dim_x-1; x++) {
                    res[x, y] = (1*img[x-1, y-1] + 2*img[x, y-1] + 1*img[x+1, y-1] +
                                 2*img[x-1, y]   + 4*img[x, y]   + 2*img[x+1, y]   +
                                 1*img[x-1, y+1] + 2*img[x, y+1] + 1*img[x+1, y+1]) / 16;
                }
            }
        """)


class Sobel3x3Node(Node):

    def __init__(self, graph, input, output_x, output_y):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output_x, output_y]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class MagnitudeNode(Node):

    def __init__(self, graph, grad_x, grad_y, mag):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [mag]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class PhaseNode(Node):

    def __init__(self, graph, grad_x, grad_y, orientation):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [orientation]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)
        self.outputs[1].ensure(i.width, i.height, FOURCC_U8)


class AccumulateImageNode(Node):

    def __init__(self, graph, input, accum):
        self.graph = graph
        self.inputs = [input]
        self.outputs = []
        self.inouts = [accum]
        self.setup()

    def verify(self):
        pass
