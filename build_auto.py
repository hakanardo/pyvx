from pyvx.backend.sample import ffi, lib
import os
import re

assert '256' == str(lib.VX_MAX_KERNEL_NAME) # Hardcoded in build_cbackend

fd = open(os.path.join('pyvx', '_auto.py'), 'w')
fd.write("class _VXAuto(object):\n")
fd.write("    def __init__(self, backend):\n")
fd.write("        self._lib = lib = backend.lib\n")
fd.write("        self._ffi = ffi = backend.ffi\n")
for n in dir(lib):
    if n[:3].upper() == 'VX_':
        fd.write("        self.%s = lib.%s\n" % (n[3:], n))
fd.write("\n\n")

api = open("pyvx/cdefs/vx_api.h").read() + open("pyvx/cdefs/vx_nodes.h").read() + open("pyvx/cdefs/vxu.h").read()
vxu_methods = ''
for entry in api.split('/*!'):
    if 'VX_API_ENTRY' not in entry:
        continue
    doc, entry = entry.split('VX_API_ENTRY')
    i = entry.find(';')
    entry = entry[:i].strip()
    name, args = entry.split('(')
    assert args[-1] == ')'
    args = args[:-1]
    args = args.replace('[VX_MAX_KERNEL_NAME]', '[]')
    args = [re.split(r'\s+', a.strip())[-1] for a in args.split(',')]
    if args[-1] == '...':
        args.pop()
    doc = re.sub(r' \*[ \/]?', '', doc)
    doc = re.subn(r'\\ref\s+', '', doc)[0]
    doc = re.subn(r'\\([a-z]+)', r':\1:', doc)[0]
    doc = re.subn(r'<\/?tt>', r'*', doc)[0]
    doc = doc.strip()

    fullname = re.split(r'\s+', name.strip())[-1]
    assert fullname[:2] == 'vx'
    args = ', '.join(a.strip(' []*') for a in args)

    if fullname[:3] == 'vxu':
        name = fullname[3:]
    else:
        name = fullname[2:]

    method = """
    def %s(self, %s):
        '''
%s
        '''
        return self._lib.%s(%s)
    """ % (name, args, doc, fullname, args)
    if fullname[:3] == 'vxu':
        vxu_methods += method
    else:
        fd.write(method)

fd.write("\n\nclass _VXUAuto(object):\n")
fd.write("    def __init__(self, backend):\n")
fd.write("        self._lib = backend.lib\n")
fd.write("        self._ffi = backend.ffi\n")
fd.write(vxu_methods)


