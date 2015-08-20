import os, re
from cffi import FFI

openvx_install = '/usr/local/src/openvx_sample/install/Linux/x64/Release/'

defs= dict(VX_API_ENTRY='', VX_API_CALL='', VX_CALLBACK='')
if os.name == 'nt':
    defs['VX_API_CALL'] = '__stdcall'
    defs['VX_CALLBACK'] = '__stdcall'

ffi = FFI()
vx = open("cdefs/vx.h").read()
vx = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', vx)[0] # Remove specifics from #defines
ffi.cdef(vx)

ffi.cdef(open("cdefs/vx_vendors.h").read())

types = open("cdefs/vx_types.h").read()

for k,v in defs.items():
    types = types.replace(k, v)

types = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', types)[0] # Remove specifics from #defines
types = re.subn(r'(\/\*.*?\*\/)', r'', types)[0] # Remove some one line comments
types = re.subn(r'=.*,', r'= ...,', types)[0] # Remove specifics from enums
types = re.subn(r'\[\s*[^\s]+?.*?\]', r'[...]', types)[0] # Remove specific array sizes

ffi.cdef(types)

ffi.set_source("pyvx.cbackend", "#include <VX/vx.h>",
               include_dirs=[os.path.join(openvx_install,'include')],
               library_dirs=[os.path.join(openvx_install,'bin')],
               extra_link_args=['-Wl,-rpath='+os.path.join(openvx_install,'bin')],
               libraries=['openvx'])
ffi.compile()

from pyvx.cbackend import ffi, lib

fd = open(os.path.join('pyvx', 'vx', '_types_auto.py'), 'w')
fd.write("from pyvx.cbackend import ffi, lib\n\n")
for n in dir(lib):
    assert n[:3].upper() == 'VX_'
    fd.write("%s = lib.%s\n" % (n[3:], n))

print lib.VX_ID_QUALCOMM.__class__
print ffi.new("vx_perf_t *")