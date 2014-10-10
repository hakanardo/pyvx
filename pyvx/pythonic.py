from pyvx.types import *
import pyvx.nodes as nodes
from pyvx.backend import parse_signature


MultipleWritersError = VX_ERROR_MULTIPLE_WRITERS
InvalidGraphError = VX_ERROR_INVALID_GRAPH
InvalidValueError = VX_ERROR_INVALID_VALUE
InvalidFormatError = VX_ERROR_INVALID_FORMAT
GraphAbandonedError = VX_ERROR_GRAPH_ABANDONED

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
        func.append('    %s = nodes.Image()' % n)
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
                setattr(nodes, pname, locals()[pname])
