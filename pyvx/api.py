from pyvx.types import VXTypes

class VX(VXTypes):

    # CONTEXT
    def ReleaseContext(self, context):
        c = self._ffi.new('vx_context *', context)
        return self._lib.vxReleaseContext(c)

    def GetContext(self, reference):
        return self._lib.vxGetContext(self._ffi.cast('vx_reference', reference))

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

    def SetContextAttribute(self, context, attribute, value, c_type=None):
        if c_type is not None:
            assert self._ffi.typeof(c_type).kind == 'primitive'
            value = self._ffi.new(c_type + '*', value)
        s = self._ffi.sizeof(self._ffi.typeof(value).item)
        return self._lib.vxSetContextAttribute(context, attribute, value, s)

    def Hint(self, reference, hint):
        return self._lib.vxHint(self._ffi.cast('vx_reference', reference), hint)

    def Directive(self, reference, directive):
        return self._lib.vxDirective(self._ffi.cast('vx_reference', reference), directive)

    def GetStatus(self, reference):
        return self._lib.vxGetStatus(self._ffi.cast('vx_reference', reference))

    # IMAGE

    def CreateUniformImage(self, context, width, height, color, value, c_type):
        if self._ffi.typeof(c_type).kind != 'array':
            c_type += '*'
        value = self._ffi.new(c_type, value)
        self._lib.vxCreateUniformImage(context, width, height, color, value)

    def CreateImageFromHandle(self, context, color, addrs, ptrs, import_type):
        if not isinstance(addrs, (tuple, list)):
            addrs = (addrs,)
        if not isinstance(ptrs, (tuple, list)):
            ptrs = (ptrs,)

        addrs = self._ffi.new('vx_imagepatch_addressing_t[]', [a[0] for a in addrs])
        ptrs = self._ffi.new('void *[]', [self._ffi.from_buffer(p) for p in ptrs])
        return self._lib.vxCreateImageFromHandle(context, color, addrs, ptrs, import_type)

