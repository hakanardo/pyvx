import os
from cffi import FFI
ffi = FFI()

ffi.cdef('''
#define VX_MAX_IMPLEMENTATION_NAME ...
#define VX_MAX_KERNEL_NAME ...
#define VX_MAX_LOG_MESSAGE_LEN ...
#define VX_VERSION_1_0 ...
#define VX_VERSION ...
''')

mydir = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(mydir, '..', '..', 'headers')
lib = ffi.verify('#include "VX/vx.h"', extra_compile_args=["-I" + d])
vars = locals()
for n in dir(lib):
    vars[n] = getattr(lib, n)
