from pyvx.backend.sample import ffi, lib
import os
import re

assert '256' == str(lib.VX_MAX_KERNEL_NAME) # Hardcoded in build_cbackend

fd = open(os.path.join('pyvx', '_auto.py'), 'w')
fd.write("class _VXAuto(object):\n")
fd.write("    def __init__(self, ffi, lib):\n")
fd.write("        self._lib = lib\n")
fd.write("        self._ffi = ffi\n")
for n in dir(lib):
    if n[:3].upper() == 'VX_':
        fd.write("        self.%s = lib.%s\n" % (n[3:], n))
fd.write("\n\n")

api = open("cdefs/vx_api.h").read() +  open("cdefs/vx_nodes.h").read()
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

    name = re.split(r'\s+', name.strip())[-1]
    assert name[:2] == 'vx'
    name = name[2:]
    args = ', '.join(a.strip(' []*') for a in args)

    method = """
    def %s(self, %s):
        '''
%s
        '''
        return self._lib.vx%s(%s)
    """ % (name, args, doc, name, args)
    fd.write(method)

