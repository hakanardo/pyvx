from pyvx.types import *
import pyvx.nodes as nodes
from pyvx.backend import *

MultipleWritersError = VX_ERROR_MULTIPLE_WRITERS
InvalidGraphError = VX_ERROR_INVALID_GRAPH
InvalidValueError = VX_ERROR_INVALID_VALUE
InvalidFormatError = VX_ERROR_INVALID_FORMAT
GraphAbandonedError = VX_ERROR_GRAPH_ABANDONED

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
