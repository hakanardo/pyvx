from pyvx.types import VXTypes

class VX(VXTypes):

    def _get_attribute(self, func, ref, attribute, c_type, python_type):
        if self._ffi.typeof(c_type).kind != 'array':
            val = self._ffi.new(c_type + '*')
            status = func(ref, attribute, val, self._ffi.sizeof(c_type))
            val = val[0]
        else:
            val = self._ffi.new(c_type)
            status = func(ref, attribute, val, self._ffi.sizeof(c_type))

        if python_type is str:
            val = self._ffi.string(val)
        elif python_type is not None:
            val = python_type(val)

        return status, val

    def _set_attribute(self, func, ref, attribute, value, c_type):
        if c_type is not None:
            assert self._ffi.typeof(c_type).kind == 'primitive'
            value = self._ffi.new(c_type + '*', value)
        s = self._ffi.sizeof(self._ffi.typeof(value).item)
        return func(ref, attribute, value, s)

    # CONTEXT
    def ReleaseContext(self, context):
        c = self._ffi.new('vx_context *', context)
        return self._lib.vxReleaseContext(c)

    def GetContext(self, reference):
        return self._lib.vxGetContext(self._ffi.cast('vx_reference', reference))

    def QueryContext(self, context, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryContext, context, attribute, c_type, python_type)

    def SetContextAttribute(self, context, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetContextAttribute, context, attribute, value, c_type)

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
        return self._lib.vxCreateUniformImage(context, width, height, color, value)

    def CreateImageFromHandle(self, context, color, addrs, ptrs, import_type):
        if not isinstance(addrs, (tuple, list)):
            addrs = (addrs,)
        if not isinstance(ptrs, (tuple, list)):
            ptrs = (ptrs,)

        addrs = self._ffi.new('vx_imagepatch_addressing_t[]', [a[0] for a in addrs])
        ptrs = self._ffi.new('void *[]', [self._ffi.from_buffer(p) for p in ptrs])
        return self._lib.vxCreateImageFromHandle(context, color, addrs, ptrs, import_type)

    def QueryImage(self, image, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryImage, image, attribute, c_type, python_type)

    def SetImageAttribute(self, image, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetImageAttribute, image, attribute, value, c_type)

    def ReleaseImage(self, image):
        ref = self._ffi.new('vx_image *', image)
        return self._lib.vxReleaseImage(ref)

    def AccessImagePatch(self, image, rect, plane_index, addr, ptr, usage):
        if addr is None:
            addr = self._ffi.new('vx_imagepatch_addressing_t *')
        if ptr is not None:
            ptr = self._ffi.from_buffer(ptr)
        ptr_p = self._ffi.new('void **', ptr)
        size = self.ComputeImagePatchSize(image, rect, plane_index)
        status = self._lib.vxAccessImagePatch(image, rect, plane_index, addr, ptr_p, usage)
        return status, addr, self._ffi.buffer(ptr_p[0], size)

    def CommitImagePatch(self, image, rect, plane_index, addr, ptr):
        ptr = self._ffi.from_buffer(ptr)
        return self._lib.vxCommitImagePatch(image, rect, plane_index, addr, ptr)

    def FormatImagePatchAddress1d(self, ptr, index, addr):
        ptr = self._ffi.from_buffer(ptr)
        p = self._lib.vxFormatImagePatchAddress1d(ptr, index, addr)
        return self._ffi.buffer(p, addr.stride_x)

    def FormatImagePatchAddress2d(self, ptr, x, y, addr):
        ptr = self._ffi.from_buffer(ptr)
        p = self._lib.vxFormatImagePatchAddress2d(ptr, x, y, addr)
        return self._ffi.buffer(p, addr.stride_x)

    def GetValidRegionImage(self, image):
        rect = self.rectangle_t(0,0,0,0)
        status = self._lib.vxGetValidRegionImage(image, rect)
        return status, rect

