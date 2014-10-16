"""
:mod:`pyvx.pythonic` --- Python friendly API
============================================

Here a transformed OpenVX API is provided that is intended to feel more
natural to a python programmer. The above example would with this API look
like this:

.. code-block:: python 

    from pyvx import *

    with Graph() as g:
        img = Image(640, 480, FOURCC_UYVY)
        smooth = Gaussian3x3(img.channel_y)
        dx, dy = Sobel3x3(smooth)
        mag = Magnitude(dx, dy)
        phi = Phase(dx, dy)
        mag.force()
        phi.force()
    g.verify()
    g.process()

This API is generated from the OpenVX API using the following transformations:

- The error codes ``VX_ERROR_XXX_YYY`` are turned into exceptions ``XxxYyyError`` and
  raised instead of returned.

- Graph's are created using

    .. code-block:: python 

        class Graph(context=None, early_verify=True):

  If ``context`` is not specified a single global context will be created an
  used. If ``early_verify`` is ``True`` a partial verification will be performed as
  the nodes are created. This allows most errors to be detected at this time
  and raised as exceptions. The tracebacks of those exceptions will point to
  the line producing the erroneous node. This simplifies debugging a lot.

  The ``Graph`` objects are context manager that support the ``with`` statement as
  shown in the example above. It is used to make all the nodes and virtual
  images produced from within the code block belong to that graph. This allows
  virtual images to be automatically created and the use of special methods to
  create binary operations (see below).

- Within the code block of a ``with Graph():`` construction, the following features
  can be used:

    - For each ``vxXxxNode`` there is a ``Xxx()`` function that has only the input arguments
      of ``vxXxxNode``. This function will create a 0x0 virtual image with color
      ``FOURCC_VIRT`` for each of the output and inout arguments. Then it will call 
      ``vxXxxNode`` and return the created images. Also, most non-image input arguments 
      have been given default values and can be skipped.

    - The ``Image`` objects have ``width``, ``height`` and ``color`` properties than
      can be adjusted at any time before the verification 
      phase. However, to get the most out of the early verification described above,
      it is recommended to make any such adjustments as soon as possible.

    - ``Image`` objects have a ``force()`` method that will turn a virtual image into a
      normal fully allocated non-virtual image.

    - ``Image`` objects that have been passed as an output or inout parameter of a node 
      have a ``producer`` property that refers to this node. It can be used to access
      a node object even if only it's outputs are available (which would be the
      typical case when using this API).

    - For each ``VX_CHANNEL_X`` the ``Image`` object has a ``channel_x`` property 
      that will 
      create a ``ChannelExtractNode`` and return it's virtual output images.

    - A lot of the python special methods are Implemented on the ``Image`` objects to
      allow numpy style expressions to be used to create nodes.

    As an example here is a graph that calculates the squared magnitude in a 32 bit 
    unsigned image:

    .. code-block:: python 

        from pyvx import *

        with Graph() as g:
            img = Image(640, 480, FOURCC_UYVY)
            dx, dy = Sobel3x3(img.channel_y)
            mag = dx*dx + dy*dy
            mag.color = FOURCC_U32
            mag.force()
        g.verify()
        g.process()


"""

from pyvx.types import *
import pyvx.nodes as nodes
from pyvx.backend import *

MultipleWritersError = ERROR_MULTIPLE_WRITERS
InvalidGraphError = ERROR_INVALID_GRAPH
InvalidValueError = ERROR_INVALID_VALUE
InvalidFormatError = ERROR_INVALID_FORMAT
GraphAbandonedError = ERROR_GRAPH_ABANDONED
InvalidNodeError = ERROR_INVALID_NODE

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
        return BinaryOperation(self, '+', self.make_similar_image(other))

    def __sub__(self, other):
        return BinaryOperation(self, '-', self.make_similar_image(other))

    def __mul__(self, other):
        return Multiply(self, self.make_similar_image(other))

    def __div__(self, other):
        return Divide(self, self.make_similar_image(other))

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return BinaryOperation(self.make_similar_image(other), '-', self)

    def __rdiv__(self, other):
        return Divide(self.make_similar_image(other), self)

    __floordiv__ = __div__
    __rfloordiv__ = __rdiv__

    def __pow__(self, other):
        return Power(self, self.make_similar_image(other))

    def __rpow__(self, other):
        return Power(self.make_similar_image(other), self)

    def __mod__(self, other):
        return BinaryOperation(self, '%', self.make_similar_image(other))

    def __rmod__(self, other):
        return BinaryOperation(self.make_similar_image(other), '%', self)

    def __truediv__(self, other):
        res = TrueDivide(self, self.make_similar_image(other))
        return res

    def __rtruediv__(self, other):
        res = TrueDivide(self.make_similar_image(other), self)
        return res

    def __lshift__(self, other):
        return BinaryOperation(self, "<<", self.make_similar_image(other))

    def __rlshift__(self, other):
        return BinaryOperation(self.make_similar_image(other), "<<", self)

    def __rshift__(self, other):
        return BinaryOperation(self, ">>", self.make_similar_image(other))

    def __rrshift__(self, other):
        return BinaryOperation(self.make_similar_image(other), ">>", self)

    def __and__(self, other):
        return BinaryOperation(self, "&", self.make_similar_image(other))

    def __rand__(self, other):
        return BinaryOperation(self.make_similar_image(other), "&", self)

    def __or__(self, other):
        return BinaryOperation(self, "|", self.make_similar_image(other))

    def __ror__(self, other):
        return BinaryOperation(self.make_similar_image(other), "|", self)

    def __xor__(self, other):
        return BinaryOperation(self, "^", self.make_similar_image(other))

    def __xror__(self, other):
        return XBinaryOperationor(self.make_similar_image(other), "^", self)

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


def _get_default_repr(cls, name):
    item = getattr(cls, name)
    if hasattr(item, '__name__'):
        return item.__name__
    return repr(item)

def _make_pythonic_node(pname, cls):
    sig = parse_signature(cls.signature)
    outputs = [n for d, n in sig if d in ('out', 'inout')]
    inputs = [n for d, n in sig  if d=='in']
    allputs = [n for d, n in sig]
    args = [n + '=' + _get_default_repr(cls, n) if hasattr(cls, n) else n 
            for n in inputs]

    func = ['def ' + pname + '(' + ', '.join(args) + '):']
    for n in outputs:
        func.append('    %s = Image()' % n)
    func.append('    nodes.' + pname + 'Node' + '(nodes.CoreGraph.get_current_graph(), ' + ', '.join(allputs) + ')')
    func.append('    return ' + ', '.join(outputs))
    return '\n'.join(func)

for n in dir(nodes):
    item = getattr(nodes, n)
    if isinstance(item, type) and issubclass(item, nodes.Node):
        if len(n) > 4 and n[-4:] == 'Node':
            pname = n[:-4]
            if pname not in locals() and hasattr(item, 'signature'):
                exec _make_pythonic_node(pname, item)
