from weakref import WeakKeyDictionary
from pyvx.types import VXTypes

keep_alive = WeakKeyDictionary()

class VX(VXTypes):

    def __init__(self, backend):
        VXTypes.__init__(self, backend)
        self._reference_types = {self._ffi.typeof(s)
                                 for s in ['vx_context', 'vx_image', 'vx_graph', 'vx_node', 'vx_scalar',
                                           'vx_delay', 'vx_lut', 'vx_distribution', 'vx_threshold', 'vx_kernel',
                                           'vx_matrix', 'vx_convolution', 'vx_pyramid', 'vx_remap', 'vx_array',
                                           'vx_parameter']}

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
        return self._lib.vxGetContext(self._reference(reference))

    def QueryContext(self, context, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryContext, context, attribute, c_type, python_type)

    def SetContextAttribute(self, context, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetContextAttribute, context, attribute, value, c_type)

    def Hint(self, reference, hint):
        return self._lib.vxHint(self._reference(reference), hint)

    def Directive(self, reference, directive):
        return self._lib.vxDirective(self._reference(reference), directive)

    def GetStatus(self, reference):
        return self._lib.vxGetStatus(self._reference(reference))


    # IMAGE

    def ReleaseImage(self, image):
        ref = self._ffi.new('vx_image *', image)
        return self._lib.vxReleaseImage(ref)

    def QueryImage(self, image, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryImage, image, attribute, c_type, python_type)

    def SetImageAttribute(self, image, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetImageAttribute, image, attribute, value, c_type)

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


    # KERNEL

    def ReleaseKernel(self, kernel):
        ref = self._ffi.new('vx_kernel *', kernel)
        return self._lib.vxReleaseKernel(ref)

    def QueryKernel(self, kernel, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryKernel, kernel, attribute, c_type, python_type)

    def SetKernelAttribute(self, kernel, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetKernelAttribute, kernel, attribute, value, c_type)


    # GRAPH

    def ReleaseGraph(self, graph):
        ref = self._ffi.new('vx_graph *', graph)
        return self._lib.vxReleaseGraph(ref)

    def QueryGraph(self, graph, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryGraph, graph, attribute, c_type, python_type)

    def SetGraphAttribute(self, graph, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetGraphAttribute, graph, attribute, value, c_type)


    # NODE

    def ReleaseNode(self, node):
        ref = self._ffi.new('vx_node *', node)
        return self._lib.vxReleaseNode(ref)

    def QueryNode(self, node, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryNode, node, attribute, c_type, python_type)

    def SetNodeAttribute(self, node, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetNodeAttribute, node, attribute, value, c_type)

    def SetGraphParameterByIndex(self, graph, index, value):
        value = self._reference(value)
        return self._lib.vxSetGraphParameterByIndex(graph, index, value)

    def RemoveNode(self, node):
        ref = self._ffi.new('vx_node *', node)
        return self._lib.vxReleaseNode(ref)

    def AssignNodeCallback(self, node, callback):
        if callback is not None:
            callback = self._ffi.callback("vx_nodecomplete_f")(callback)
            keep_alive.setdefault(node, []).append(callback)
        else:
            callback = self._ffi.NULL
        return self._lib.vxAssignNodeCallback(node, callback)


    # PARAMETER

    def ReleaseParameter(self, parameter):
        ref = self._ffi.new('vx_parameter *', parameter)
        return self._lib.vxReleaseParameter(ref)

    def QueryParameter(self, parameter, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryParameter, parameter, attribute, c_type, python_type)

    def SetParameterByIndex(self, node, index, value):
        value = self._reference(value)
        return self._lib.vxSetParameterByIndex(node, index, value)

    def SetParameterByReference(self, parameter, value):
        value = self._reference(value)
        return self._lib.vxSetParameterByReference(parameter, value)


    # SCALAR

    def _new_scalar_value_ptr(self, data_type, value=None):
        data_type_name = self._ffi.string(self._ffi.cast("enum vx_type_e", data_type))
        assert data_type_name.startswith('VX_TYPE_')
        return self._ffi.new('vx_%s *' % data_type_name[8:].lower(), value)

    def CreateScalar(self, context, data_type, value):
        ptr = self._new_scalar_value_ptr(data_type, value)
        return self._lib.vxCreateScalar(context, data_type, ptr)

    def ReleaseScalar(self, scalar):
        ref = self._ffi.new('vx_scalar *', scalar)
        return self._lib.vxReleaseScalar(ref)

    def QueryScalar(self, scalar, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryScalar, scalar, attribute, c_type, python_type)

    def ReadScalarValue(self, scalar):
        s, data_type = self.QueryScalar(scalar, self.SCALAR_ATTRIBUTE_TYPE, "vx_enum")
        ptr = self._new_scalar_value_ptr(data_type)
        s = self._lib.vxReadScalarValue(scalar, ptr)
        return s, ptr[0]

    def WriteScalarValue(self, scalar, value):
        s, data_type = self.QueryScalar(scalar, self.SCALAR_ATTRIBUTE_TYPE, "vx_enum")
        ptr = self._new_scalar_value_ptr(data_type, value)
        return self._lib.vxWriteScalarValue(scalar, ptr)


    # REFERENCE

    def _reference(self, reference):
        if self._ffi.typeof(reference) not in self._reference_types:
            raise TypeError("Can't cast %r to vx_reference" % reference)
        return self._ffi.cast('vx_reference', reference)

    def QueryReference(self, reference, attribute, c_type, python_type=None):
        reference = self._reference(reference)
        return self._get_attribute(self._lib.vxQueryReference, reference, attribute, c_type, python_type)

