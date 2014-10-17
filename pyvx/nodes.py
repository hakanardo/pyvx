"""
:mod:`pyvx.nodes` --- Node implementations
==========================================

This module contains the implementations of the different processing nodes. They
are implemented by subclassing ``Node`` and overriding ``signature``, ``verify()``
and ``compile()``. As an example here is the implementation of the Gaussian3x3Node:

.. code-block:: python 

    class Gaussian3x3Node(Node):
        signature = "in input, out output"

        def verify(self):
            self.ensure(self.input.color.items == 1)
            self.output.ensure_similar(self.input)

        def compile(self, code):
            code.add_block(self, \"""
                for (long y = 0; y < img.height; y++) {
                    for (long x = 0; x < img.width; x++) {
                        res[x, y] = (1*img[x-1, y-1] + 2*img[x, y-1] + 1*img[x+1, y-1] +
                                     2*img[x-1, y]   + 4*img[x, y]   + 2*img[x+1, y]   +
                                     1*img[x-1, y+1] + 2*img[x, y+1] + 1*img[x+1, y+1]) / 16;
                    }
                }
                \""", img=self.input, res=self.output)

- ``Node.signature`` is a string specifying the argument names and there directions 
  (in, out or inout). The arguments will be assigned to attributes with the same
  names when the node is created. The arguments can be given default values by 
  assigning them to class-level attributes.

- ``Node.verify(self)`` is called during the verification phase and can assume that all 
  nodes it depend on have verified successfully. It is supposed to check the
  arguments and raise one of the ``VerificationError``'s if they don't make sense. Also
  any output images with width/height set to 0 or color set to FOURCC_VIRT should be given 
  proper values. There are a few helper methods available described below.

- ``Node.compile(self, code)`` is called after verification of the entire graph was
  successful. It is responsible for generating C code implementing the node using
  the ``code`` argument. It has a notion of magic variables used to abstract away 
  the pixel access calculations. See :class:`pyvx.codegen.Code`. 

To simplify the implementation of ``verify()`` there are a few helper functions. They
will updated the properties of the images if they've not yet been set, and 
raise ``ERROR_INVALID_FORMAT`` if they were set to something different.

- ``Image.ensure_shape(self, other_image)`` Ensures ``self`` has the same width
  and height as other_image.

- ``Image.ensure_shape(self, width, height)`` Ensures ``self`` has the width 
  ``width`` an the height ``height``.

- ``Image.ensure_color(self, color)`` Ensures that the color of ``self`` is ``color``

- ``Image.suggest_color(self, color)`` Sets ``self.color`` to ``color`` if it is not 
  yet specified.

- ``Image.ensure_similar(self, image)`` Ensures that the shape and number of channels
  of ``self`` and ``image`` are the same, and suggests that the color of ``self`` is 
  the same as ``image``.

- ``Node.ensure(self, condition)`` raises ``ERROR_INVALID_FORMAT`` if ``condition``
  is ``false``.

To allow for a general implementation of the graph optimizations, there are special 
subclasses of ``Node`` that should be used. For strictly element-wise operations
there is ``ElementwiseNode``. It expects a ``body`` attribute with the code
that will be executed for each pixel. This code can assume that there are variables
with the same name as the arguments available. For the input arguments those 
variables contains the pixel values of the current pixel and it is the responsibility
of this code to assign the output variables. As an example, here is the implementation
of the ``PowerNode``:

.. code-block:: python 

    class PowerNode(ElementwiseNode):
        signature = "in in1, in in2, in convert_policy, out out"
        body = "out = pow(in1, in2);"

If some logic is needed to produce the code, ``body`` can be implemented as a 
``property``. That is for example done by the ``BinaryOperationNode``:

.. code-block:: python 

    class BinaryOperationNode(ElementwiseNode):
        signature = "in in1, in op, in in2, in convert_policy, out out"
        @property
        def body(self):
            return "out = in1 %s in2;" % self.op

The default ``ElementwiseNode.verify()`` will ensure that the output images are of the same size
as the input images and will use :func:`pyvx.types.result_color`  to 
replace  ``FOURCC_VIRT`` colors among the output images. If this is not appropriate 
it can be overridden.

"""
from pyvx.backend import *
import cffi
import os

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
                    raise ERROR_INVALID_FORMAT("Saturated arithmetic only supported for 8- and 16- bit integers.")

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

class BinaryOperationNode(ElementwiseNode):
    signature = "in in1, in op, in in2, in convert_policy, out out"
    @property
    def body(self):
        return "out = in1 %s in2;" % self.op

class MultiplyNode(ElementwiseNode):
    signature = "in in1, in in2, in scale, in convert_policy, in round_policy, out out"
    scale = 1
    round_policy = ROUND_POLICY_TO_ZERO

    @property
    def body(self):
        if self.round_policy is ROUND_POLICY_TO_ZERO:
            return "out = in1 * in2 * %r;" % self.scale
        elif self.round_policy is ROUND_POLICY_TO_NEAREST_EVEN:
            return "out = rint(in1 * in2 * %r);" % self.scale
        else:
            raise NotImplementedError

class DivideNode(ElementwiseNode):
    signature = "in in1, in in2, in scale, in convert_policy, in round_policy, out out"
    scale = 1
    round_policy = ROUND_POLICY_TO_ZERO

    @property
    def body(self):
        if self.round_policy is ROUND_POLICY_TO_ZERO:
            return "out = (in1 * %r) / in2;" % self.scale
        elif self.round_policy is ROUND_POLICY_TO_NEAREST_EVEN:
            return "out = rint((in1 * %r) / in2);" % self.scale
        else:
            raise NotImplementedError

class TrueDivideNode(ElementwiseNode):
    signature = "in in1, in in2, out out"
    body = "out = ((double) in1) / ((double) in2);"

    def verify(self):
        self.out.suggest_color(FOURCC_F64)
        ElementwiseNode.verify(self)

class PowerNode(ElementwiseNode):
    signature = "in in1, in in2, in convert_policy, out out"
    body = "out = pow(in1, in2);"

class CompareNode(BinaryOperationNode):
    signature = "in in1, in op, in in2, out out"

    def verify(self):
        self.out.suggest_color(FOURCC_U8)
        ElementwiseNode.verify(self)

class ChannelExtractNode(Node):
    signature = "in input, in channel, out output"

    def verify(self):
        if self.channel not in self.input.color.channels:
            raise ERROR_INVALID_FORMAT(
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

class PhaseNode(ElementwiseNode):
    signature = 'in grad_x, in grad_y, out orientation'

    def verify(self):
        self.ensure(self.grad_x.color.items == 1)
        self.ensure(self.grad_y.color.items == 1)
        self.orientation.suggest_color(FOURCC_U8)
        self.orientation.ensure_similar(self.grad_x)
        self.orientation.ensure_similar(self.grad_y)

    body = "orientation = (atan2(grad_y, grad_x) + M_PI) * (255.0 / 2.0 / M_PI);"

class AccumulateImageNode(Node):
    signature = 'in input, inout accum'

    def verify(self):
        pass

mydir = os.path.dirname(os.path.abspath(__file__))

class PlayNode(Node):
    signature = 'in path, out output'
    player = None

    ffi = cffi.FFI()
    ffi.cdef("""
            struct vlcplay {
                int width, height;
                ...;
            };

            struct vlcplay *vlcplay_create(char *path);
            int vlcplay_next(struct vlcplay *m, unsigned char *buf);
            void vlcplay_release(struct vlcplay *m);
            """)
    try:
        lib = ffi.verify(open(os.path.join(mydir, 'vlcplay.c')).read(),
                         extra_compile_args=['-O3'],
                         libraries=['vlc'],
                         )
    except (cffi.VerificationError, IOError) as e:
        lib = None


    def verify(self):
        if self.lib is None:
            raise ERROR_INVALID_NODE('''
                                     
                PlayNode failed to compile. See error message from the compiler above,
                and make sure you have vlc installed. On Debian:

                    apt-get install vlc libvlc-dev

                If pyvx is installed centraly it needs to be reinstalled after the
                issue have been resolved. Using pip that is achieved with:

                    pip install --upgrade --force-reinstall pyvx

                ''')        
        if not self.player:
            self.player = self.lib.vlcplay_create(self.path)
        if not self.player:
            raise ERROR_INVALID_VALUE("Unable to decode '%s' using vlc." % self.path)
        self.output.ensure_shape(self.player.width, self.player.height)
        self.output.ensure_color(FOURCC_RGB)
        self.output.force()

    def compile(self, code):
        adr = int(self.ffi.cast('long', self.player))
        code.add_block(self, "if (vlcplay_next((void *)0x%x, img.data)) return VX_ERROR_GRAPH_ABANDONED;" % adr, img=self.output);
        code.extra_link_args.append(self.ffi.verifier.modulefilename)
        code.includes.add('#include "vlcplay.h"')


    def __del__(self):
        self.lib.vlcplay_release(self.player)

class ShowNode(Node):
    signature = "in input, in name"
    viewer = None
    name = "View"

    ffi = cffi.FFI()
    ffi.cdef("""
            struct glview {
                int width, height;
                ...;
            };
            struct glview *glview_create(int width, int height, int pixel_type, int pixel_size, char *name);
            int glview_next(struct glview *m, unsigned char *imageData);
            void glview_release(struct glview *m);

            #define GL_RGB ...
            #define GL_UNSIGNED_BYTE ...

             """)
    try:
        lib = ffi.verify(open(os.path.join(mydir, 'glview.c')).read(), 
                         extra_compile_args=['-O3'],
                         libraries=['glut', 'GL', 'GLU'])
    except (cffi.VerificationError, IOError) as e:
        print e
        lib = None

    def verify(self):
        if self.lib is None:
            raise ERROR_INVALID_NODE('''

                ShowNode failed to compile. See error message from the compiler above,
                and make sure you have glut GL and GLU installed. On Debian:

                    apt-get install freeglut3-dev

                If pyvx is installed centraly it needs to be reinstalled after the
                issue have been resolved. Using pip that is achieved with:

                    pip install --upgrade --force-reinstall pyvx

                ''')
        self.input.ensure_color(FOURCC_RGB)
        if self.viewer:
            if self.viewer.width == self.input.width and self.viewer.height == self.input.height:
                return
            self.lib.glview_release(self.viewer)
        self.viewer = self.lib.glview_create(self.input.width, 
                                             self.input.height,
                                             self.lib.GL_RGB, 
                                             self.lib.GL_UNSIGNED_BYTE, 
                                             self.name)

    def compile(self, code):
        adr = int(self.ffi.cast('long', self.viewer))
        code.add_block(self, "if (glview_next((void *)0x%x, img.data)) return VX_ERROR_GRAPH_ABANDONED;" % adr, img=self.input);
        code.extra_link_args.append(self.ffi.verifier.modulefilename)
        code.includes.add('#include "glview.h"')

    def __del__(self):
        if self.viewer:
            self.lib.glview_release(self.viewer)
