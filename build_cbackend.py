import os
from cffi import FFI

openvx_install = '/usr/local/src/openvx_sample/install/Linux/x64/Release/'


ffi = FFI()
ffi.cdef(open("cdefs/vx_vendors.h").read())
ffi.cdef(open("cdefs/vx_types.h").read())

ffi.set_source("pyvx.cbackend", "#include <VX/vx.h>",
               include_dirs=[os.path.join(openvx_install,'include')],
               library_dirs=[os.path.join(openvx_install,'bin')],
               extra_link_args=['-Wl,-rpath='+os.path.join(openvx_install,'bin')],
               libraries=['openvx'])
ffi.compile()

from pyvx.cbackend import ffi, lib
print dir(lib)

print lib.VX_ID_QUALCOMM.__class__