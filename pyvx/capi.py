""" 
:mod:`pyvx.capi` --- C API
==========================================

This module allows the use of this python implementation as an `OpenVX`_ backend 
from a C program. A shared library is provided that embeds python and exports a C API
following the `OpenVX`_ specification. That way the C program does not need to
be aware of the fact that python is used. Also, any C program following the
`OpenVX`_ specification should be compilable with this backend.

.. code-block:: bash

  sudo python -mpyvx.capi build /usr/local/

This will install `libopenvx.so*` into `/usr/local/lib` and place the
`OpenVX`_ headers in `/usr/local/include/VX`.

.. _`OpenVX`: https://www.khronos.org/openvx

"""

from pyvx import model, nodes
from pyvx.codegen import CApiBuilder
from pyvx.inc import vx

from pyvx import __version_info__, __version__
major, minor, _ = __version_info__
soversion = '%d.%d' % (major, minor)

builder = CApiBuilder(vx.ffi)
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

def exception_handler(e, return_type):
    import traceback
    traceback.print_exc() # xxx send to log and only for none VxError exceptions
    if return_type == vx.ffi.typeof('vx_status'):
        return model.exception2errno(e)
    return vx.ffi.NULL
builder.exception_handler = exception_handler


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
        if obj.signature:
            args = ', '.join([p.data_type.ctype for p in obj.signature])
            cdecl = 'vx_node vx%s(vx_graph, %s)' % (obj.__name__, args)
            builder.add_function(cdecl, obj)

# FIXME: Cach exeptions convert to e.errno or 0 depending on return type and log the error.

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
