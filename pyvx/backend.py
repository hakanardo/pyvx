from pyvx.types import *
from pyvx.codegen import Code, Enum
from cffi import FFI
from collections import defaultdict
from itertools import chain
import threading, os
from tempfile import mkdtemp
from shutil import rmtree

class Context(object):
    references = []

    def add_reference(self, ref):
        self.references.append(ref)

    def clear_references(self):
        self.references = []

class CoreImage(object):
    count = 0
    optimized_out = False

    def __init__(self, width=0, height=0, color=FOURCC_VIRT,
                 data=None, context=None, virtual=None, graph=None):
        if graph is None:
            graph = CoreGraph.get_current_graph(none_check=False)
        if context is None:
            context = graph.context
        if virtual is None:
            virtual = (color == FOURCC_VIRT)
        if virtual:
            assert graph is not None
        assert context is not None
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
        CoreImage.count += 1
        self.count = CoreImage.count

    def set_data_pointer(self, data):
        if hasattr(data, 'typecode'):
            assert data.typecode == self.color.dtype
        if hasattr(data, 'to_cffi'):
            self.data = data.to_cffi(FFI())
        elif hasattr(data, 'buffer_info'):
            addr, l = data.buffer_info()
            assert l == self.width * self.height * self.color.items
            self.data = FFI().cast(self.color.ctype + ' *', addr)
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
            raise ERROR_INVALID_FORMAT

    def ensure_color(self, color):
        self.suggest_color(color)
        if  self.color != color:
            raise ERROR_INVALID_FORMAT            

    def suggest_color(self, color):
        if self.color == FOURCC_VIRT:
            self.color = color

    def ensure_similar(self, image):
        self.ensure_shape(image)
        self.suggest_color(image.color)
        if self.color.items != image.color.items:
            raise ERROR_INVALID_FORMAT

    def alloc(self):
        if self.optimized_out:
            self.ctype = self.color.ctype
            self.csym = "__img%d" % self.count
            self.cdeclaration = "%s %s;\n" % (self.ctype, self.csym)
        else:            
            if self.data is None:
                items = self.width * self.height * self.color.items
                self.data = FFI().new(self.color.ctype + '[]', items)
            addr = FFI().cast('long', self.data)
            self.ctype = self.color.ctype + " *"
            self.csym = "__img%d" % self.count
            self.cdeclaration = "%s __restrict__ %s = ((%s) 0x%x);\n" % (
                    self.ctype, self.csym, self.ctype, addr)

    def getitem2d(self, node, channel, x, y):
        if self.optimized_out:
            return self.csym
        if channel is None:
            if self.color.items != 1:
                raise ERROR_INVALID_FORMAT("Cant access pixel of multi channel image without specifying channel.")
            channel = CHANNEL_0
        else:                
            channel = eval(channel.upper())
        name = self.csym
        ss = self.color.subsamp(channel)
        off =  self.color.offset(channel)
        stride_y = self.width * self.color.items
        stride_x = self.color.items
        if node.border_mode == BORDER_MODE_UNDEFINED:
            l = self.width * self.height - 1
            return "%s[clamp( %s(%s) * %d + %s(%s) * %d + %d, 0, %d )]" % (
                    name,     ss, y,stride_y, ss,x,  stride_x, off,    l)
        elif node.border_mode == BORDER_MODE_REPLICATE:
            return "%s[%s(clamp(%s, 0, %d)) * %d + %s(clamp(%s, 0, %d)) * %d + %d]" % (
                   name, ss, y, self.height-1, stride_y, ss, x, self.width-1, stride_x, off)
        else:
            raise NotImplementedError

    def getitem(self, node, channel, idx):
        if self.optimized_out:
            return self.csym        
        if isinstance(idx, tuple):
            return self.getitem2d(node, channel, *idx)

        name = self.csym
        if channel == 'data':
            return '%s[%s]' % (name, idx)
        if channel is None:
            if node.border_mode == BORDER_MODE_UNDEFINED:
                l = self.width * self.height * self.color.items - 1
                return "%s[clamp(%s, 0, %d)]" % (name, idx, l)
            else:
                raise NotImplementedError
        else:
            channel = eval(channel.upper())
            ss = self.color.subsamp(channel)
            off =  self.color.offset(channel)
            stride_x = self.color.items
            l = self.width * self.height * self.color.items - 1
            return "%s[%s(clamp(%s, 0, %d)) * %d + %d]" % (
                    name,  ss, idx,   l,  stride_x, off)

    def setitem(self, node, channel, idx, op, value):
        if self.optimized_out:
            return self.csym + ' = ' + value
        if node.convert_policy == CONVERT_POLICY_SATURATE:
            if op != '=':
                raise NotImplementedError
            return "%s = clamp(%s, %r, %r)" % (
                self.getitem(node, channel, idx), value,
                self.color.minval, self.color.maxval)
        return self.getitem(node, channel, idx) + ' ' + op + ' ' + value

    def getattr(self, node, attr):
        if attr == "width":
            return str(self.width)
        elif attr == "height":
            return str(self.height)
        elif attr == "pixels":
            return str(self.width * self.height)
        elif attr == "values":
            return str(self.width * self.height * self.color.items)
        elif attr == "data":
            return self.csym
        else:
            raise AttributeError

class ConstantImage(CoreImage):
    def __init__(self, width, height, value):
        self.width = width
        self.height = height
        self.value = value
        self.color = value_color_type(value)
        self.virtual = False
        self.producer = None

    def getitem(self, node, channel, idx):
        return str(self.value)

    def setitem(self, node, channel, idx, op, value):
        raise ERROR_INVALID_GRAPH("ConstantImage's are not writeable.")

    def alloc(self):
        self.cdeclaration = ''

class CoreGraph(object):
    default_context = None
    local_state = threading.local()
    local_state.current_graph = None
    show_source = False

    def __init__(self, context=None, early_verify=True):
        if context is None:
            if CoreGraph.default_context is None:
                CoreGraph.default_context = Context()
            context = CoreGraph.default_context
        self.context = context
        self.nodes = []
        self.early_verify = early_verify

    def add_reference(self, *args):
        return self.context.add_reference(*args)

    def __enter__(self):
        assert CoreGraph.local_state.current_graph is None
        CoreGraph.local_state.current_graph = self
        return self

    def __exit__(self, *args):
        assert CoreGraph.local_state.current_graph is self
        CoreGraph.local_state.current_graph = None

    @staticmethod
    def get_current_graph(none_check=True):
        if none_check and CoreGraph.local_state.current_graph is None:
            raise AssertionError("This function can only be called from within a 'width Graph():' block.")
        return CoreGraph.local_state.current_graph            

    def _add_node(self, node):
        self.nodes.append(node)

    def verify(self):
        self.images = set()        
        for node in self.nodes:
            for d in node.inputs + node.outputs + node.inouts:
                if isinstance(d, CoreImage):
                    self.images.add(d)
        self.nodes = self.schedule()

        for node in self.nodes:
            node.do_verify()

        # Virtual data produced
        for d in self.images:
            if d.virtual and d.producer is None:
                raise ERROR_INVALID_GRAPH("Virtual data never produced.")
            if d.color == FOURCC_VIRT:
                raise ERROR_INVALID_FORMAT("FOURCC_VIRT not resolved into specific type.")

        self.optimize()
        self.compile()

    def schedule(self):
        scheduler = Scheduler(self.nodes, self.images)
        one_order = []
        while scheduler.loaded_nodes:
            n = scheduler.loaded_nodes.pop()
            scheduler.fire(n)
            one_order.append(n)
        if scheduler.blocked_nodes:
            raise ERROR_INVALID_GRAPH("Loops not allowed in the graph.")
        return one_order

    def compile(self):
        for d in self.images:
            d.alloc()
        imgs = ''.join(d.cdeclaration for d in self.images)
        head = '''
            long clamp(long val, long min_val, long max_val) {
                if (val < min_val) return min_val;
                if (val > max_val) return max_val;
                return val;
            }
            long subsample(long val) {
                return val & (~1);
            }
        ''' + Enum(*status_codes, prefix="VX_").typedef('vx_status') + "\n"
        code = Code(imgs + "\n")
        code.includes.add('#include <math.h>')
        for n in self.nodes:
            assert not n.optimized_out
            n.compile(code)
        ffi = FFI()
        ffi.cdef("int func(void);")
        if self.show_source:
            print str(code)
        inc = '\n'.join(code.includes) + '\n'
        tmpdir = mkdtemp()
        mydir = os.path.dirname(os.path.abspath(__file__))
        try:
            lib = ffi.verify(inc + head + 
                             "int func(void) {" + str(code) + "return VX_SUCCESS;}",
                             extra_compile_args=["-O3", "-march=native", "-std=c99",
                                                 "-I" + mydir],
                             extra_link_args=code.extra_link_args,
                             tmpdir=tmpdir)
        finally:
            rmtree(tmpdir)
        self.compiled_func = lib.func

    def process(self):
        r = self.compiled_func()
        r = status_codes[r]
        return r

class Scheduler(object):
    def __init__(self, nodes, images):
        self.nodes = nodes
        self.images = images
        self.present = defaultdict(lambda : True)
        for d in self.images:
            self.present[d] = not d.virtual
        for n in self.nodes:
            for d in n.outputs + n.inouts:
                self.present[d] = False
        self.blocked_nodes = set(self.nodes)
        self.loaded_nodes = set()
        self.fire()

    def fire(self, node=None):
        if node is not None:
            for d in node.outputs:
                self.present[d] = True
        for n in list(self.blocked_nodes):
            if all(self.present[d] for d in n.inputs):
                self.blocked_nodes.remove(n)
                self.loaded_nodes.add(n)

def parse_signature(signature):
    sig = [v.strip().split(' ') for v in signature.split(',')]
    return [(v[0].lower(), v[-1]) for v in sig]

class Node(object):
    border_mode = BORDER_MODE_UNDEFINED
    border_mode_value = 0
    convert_policy = CONVERT_POLICY_TRUNCATE
    round_policy = ROUND_POLICY_TO_NEAREST_EVEN
    optimized_out = False

    def __init__(self, graph, *args, **kwargs):
        self.graph = graph
        self.inputs, self.outputs, self.inouts = [], [], []
        self.input_images, self.output_images, self.inout_images = {}, {}, {}
        for i, (direction, name) in enumerate(parse_signature(self.signature)):
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
                if isinstance(val, CoreImage):
                    self.input_images[name] = val
            elif direction == 'out':
                self.outputs.append(val)
                if isinstance(val, CoreImage):
                    self.output_images[name] = val
            elif direction == 'inout':
                self.inouts.append(val)
                if isinstance(val, CoreImage):
                    self.inout_images[name] = val                
            else:
                raise TypeError("Bad direction '%s' of argument '%s'" % (direction, name))
            setattr(self, name, val)
        self.setup()

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
                raise ERROR_MULTIPLE_WRITERS

        # Bidirection data not virtual
        for d in self.inouts:
            if d.virtual:
                raise ERROR_INVALID_GRAPH("Bidirection data cant be virtual.")

        for d in self.inputs:
            if isinstance(d, CoreImage) and (not d.width or not d.height):
                raise ERROR_INVALID_FORMAT
        self.verify()

    def ensure(self, condition):
        if not condition:
            raise ERROR_INVALID_FORMAT

class MergedNode(Node):

    def __init__(self, graph, nodes):
        self.original_nodes = nodes
        self.graph = graph
        self.inputs, self.outputs, self.inouts = set(), set(), set()
        for n in nodes:
            self.inputs |= set(n.inputs)
            self.outputs |= set(n.outputs)
            self.inouts |= set(n.inouts)
        self.inputs -= self.outputs
        self.inputs -= self.inouts

        self.inputs = list(self.inputs)
        self.outputs = list(self.outputs)
        self.inouts = list(self.inouts)
        self.input_images = {i: img for i, img in enumerate(self.inputs) 
                                    if isinstance(img, CoreImage)}
        self.output_images = {i: img for i, img in enumerate(self.outputs) 
                                     if isinstance(img, CoreImage)}
        self.inout_images = {i: img for i, img in enumerate(self.inouts) 
                                    if isinstance(img, CoreImage)}
        self.graph._add_node(self)
        for d in self.outputs + self.inouts:
            assert d.producer in nodes
            d.producer = self

