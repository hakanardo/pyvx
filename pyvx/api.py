from pyvx.types import VXTypes

class VX(VXTypes):
    def ReleaseContext(self, context):
        c = self._ffi.new('vx_context *', context)
        return self._lib.vxReleaseContext(c)
