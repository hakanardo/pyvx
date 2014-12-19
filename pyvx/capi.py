from pyvx import model, nodes
from pyvx.codegen import CApiBuilder
from pyvx.inc import vx

from pyvx import __version_info__, __version__
major, minor, _ = __version_info__
soversion = '%d.%d' % (major, minor)

builder = CApiBuilder(vx.ffi)
builder.set_exception_return_value('vx_status', vx.FAILURE)
builder.setup = """
import sys
sys.path = ['.'] + sys.path
import pyvx
if pyvx.__version__ != %r: 
    print 'Version mismatch. Please reinstall pyvx and/or recompile your binary. Exiting...'
    exit()
from pyvx.capi import builder
builder.load()
""" % __version__
builder.includes.add('#include <VX/vx.h>')

for n in dir(model):
    obj = getattr(model, n)
    if isinstance(obj, type) and issubclass(obj, model.VxObject) and hasattr(obj, 'type'):
        builder.add_wrapped_reference_type(obj.type.ctype)
    if hasattr(obj, 'capis'):
        for api in obj.capis:
            builder.add_function(api.cdecl, obj)

for n in dir(nodes):
    obj = getattr(nodes, n)
    if isinstance(obj, type) and issubclass(obj, model.Node):
        if hasattr(obj, 'signature'):
            args = ', '.join([a[1].ctype for a in nodes.parse_signature(obj.signature)])
            cdecl = 'vx_node vx%s(vx_graph, %s)' % (obj.__name__, args)
            builder.add_function(cdecl, obj)



def build(prefix='/usr/local'):
    from pyvx.inc.vx import ffi
    import os
    from distutils.dir_util import copy_tree

    libdir = os.path.join(prefix, 'lib')
    incdir = os.path.join(prefix, 'include', 'VX')
    if not os.path.exists(libdir):
        os.makedirs(libdir)
    if not os.path.exists(incdir):
        os.makedirs(incdir)

    builder.build('openvx', __version__, soversion, libdir)
    srcdir = os.path.join(os.path.dirname(__file__), 'inc', 'headers', 'VX')
    copy_tree(srcdir, incdir)
    os.system('ldconfig')

    return builder.library_names

if __name__ == '__main__':
    import sys
    if len(sys.argv) in (2,3) and sys.argv[1] == 'build':
        build(*sys.argv[2:])
    else:
        print 'Usage: %s build [<prefix>]' % sys.argv[0]
