from pyvx.backend import *
from cffi import FFI
import os

class Image(CoreImage):

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
        if CoreGraph.get_current_graph(none_check=False) is None:
            return self is other
        return Compare(self, "==", self.make_similar_image(other))

    def __ne__(self, other):
        return Compare(self, "!=", self.make_similar_image(other))

    def __gt__(self, other):
        return Compare(self, ">", self.make_similar_image(other))

    def __ge__(self, other):
        return Compare(self, ">=", self.make_similar_image(other))

    def __nonzero__(self):
        raise ValueError("The truth value of an Image is ambigous.")

    def __hash__(self):
        if CoreGraph.get_current_graph(none_check=False) is None:
            return object.__hash__(self)
        else:
            raise TypeError("Images are not hasable when used within 'with Graph():' blocks.")


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

    def compile(self, code, noloop=False):
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
        if noloop:
            head = ""
        else:
            head = "for (long __i = 0; __i < __tmp_image_%s.values; __i++) " % iin[0][0]
        body = inp + self.body + outp
        block = head + "{" + body + "}"
        code.add_block(self, setup + block, **magic)

class MergedElementwiseNode(MergedNode):
    def compile(self, code):
        img = self.original_nodes[0].input_images.values()[0]
        code.add_code("\n// MergedElementwiseNode\n")
        code.indent_level += 4
        code.add_code("for (long __i = 0; __i < %s; __i++) {\n" %
                       img.getattr(self, "values"))
        for n in self.original_nodes:
            n.compile(code, True)
        code.indent_level -= 4
        code.add_code("}\n")

class AddNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 + in2;"

def Add(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    AddNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class SubtractNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 - in2;"

def Subtract(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    SubtractNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
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
    MultiplyNode(CoreGraph.get_current_graph(), in1, in2, scale, convert_policy, round_policy, res)
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
    DivideNode(CoreGraph.get_current_graph(), in1, in2, scale, convert_policy, round_policy, res)
    return res

class TrueDivideNode(ElementwiseNode):
    signature = "in in1, in in2, out out"
    body = "out = ((double) in1) / ((double) in2);"

def TrueDivide(in1, in2):
    res = Image(color=FOURCC_F64)
    TrueDivideNode(CoreGraph.get_current_graph(), in1, in2, res)
    return res

class PowerNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = pow(in1, in2);"

def Power(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    PowerNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class ModulusNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 % in2;"

def Modulus(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    ModulusNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class LeftShiftNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 << in2;"

def LeftShift(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    LeftShiftNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class RightShiftNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 >> in2;"

def RightShift(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    RightShiftNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class AndNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 & in2;"

def And(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    AndNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class OrNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 | in2;"

def Or(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    OrNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class XorNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = in1 ^ in2;"

def Xor(in1, in2, convert_policy=CONVERT_POLICY_TRUNCATE):
    res = Image()
    XorNode(CoreGraph.get_current_graph(), in1, in2, convert_policy, res)
    return res

class CompareNode(ElementwiseNode):
    signature = "in in1, in op, in in2, out out"

    @property
    def body(self):
        return "out = in1 %s in2;" % self.op

def Compare(in1, op, in2):
    res = Image()
    res.color = FOURCC_U8
    CompareNode(CoreGraph.get_current_graph(), in1, op, in2, res)
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
    ChannelExtractNode(CoreGraph.get_current_graph(),
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
    Gaussian3x3Node(CoreGraph.get_current_graph(), input, output)
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
    Sobel3x3Node(CoreGraph.get_current_graph(), input, dx, dy)
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
    MagnitudeNode(CoreGraph.get_current_graph(), grad_x, grad_y, mag)
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
    PhaseNode(CoreGraph.get_current_graph(), grad_x, grad_y, ph)
    return ph


class AccumulateImageNode(Node):
    signature = 'in input, inout accum'

    def verify(self):
        pass

def AccumulateImage(input):
    accum = Image()
    AccumulateImageNode(CoreGraph.get_current_graph(), input, accum)
    return accum
    

ffi = FFI()
ffi.cdef("""
        struct vlcplay {
            int width, height;
            ...;
        };

        struct vlcplay *vlcplay_create(char *path);
        void vlcplay_next(struct vlcplay *m, unsigned char *buf);
        void vlcplay_release(struct vlcplay **m);
         """)
mydir = os.path.dirname(os.path.abspath(__file__))
lib = ffi.verify("""
                 #include "vlcplay.h"
                 """, 
                 extra_compile_args=['-O3', '-I' + mydir],
                 sources=[os.path.join(mydir, f) for f in ['vlcplay.c']],
                 libraries=['vlc'])

class PlayNode(Node):
    signature = 'in path, out output'

    def verify(self):
        self.player = lib.vlcplay_create(self.path)
        self.output.ensure_shape(self.player.width, self.player.height)
        self.output.ensure_color(FOURCC_RGB)
        self.output.force()

    def compile(self, code):
        adr = int(ffi.cast('long', self.player))
        code.add_block(self, "vlcplay_next((void *)0x%x, img.data);" % adr, img=self.output);
        code.extra_link_args.append(ffi.verifier.modulefilename)

def Play(path):
    img = Image()
    PlayNode(CoreGraph.get_current_graph(), path, img)
    return img