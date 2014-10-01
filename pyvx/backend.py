from pyvx.types import *
from pyvx.codegen import Code
from cffi import FFI
from collections import defaultdict
from itertools import chain

class Context(object):
    pass

class Image(object):
    count = 0

    def __init__(self, width=0, height=0, color=FOURCC_VIRT,
                 data=None, context=None, virtual=None, graph=None):
        if graph is None:
            graph = Graph.current_graph
        if context is None:
            context = graph.context
        if virtual is None:
            virtual = (color == FOURCC_VIRT)
        if virtual:
            assert graph is not None
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
        Image.count += 1
        self.count = Image.count

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
            self.data = FFI().new(self.color.ctype + '[]', items)
        addr = FFI().cast('long', self.data)
        self.ctype = self.color.ctype + " *"
        self.csym = "__img%d" % self.count
        self.cdeclaration = "%s __restrict__ %s = ((%s) 0x%x);\n" % (
                self.ctype, self.csym, self.ctype, addr)

    def getitem2d(self, node, channel, x, y):
        if channel is None:
            if self.color.items != 1:
                raise InvalidFormatError("Cant access pixel of multi channel image without specifying channel.")
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
        if node.convert_policy == CONVERT_POLICY_SATURATE:
            if op != '=':
                raise NotImplementedError
            return "%s = clamp(%s, %r, %r)" % (
                self.getitem(node, channel, idx), value,
                self.color.minval, self.color.maxval)
        return self.getitem(node, channel, idx) + op + value

    def getattr(self, node, attr):
        if attr == "width":
            return str(self.width)
        elif attr == "height":
            return str(self.height)
        elif attr == "pixels":
            return str(self.width * self.height)
        elif attr == "values":
            return str(self.width * self.height * self.color.items)
        else:
            raise AttributeError

    @property
    def channel_r(self):
        return ChannelExtract(self, CHANNEL_R)
        
    @property
    def channel_g(self):
        return ChannelExtract(self, CHANNEL_G)
        
    @property
    def channel_b(self):
        return ChannelExtract(self, CHANNEL_B)
        
    @property
    def channel_u(self):
        return ChannelExtract(self, CHANNEL_U)
        
    @property
    def channel_y(self):
        return ChannelExtract(self, CHANNEL_Y)
        
    @property
    def channel_v(self):
        return ChannelExtract(self, CHANNEL_V)
        
    @property
    def channel_a(self):
        return ChannelExtract(self, CHANNEL_A)
        
    @property
    def channel_0(self):
        return ChannelExtract(self, CHANNEL_0)
        
    @property
    def channel_1(self):
        return ChannelExtract(self, CHANNEL_1)
        
    @property
    def channel_2(self):
        return ChannelExtract(self, CHANNEL_2)

    @property
    def channel_3(self):
        return ChannelExtract(self, CHANNEL_3)
                
    def make_similar_image(self, other):
        if isinstance(other, Image):
            return other
        return ConstantImage(self.width, self.height, other)

    def __add__(self, other):
        return Add(self, self.make_similar_image(other))

    def __sub__(self, other):
        return Subtract(self, self.make_similar_image(other))

    def __mul__(self, other):
        return Multiply(self, self.make_similar_image(other))

    def __div__(self, other):
        return Divide(self, self.make_similar_image(other))

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return Subtract(self.make_similar_image(other), self)

    def __rdiv__(self, other):
        return Divide(self.make_similar_image(other), self)

    __floordiv__ = __div__
    __rfloordiv__ = __rdiv__

    def __pow__(self, other):
        return Power(self, self.make_similar_image(other))

    def __rpow__(self, other):
        return Power(self.make_similar_image(other), self)

    def __mod__(self, other):
        return Modulus(self, self.make_similar_image(other))

    def __rmod__(self, other):
        return Modulus(self.make_similar_image(other), self)

    def __truediv__(self, other):
        res = TrueDivide(self, self.make_similar_image(other))
        return res

    def __rtruediv__(self, other):
        res = TrueDivide(self.make_similar_image(other), self)
        return res

    def __lshift__(self, other):
        return LeftShift(self, self.make_similar_image(other))

    def __rlshift__(self, other):
        return LeftShift(self.make_similar_image(other), self)

    def __rshift__(self, other):
        return RightShift(self, self.make_similar_image(other))

    def __rrshift__(self, other):
        return RightShift(self.make_similar_image(other), self)

    def __and__(self, other):
        return And(self, self.make_similar_image(other))

    def __rand__(self, other):
        return And(self.make_similar_image(other), self)

    def __or__(self, other):
        return Or(self, self.make_similar_image(other))

    def __ror__(self, other):
        return Or(self.make_similar_image(other), self)

    def __xor__(self, other):
        return Xor(self, self.make_similar_image(other))

    def __xror__(self, other):
        return Xor(self.make_similar_image(other), self)

    def __lt__(self, other):
        return Compare(self, "<", self.make_similar_image(other))

    def __le__(self, other):
        return Compare(self, "<=", self.make_similar_image(other))

    def __eq__(self, other):
        return Compare(self, "==", self.make_similar_image(other))

    def __ne__(self, other):
        return Compare(self, "!=", self.make_similar_image(other))

    def __gt__(self, other):
        return Compare(self, ">", self.make_similar_image(other))

    def __ge__(self, other):
        return Compare(self, ">=", self.make_similar_image(other))

    def __nonzero__(self):
        raise ValueError("The truth value of an Image is ambigous.")

class ConstantImage(Image):
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
        raise InvalidGraphError("ConstantImage's are not writeable.")

    def alloc(self):
        self.cdeclaration = ''

class Graph(object):
    default_context = None
    current_graph = None

    def __init__(self, context=None, early_verify=True):
        if context is None:
            if Graph.default_context is None:
                Graph.default_context = Context()
            context = Graph.default_context
        self.context = context
        self.nodes = []
        self.data_objects = set()
        self.early_verify = early_verify

    def __enter__(self):
        assert Graph.current_graph is None
        Graph.current_graph = self

    def __exit__(self, *args):
        assert Graph.current_graph is self
        Graph.current_graph = None

    def _add_node(self, node):
        self.nodes.append(node)
        for d in node.inputs + node.outputs + node.inouts:
            self.data_objects.add(d)

    def verify(self):
        self.images = [d for d in self.data_objects if isinstance(d, Image)]
        self.nodes = self.schedule()

        for node in self.nodes:
            node.do_verify()

        # Virtual data produced
        for d in self.images:
            if d.virtual and d.producer is None:
                raise InvalidGraphError("Virtual data never produced.")
            if d.color == FOURCC_VIRT:
                raise InvalidFormatError("FOURCC_VIRT not resolved into specific type.")

        self.compile()

    def schedule(self):
        present = defaultdict(lambda : True)
        for d in self.images:
            present[d] = not d.virtual
        for n in self.nodes:
            for d in n.outputs + n.inouts:
                present[d] = False
        worklist = self.nodes[:]
        inorder = []
        while worklist:
            remaining = []
            for n in worklist:
                if all(present[d] for d in n.inputs):
                    inorder.append(n)
                    for d in n.outputs:
                        present[d] = True
                else:
                    remaining.append(n)
            if len(worklist) == len(remaining):
                raise InvalidGraphError("Loops not allowed in the graph.")
            worklist = remaining
        return inorder

    def compile(self):
        for d in self.images:
            d.alloc()
        imgs = ''.join(d.cdeclaration for d in self.images)
        code = Code('''
                    long clamp(long val, long min_val, long max_val) {
                        if (val < min_val) return min_val;
                        if (val > max_val) return max_val;
                        return val;
                    }
                    long subsample(long val) {
                        return val & (~1);
                    }
                    \n''' + imgs)
        for n in self.nodes:
            n.compile(code)
        ffi = FFI()
        ffi.cdef("void func(void);")
        #print str(code)
        inc = "#include <math.h>\n"
        lib = ffi.verify(inc + "void func(void) {" + str(code) + "}",
                         extra_compile_args=["-O3", "-march=native", "-std=c99"])
        self.compiled_func = lib.func

    def process(self):
        self.compiled_func()

class Node(object):
    border_mode = BORDER_MODE_UNDEFINED
    border_mode_value = 0
    convert_policy = CONVERT_POLICY_TRUNCATE
    round_policy = ROUND_POLICY_TO_NEAREST_EVEN

    def __init__(self, graph, *args, **kwargs):
        self.graph = graph
        self.inputs, self.outputs, self.inouts = [], [], []
        self.input_images, self.output_images, self.inout_images = {}, {}, {}
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
                if isinstance(val, Image):
                    self.input_images[name] = val
            elif direction == 'out':
                self.outputs.append(val)
                if isinstance(val, Image):
                    self.output_images[name] = val
            elif direction == 'inout':
                self.inouts.append(val)
                if isinstance(val, Image):
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
                raise MultipleWritersError

        # Bidirection data not virtual
        for d in self.inouts:
            if d.virtual:
                raise InvalidGraphError("Bidirection data cant be virtual.")

        for d in self.inputs:
            if isinstance(d, Image) and (not d.width or not d.height):
                raise InvalidFormatError
        self.verify()

    def ensure(self, condition):
        if not condition:
            raise InvalidFormatError


class ElementwiseNode(Node):
    small_ints = ('uint8_t', 'int8_t', 'uint16_t', 'int16_t')

    def verify(self):
        inputs = self.input_images.values()
        outputs = self.output_images.values() + self.inout_images.values()
        color = result_color(*[i.color for i in inputs])
        for img in outputs:
            img.suggest_color(color)
            img.ensure_similar(inputs[0])
            if self.convert_policy == CONVERT_POLICY_SATURATE:
                if img.color.ctype not in self.small_ints:
                    raise InvalidFormatError("Saturated arithmetic only supported for 8- and 16- bit integers.")

    def tmptype(self, ctype):
        if ctype in self.small_ints:
            return 'long'
        return ctype

    def compile(self, code):
        iin = self.input_images.items() + self.inout_images.items()
        iout = self.output_images.items() + self.inout_images.items()
        magic = {'__tmp_image_%s' % name : img 
                 for name, img in iin + iout}
        setup = ''.join("%s %s;" % (self.tmptype(img.color.ctype), name)
                        for name, img in iin + iout)
        inp = ''.join("%s = __tmp_image_%s[__i];" % (name, name)
                      for name, img in iin)
        outp = ''.join("__tmp_image_%s[__i] = %s;" % (name, name)
                       for name, img in iout)
        head = "for (long __i = 0; __i < __tmp_image_%s.values; __i++) " % iin[0][0]
        body = inp + self.body + outp
        block = head + "{" + body + "}"
        code.add_block(self, setup + block, **magic)


class AddNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 + in2;"

def Add(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    AddNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class SubtractNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 - in2;"

def Subtract(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    SubtractNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class MultiplyNode(ElementwiseNode):
    signature = "in in1, in in2, in scale, in convert_policy, in round_policy, out out"

    @property
    def body(self):
        if self.round_policy is ROUND_POLICY_TO_ZERO:
            return "out = in1 * in2 * %r;" % self.scale
        elif self.round_policy is ROUND_POLICY_TO_NEAREST_EVEN:
            return "out = rint(in1 * in2 * %r);" % self.scale
        else:
            raise NotImplementedError

def Multiply(in1, in2, scale=1, convert_policy=CONVERT_POLICY_TRUNCATE, round_policy=ROUND_POLICY_TO_ZERO):
    res = Image()
    MultiplyNode(Graph.current_graph, in1, in2, scale, convert_policy, round_policy, res)
    return res

class DivideNode(ElementwiseNode):
    signature = "in in1, in in2, in scale, in convert_policy, in round_policy, out out"

    @property
    def body(self):
        if self.round_policy is ROUND_POLICY_TO_ZERO:
            return "out = (in1 * %r) / in2;" % self.scale
        elif self.round_policy is ROUND_POLICY_TO_NEAREST_EVEN:
            return "out = rint((in1 * %r) / in2);" % self.scale
        else:
            raise NotImplementedError

def Divide(in1, in2, scale=1, convert_policy=CONVERT_POLICY_TRUNCATE, round_policy=ROUND_POLICY_TO_ZERO):
    res = Image()
    DivideNode(Graph.current_graph, in1, in2, scale, convert_policy, round_policy, res)
    return res

class TrueDivideNode(ElementwiseNode):
    signature = "in in1, in in2, out out"
    body = "out = ((double) in1) / ((double) in2);"

def TrueDivide(in1, in2):
    res = Image(color=FOURCC_F64)
    TrueDivideNode(Graph.current_graph, in1, in2, res)
    return res

class PowerNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = pow(in1, in2);"

def Power(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    PowerNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class ModulusNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 % in2;"

def Modulus(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    ModulusNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class LeftShiftNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 << in2;"

def LeftShift(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    LeftShiftNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class RightShiftNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 >> in2;"

def RightShift(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    RightShiftNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class AndNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 & in2;"

def And(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    AndNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class OrNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 | in2;"

def Or(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    OrNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class XorNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 ^ in2;"

def Xor(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    XorNode(Graph.current_graph, in1, in2, convert_policy, res)
    return res

class CompareNode(ElementwiseNode):
    signature = "in in1, in op, in in2, out out"

    @property
    def body(self):
        return "out = in1 %s in2;" % self.op

def Compare(in1, op, in2):
    res = Image()
    res.color = FOURCC_U8
    CompareNode(Graph.current_graph, in1, op, in2, res)
    return res



class ChannelExtractNode(Node):
    signature = "in input, in channel, out output"

    def verify(self):
        if self.channel not in self.input.color.channels:
            raise InvalidFormatError(
                'Cant extract channel %s from %s image.' % (
                    self.channel.__name__, self.input.color.__name__))
        self.output.ensure_color(FOURCC_U8)        
        self.output.ensure_shape(self.input)

    def compile(self, code):
        code.add_block(self, """
            for (long i = 0; i < out.pixels; i++) {
                out[i] = input.%s[i];
            }
            """ % self.channel.__name__.lower(), 
            input=self.input, out=self.output)


def ChannelExtract(input, channel):
    output = Image()
    ChannelExtractNode(Graph.current_graph,
                          input, channel, output)
    return output


class Gaussian3x3Node(Node):
    signature = "in input, out output"

    def verify(self):
        self.ensure(self.input.color.items == 1)
        self.output.ensure_similar(self.input)

    def compile(self, code):
        code.add_block(self, """
            for (long y = 0; y < img.height; y++) {
                for (long x = 0; x < img.width; x++) {
                    res[x, y] = (1*img[x-1, y-1] + 2*img[x, y-1] + 1*img[x+1, y-1] +
                                 2*img[x-1, y]   + 4*img[x, y]   + 2*img[x+1, y]   +
                                 1*img[x-1, y+1] + 2*img[x, y+1] + 1*img[x+1, y+1]) / 16;
                }
            }
            """, img=self.input, res=self.output)

def Gaussian3x3(input):
    output = Image()
    Gaussian3x3Node(Graph.current_graph, input, output)
    return output


class Sobel3x3Node(Node):
    signature = 'in input, out output_x, out output_y'

    def verify(self):
        self.ensure(self.input.color.items == 1)
        if self.input.color in [FOURCC_U8, FOURCC_U16]:
            ot = FOURCC_S16
        else:
            ot = signed_color(self.input.color)
        self.output_x.suggest_color(ot)
        self.output_y.suggest_color(ot)
        self.output_x.ensure_similar(self.input)
        self.output_y.ensure_similar(self.input)

    def compile(self, code):
        code.add_block(self, """
            for (long y = 0; y < img.height; y++) {
                for (long x = 0; x < img.width; x++) {
                    dx[x, y] = (-1*img[x-1, y-1] + 1*img[x+1, y-1] +
                                -2*img[x-1, y]   + 2*img[x+1, y]   +
                                -1*img[x-1, y+1] + 1*img[x+1, y+1]);
                    dy[x, y] = (-1*img[x-1, y-1] - 2*img[x, y-1] - 1*img[x+1, y-1] +
                                 1*img[x-1, y+1] + 2*img[x, y+1] + 1*img[x+1, y+1]);
                }
            }
            """, img=self.input, dx=self.output_x, dy=self.output_y)

def Sobel3x3(input):
    dx, dy = Image(), Image()
    Sobel3x3Node(Graph.current_graph, input, dx, dy)
    return dx, dy


class MagnitudeNode(ElementwiseNode):
    signature = 'in grad_x, in grad_y, out mag'
    convert_policy = CONVERT_POLICY_SATURATE

    def verify(self):
        self.ensure(self.grad_x.color.items == 1)
        self.ensure(self.grad_y.color.items == 1)
        it = result_color(self.grad_x.color, self.grad_y.color)
        if it in [FOURCC_U8, FOURCC_U16, FOURCC_S8, FOURCC_S16]:
            ot = FOURCC_U16
        else:
            ot = it
        self.mag.suggest_color(ot)
        self.mag.ensure_similar(self.grad_x)
        self.mag.ensure_similar(self.grad_y)

    body = "mag = sqrt( grad_x * grad_x + grad_y * grad_y );"


def Magnitude(grad_x, grad_y):
    mag = Image()
    MagnitudeNode(Graph.current_graph, grad_x, grad_y, mag)
    return mag


class PhaseNode(ElementwiseNode):
    signature = 'in grad_x, in grad_y, out orientation'

    def verify(self):
        self.ensure(self.grad_x.color.items == 1)
        self.ensure(self.grad_y.color.items == 1)
        self.orientation.suggest_color(FOURCC_U8)
        self.orientation.ensure_similar(self.grad_x)
        self.orientation.ensure_similar(self.grad_y)

    body = "orientation = (atan2(grad_y, grad_x) + M_PI) * (255.0 / 2.0 / M_PI);"

def Phase(grad_x, grad_y):
    ph = Image()
    PhaseNode(Graph.current_graph, grad_x, grad_y, ph)
    return ph


class AccumulateImageNode(Node):
    signature = 'in input, inout accum'

    def verify(self):
        pass

def AccumulateImage(input):
    accum = Image()
    AccumulateImageNode(Graph.current_graph, input, accum)
    return accum
