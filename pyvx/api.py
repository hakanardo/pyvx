from pyvx.types import VXTypes

class VX(VXTypes):
    def ReleaseContext(self, context):
        c = self._ffi.new('vx_context *', context)
        return self._lib.vxReleaseContext(c)

    def QueryContext(self, context, attribute, c_type, python_type=None):
        if self._ffi.typeof(c_type).kind != 'array':
            val = self._ffi.new(c_type + '*')
            status = self._lib.vxQueryContext(context, attribute, val, self._ffi.sizeof(c_type))
            val = val[0]
        else:
            val = self._ffi.new(c_type)
            status = self._lib.vxQueryContext(context, attribute, val, self._ffi.sizeof(c_type))

        if python_type is str:
            val = self._ffi.string(val)
        elif python_type is not None:
            val = python_type(val)

        return status, val