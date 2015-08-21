import os, re
from cffi import FFI

name = 'sample'
openvx_install = '/usr/local/src/openvx_sample/install/Linux/x64/Release/'
#-               include_dirs=[os.path.join(openvx_install,'include')],
#-               library_dirs=[os.path.join(openvx_install,'bin')],
#-               extra_link_args=['-Wl,-rpath='+os.path.join(openvx_install,'bin')],


defs= dict(VX_API_ENTRY='', VX_API_CALL='', VX_CALLBACK='', VX_MAX_KERNEL_NAME='256')
if os.name == 'nt':
    defs['VX_API_CALL'] = '__stdcall'
    defs['VX_CALLBACK'] = '__stdcall'

ffi = FFI()

# vx.h
vx = open("cdefs/vx.h").read()
vx = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', vx)[0] # Remove specifics from #defines
ffi.cdef(vx)

# vx_vendors.h
ffi.cdef(open("cdefs/vx_vendors.h").read())

# vx_types.h
types = open("cdefs/vx_types.h").read()

for k,v in defs.items():
    types = types.replace(k, v)

types = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', types)[0] # Remove specifics from #defines
types = re.subn(r'(\/\*.*?\*\/)', r'', types)[0] # Remove some one line comments
types = re.subn(r'=.*,', r'= ...,', types)[0] # Remove specifics from enums
types = re.subn(r'\[\s*[^\s]+?.*?\]', r'[...]', types)[0] # Remove specific array sizes

ffi.cdef(types)
ffi.cdef('''
    char *_get_FMT_REF(void);
    char *_get_FMT_SIZE(void);
''')

# vx_kernels.h
kernels = open("cdefs/vx_kernels.h").read()
kernels = re.subn(r'=.*,', r'= ...,', kernels)[0] # Remove specifics from enums
ffi.cdef(kernels)

# vx_api.h
api = open("cdefs/vx_api.h").read()
for k, v in defs.items():
    api = api.replace(k, v)
ffi.cdef(api)

ffi.set_source("pyvx.backend.%s" % name, """
    #include <VX/vx.h>
    char *_get_FMT_REF(void) {return VX_FMT_REF;}
    char *_get_FMT_SIZE(void) {return VX_FMT_SIZE;}
               """,
               include_dirs=[os.path.join(openvx_install, 'include')],
               library_dirs=[os.path.join(openvx_install, 'bin')],
               extra_link_args=['-Wl,-rpath='+os.path.join(openvx_install, 'bin')],
               libraries=['openvx'])
ffi.compile()

from pyvx._cbackend_types import ffi, lib
assert defs["VX_MAX_KERNEL_NAME"] == str(lib.VX_MAX_KERNEL_NAME)

fd = open(os.path.join('pyvx', '_auto.py'), 'w')
fd.write("class _VXAuto(object):\n")
fd.write("    def __init__(self, ffi, lib):\n")
for n in dir(lib):
    if n[:3].upper() == 'VX_':
        fd.write("        self.%s = lib.%s\n" % (n[3:], n))

