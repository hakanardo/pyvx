from pyvx.backend.sample import ffi, lib
import os
assert '256' == str(lib.VX_MAX_KERNEL_NAME) # Hardcoded in build_cbackend

fd = open(os.path.join('pyvx', '_auto.py'), 'w')
fd.write("class _VXAuto(object):\n")
fd.write("    def __init__(self, ffi, lib):\n")
for n in dir(lib):
    if n[:3].upper() == 'VX_':
        fd.write("        self.%s = lib.%s\n" % (n[3:], n))
