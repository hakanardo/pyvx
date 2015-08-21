import os, re
from cffi import FFI

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
ffi.cdef('''
    char *_get_FMT_REF(void);
    char *_get_FMT_SIZE(void);
''')

ffi.set_source("pyvx.cbackend", """
    #include <VX/vx.h>
    char *_get_FMT_REF(void) {return VX_FMT_REF;}
    char *_get_FMT_SIZE(void) {return VX_FMT_SIZE;}
               """,
               include_dirs=['include'],
               libraries=['openvx'])
ffi.compile()

from pyvx.cbackend import ffi, lib

fd = open(os.path.join('pyvx', 'vx', '_types_auto.py'), 'w')
fd.write("from pyvx.cbackend import ffi, lib\n\n")
for n in dir(lib):
    if n[:3].upper() == 'VX_':
        fd.write("%s = lib.%s\n" % (n[3:], n))
