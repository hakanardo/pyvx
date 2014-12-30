import pyvx.model as model
from pyvx.types import *
from pyvx.codegen import Code
from cffi import FFI
from collections import defaultdict
from itertools import chain
import threading
import os
import re
from tempfile import mkdtemp
from shutil import rmtree

class Context(model.Context):
    def create_image(self, width, height, color):
        return CoreImage(width, height, color, context=self, virtual=False)
 
    def create_virtual_image(self, graph, width, height, color):
        return CoreImage(width, height, color, graph=graph, virtual=True)

    def create_graph(self, early_verify):
        return CoreGraph(self, early_verify)

    def create_scalar(self, data_type, initial_value):
        return Scalar(self, data_type, initial_value)

    def get_kernel(self, kernel):
        try:
            return Kernel(self, NodeMeta.kernels[kernel])
        except KeyError:
            raise InvalidValueError('Cant find kernel %r' % kernel)
        
# Placeholder for the value of required arguments not yet assigned.
class Missing(object): pass

# Placeholder for optional arguments not used.
class Unassigned(object): pass

class CoreImage(model.Image):
    count = 0
    optimized_out = False
    color_space = COLOR_SPACE_DEFAULT
    channel_range = CHANNEL_RANGE_FULL

    def __init__(self, width=0, height=0, color=DF_IMAGE_VIRT,
                 data=None, context=None, virtual=None, graph=None):
        if graph is None:
            graph = CoreGraph.get_current_graph(none_check=False)
        if context is None:
            context = graph.context
        if virtual is None:
            virtual = (color == DF_IMAGE_VIRT)
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
            self._set_data_pointer(data)
        else:
            self.data = None
        CoreImage.count += 1
        self.count = CoreImage.count

    @property
    def imagepatch_addressing(self):
        return self.image_format.imagepatch_addressing(self.width, self.height)

    @property
    def image_format(self):
        return image_format(self.color)

    def _set_data_pointer(self, data):
        if hasattr(data, 'typecode'):
            assert data.typecode == self.image_format.dtype
        if hasattr(data, 'to_cffi'):
            self.data = data.to_cffi(FFI())
        elif hasattr(data, 'buffer_info'):
            addr, l = data.buffer_info()
            assert l == self.width * self.height * self.image_format.items
            self.data = FFI().cast(self.image_format.ctype + ' *', addr)
        else:
            raise NotImplementedError(
                "Dont know how to convert %r to a cffi buffer" % data)
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
        if self.color != color:
            raise InvalidFormatError

    def suggest_color(self, color):
        if self.color == DF_IMAGE_VIRT:
            self.color = color

    def ensure_similar(self, image):
        self.ensure_shape(image)
        self.suggest_color(image.color)
        if self.image_format.items != image.image_format.items:
            raise InvalidFormatError

    def alloc(self):
        if self.optimized_out:
            self.ctype = self.image_format.ctype
            self.csym = "__img%d" % self.count
            self.cdeclaration = "%s %s;\n" % (self.ctype, self.csym)
        else:
            if self.data is None:
                items = self.width * self.height * self.image_format.items
                self.data = FFI().new(self.image_format.ctype + '[]', items)
            addr = FFI().cast('long', self.data)
            self.ctype = self.image_format.ctype + " *"
            self.csym = "__img%d" % self.count
            self.cdeclaration = "%s __restrict__ %s = ((%s) 0x%x);\n" % (
                self.ctype, self.csym, self.ctype, addr)

    def getitem2d(self, node, channel, x, y):
        if self.optimized_out:
            return self.csym
        if channel is None:
            if self.image_format.items != 1:
                raise InvalidFormatError(
                    "Cant access pixel of multi channel image without specifying channel.")
            channel = CHANNEL_0
        else:
            channel = eval(channel.upper())
        name = self.csym
        ss = self.image_format.subsamp(channel)
        off = self.image_format.offset(channel)
        stride_y = self.width * self.image_format.items
        stride_x = self.image_format.items
        if node.border_mode == BORDER_MODE_UNDEFINED:
            l = self.width * self.height - 1
            return "%s[clamp( %s(%s) * %d + %s(%s) * %d + %d, 0, %d )]" % (
                name,     ss, y, stride_y, ss, x,  stride_x, off,    l)
        elif node.border_mode == BORDER_MODE_REPLICATE:
            return "%s[%s(clamp(%s, 0, %d)) * %d + %s(clamp(%s, 0, %d)) * %d + %d]" % (
                   name, ss, y, self.height - 1, stride_y, ss, x, self.width - 1, stride_x, off)
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
                l = self.width * self.height * self.image_format.items - 1
                return "%s[clamp(%s, 0, %d)]" % (name, idx, l)
            else:
                raise NotImplementedError
        else:
            channel = eval(channel.upper())
            ss = self.image_format.subsamp(channel)
            off = self.image_format.offset(channel)
            stride_x = self.image_format.items
            l = self.width * self.height * self.image_format.items - 1
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
                self.image_format.minval, self.image_format.maxval)
        return self.getitem(node, channel, idx) + ' ' + op + ' ' + value

    def getattr(self, node, attr):
        if attr == "width":
            return str(self.width)
        elif attr == "height":
            return str(self.height)
        elif attr == "pixels":
            return str(self.width * self.height)
        elif attr == "values":
            return str(self.width * self.height * self.image_format.items)
        elif attr == "data":
            return self.csym
        else:
            raise AttributeError


class ConstantImage(CoreImage):

    def __init__(self, width, height, value):
        self.width = width
        self.height = height
        if isinstance(value, Scalar):
            value = value.value
        self.value = value
        self.color = value_color_type(value)
        self.virtual = False
        self.producer = None

    def getitem(self, node, channel, idx):
        return str(self.value)

    def setitem(self, node, channel, idx, op, value):
        raise InvalidGraphError("ConstantImage's are not writeable.")

    def alloc(self):
        self.cdeclaration = ''


class CoreGraph(model.Graph):
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
        self.compiled_func = None
        self.parameters = []

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
            raise AssertionError(
                "This function can only be called from within a 'width Graph():' block.")
        return CoreGraph.local_state.current_graph

    def _add_node(self, node):
        self.nodes.append(node)

    def verify(self):
        self.images = set()
        for node in self.nodes:
            for p in node.parameters:
                d = p.value
                if d is Missing:
                    raise InvalidParametersError('Required parameter "%s" missing on %r.' % (p.name, node))
                if isinstance(d, CoreImage):
                    self.images.add(d)
        self.nodes = self.schedule()

        for node in self.nodes:
            node.do_verify()

        # Virtual data produced
        for d in self.images:
            if d.virtual and d.producer is None:
                raise InvalidGraphError("Virtual data never produced.")
            if d.color == DF_IMAGE_VIRT:
                raise InvalidFormatError(
                    "DF_IMAGE_VIRT not resolved into specific type.")

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
            raise InvalidGraphError("Loops not allowed in the graph.")
        return one_order

    def optimize(self):
        pass

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
        '''
        code = Code(imgs + "\n")
        code.includes.add('#include <math.h>')
        code.includes.add('#include <VX/vx.h>')
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
        vxdir = os.path.join(mydir, 'inc', 'headers')
        try:
            lib = ffi.verify(inc + head +
                             "int func(void) {" + str(code) +
                             "return VX_SUCCESS;}",
                             extra_compile_args=["-O3", "-march=native", "-std=c99",
                                                 "-I" + mydir,
                                                 "-I" + vxdir],
                             extra_link_args=code.extra_link_args,
                             tmpdir=tmpdir)
        finally:
            rmtree(tmpdir)
        self.compiled_func = lib.func

    def process(self):
        if self.compiled_func is None:
            self.verify()
        return self.compiled_func()

    def add_parameter(self, parameter):
        if not isinstance(parameter, Parameter):
            raise InvalidReferenceError('The reference parameter is not a Parameter object')
        if parameter.node.graph is not self:
            raise InvalidParametersError('Parameter does not belong to a node in this graph')
        self.parameters.append(parameter)


class Scheduler(object):

    def __init__(self, nodes, images):
        self.nodes = nodes
        self.images = images
        self.present = defaultdict(lambda: True)
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
            # print n
            # for d in n.inputs:
            #     print '    ', d, self.present[d]
            if all(self.present[d] for d in n.inputs):
                self.blocked_nodes.remove(n)
                self.loaded_nodes.add(n)


class Scalar(model.Scalar):

    def __init__(self, context, data_type, value):
        self.context = context
        self.data_type = data_type
        self.value = value
        self.producer = None

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __div__(self, other):
        return self.value / other

    def __floordiv__(self, other):
        return self.value // other

    def __radd__(self, other):
        return other + self.value

    def __rsub__(self, other):
        return other - self.value

    def __rmul__(self, other):
        return other * self.value

    def __rdiv__(self, other):
        return other / self.value

    def __rfloordiv__(self, other):
        return other // self.value

    __floordiv__ = __div__
    __rfloordiv__ = __rdiv__

    def __pow__(self, other):
        return self.value ** other

    def __rpow__(self, other):
        return other ** self.value

    def __mod__(self, other):
        return self.value % other

    def __rmod__(self, other):
        return other % self.value

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __lshift__(self, other):
        return self.value << other

    def __rlshift__(self, other):
        return other << self.value

    def __rshift__(self, other):
        return self.value >> other

    def __rrshift__(self, other):
        return other >> self.value

    def __and__(self, other):
        return self.value & other

    def __rand__(self, other):
        return other & self.value

    def __or__(self, other):
        return self.value | other

    def __ror__(self, other):
        return other | self.value

    def __xor__(self, other):
        return self.value ^ other

    def __rxor__(self, other):
        return other ^ self.value

    def __cmp__(self, other):
        return cmp(self.value, other)

    def __nonzero__(self):
        raise self.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class Kernel(model.Kernel):
    def __init__(self, context, node_class):
        self.context = context
        self.name = node_class.kernel_name
        self.enumeration = node_class.kernel_enum
        self.node_class = node_class


class Parameter(model.Parameter):
    vxtype = TYPE_PARAMETER

    def __init__(self, node, name, index, direction, data_type, state, value):
        self.context = node.graph.context
        self.node = node
        self.name = name
        self._index = index
        self._direction = direction
        self._data_type = data_type
        self._state = state
        self.value = value

    @property
    def value(self):
        return self.ref

    @value.setter
    def value(self, value):
        if value is Missing or value is Unassigned:
            self.ref = value
            return
        if repr(value).startswith('<cdata \'char *\''): # XXX: Hack!
            value = ffi.string(value)
        if not isinstance(value, model.VxObject):
            value = Scalar(self.context, self.data_type, value)
        if self.data_type < TYPE_SCALAR_MAX or self.data_type == TYPE_STRING:
            assert value.type == TYPE_SCALAR
        else:
            assert value.type == self.data_type
        self.ref = value

class param(object):
    def __init__(self, name, direction, data_type, default=Missing):
        self.name = name
        self.direction = direction
        self.data_type = data_type
        self.default = default
        self.state = PARAMETER_STATE_REQUIRED if default is Missing \
                     else PARAMETER_STATE_OPTIONAL

    def __get__(self, instance, owner):
        assert instance.parameters[self.index].name == self.name
        return instance.parameters[self.index].ref

    def __set__(self, instance, value):
        assert instance.parameters[self.index].name == self.name        
        instance.parameters[self.index].ref = value
    

class NodeMeta(model.VxObjectMeta):
    kernels = {}
    def __new__(cls, name, bases, attrs):
        cls = model.VxObjectMeta.__new__(cls, name, bases, attrs)
        for i, p in enumerate(cls.signature):
            p.index = i
            setattr(cls, p.name, p)
        if hasattr(cls, 'kernel_enum'):
            assert cls.kernel_enum not in NodeMeta.kernels
            NodeMeta.kernels[cls.kernel_enum] = cls
        if 'kernel_name' not in attrs:
            assert name.endswith('Node')
            cls.kernel_name = name[:-4]
        assert cls.kernel_name not in NodeMeta.kernels
        NodeMeta.kernels[cls.kernel_name] = cls
        return cls

class Node(model.Node):
    __metaclass__ = NodeMeta
    border_mode = BORDER_MODE_UNDEFINED
    border_mode_value = 0
    convert_policy = CONVERT_POLICY_WRAP
    round_policy = ROUND_POLICY_TO_NEAREST_EVEN
    optimized_out = False
    signature = ()

    def __init__(self, graph, *args, **kwargs):
        self.graph = graph
        self.context = graph.context
        self.parameters = [Parameter(self, p.name, p.index, p.direction, 
                                     p.data_type, p.state, p.default)
                           for p in self.signature]
        for param in self.parameters:
            if param.index < len(args):
                param.value = args[param.index]
                if param.name in kwargs:
                    raise TypeError(
                        "Got multiple values for keyword argument '%s'" % name)
            elif param.name in kwargs:
                param.value = kwargs[name]
            elif param.value is Missing:
                if kwargs.get('_ignore_missin_parameters', False): 
                    param.value = Missing
                else:
                    raise TypeError("Required argument missing")
        self.setup()

    @property
    def inputs(self):
        return [p.value for p in self.parameters 
                if p.direction == INPUT and p.value is not Unassigned]

    @property
    def outputs(self):
        return [p.value for p in self.parameters 
                if p.direction == OUTPUT and p.value is not Unassigned]

    @property
    def inouts(self):
        return [p.value for p in self.parameters 
                if p.direction == BIDIRECTIONAL and p.value is not Unassigned]

    @property
    def input_images(self):
        return [i for i in self.inputs if isinstance(i, CoreImage)]

    @property
    def output_images(self):
        return [i for i in self.outputs if isinstance(i, CoreImage)]

    @property
    def inout_images(self):
        return [i for i in self.inouts if isinstance(i, CoreImage)]

    def setup(self):
        self.graph._add_node(self)
        for d in self.outputs + self.inouts:
            if d is not Missing and d.producer is None:
                d.producer = self
        if self.graph.early_verify:
            self.do_verify()

    def do_verify(self):
        # All arguments are assigned
        for d in self.inputs + self.outputs + self.inouts:
            if d is Missing:
                raise InvalidParametersError('Required parameter missing')

        # Signle writer
        for d in self.outputs + self.inouts:
            if d is None:
                continue
            if d.producer is None:
                d.producer = self
            if d.producer is not self:
                raise MultipleWritersError

        # Bidirection data not virtual
        for d in self.inouts:
            if d.virtual:
                raise InvalidGraphError("Bidirection data cant be virtual.")

        for d in self.inputs:
            if isinstance(d, CoreImage) and (not d.width or not d.height):
                raise InvalidFormatError('Input image dimentions unknown')
        self.verify()

    def ensure(self, condition):
        if not condition:
            raise InvalidFormatError


class MergedNode(Node):

    def __init__(self, graph, nodes):
        self.original_nodes = nodes
        self.graph = graph
        inputs, outputs, inouts = set(), set(), set()
        for n in nodes:
            inputs |= set(n.inputs)
            outputs |= set(n.outputs)
            inouts |= set(n.inouts)
        inputs -= outputs
        inputs -= inouts

        inputs = list(inputs)
        outputs = list(outputs)
        inouts = list(inouts)
        self.graph._add_node(self)
        for d in outputs + inouts:
            assert d.producer in nodes
            d.producer = self

        self.parameters = [Parameter(self, None, None, INPUT, ref.type, 
                                     PARAMETER_STATE_REQUIRED, ref)
                           for ref in inputs] + \
                          [Parameter(self, None, None, OUTPUT, ref.type, 
                                     PARAMETER_STATE_REQUIRED, ref)
                           for ref in outputs] + \
                          [Parameter(self, None, None, BIDIRECTIONAL, ref.type, 
                                     PARAMETER_STATE_REQUIRED, ref)
                           for ref in inouts]

        assert self.inputs == inputs
        assert self.outputs == outputs
        assert self.inouts == inouts
