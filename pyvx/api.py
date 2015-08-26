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
                                           'vx_parameter', 'vx_reference']}

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

    def _enum2ctype(self, data_type):
        data_type_name = self._ffi.string(self._ffi.cast("enum vx_type_e", data_type))
        assert data_type_name.startswith('VX_TYPE_')
        return 'vx_' + data_type_name[8:].lower()

    def _callback(self, ctype, callback, parent):
        callback = self._ffi.callback(ctype)(callback)
        keep_alive.setdefault(parent, []).append(callback)
        return callback

    # CONTEXT
    def ReleaseContext(self, context):
        c = self._ffi.new('vx_context *', context)
        return self._lib.vxReleaseContext(c)

    def QueryContext(self, context, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryContext, context, attribute, c_type, python_type)

    def SetContextAttribute(self, context, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetContextAttribute, context, attribute, value, c_type)


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

    def RemoveNode(self, node):
        ref = self._ffi.new('vx_node *', node)
        return self._lib.vxReleaseNode(ref)

    def AssignNodeCallback(self, node, callback):
        if callback is not None:
            callback = self._callback("vx_nodecomplete_f", callback, node)
        else:
            callback = self._ffi.NULL
        return self._lib.vxAssignNodeCallback(node, callback)


    # PARAMETER

    def ReleaseParameter(self, parameter):
        ref = self._ffi.new('vx_parameter *', parameter)
        return self._lib.vxReleaseParameter(ref)

    def QueryParameter(self, parameter, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryParameter, parameter, attribute, c_type, python_type)


    # SCALAR

    def CreateScalar(self, context, data_type, value):
        ptr = self._ffi.new(self._enum2ctype(data_type) + '*', value)
        return self._lib.vxCreateScalar(context, data_type, ptr)

    def ReleaseScalar(self, scalar):
        ref = self._ffi.new('vx_scalar *', scalar)
        return self._lib.vxReleaseScalar(ref)

    def QueryScalar(self, scalar, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryScalar, scalar, attribute, c_type, python_type)

    def ReadScalarValue(self, scalar):
        s, data_type = self.QueryScalar(scalar, self.SCALAR_ATTRIBUTE_TYPE, "vx_enum")
        ptr = self._ffi.new(self._enum2ctype(data_type) + '*')
        s = self._lib.vxReadScalarValue(scalar, ptr)
        return s, ptr[0]

    def WriteScalarValue(self, scalar, value):
        s, data_type = self.QueryScalar(scalar, self.SCALAR_ATTRIBUTE_TYPE, "vx_enum")
        ptr = self._ffi.new(self._enum2ctype(data_type) + '*', value)
        return self._lib.vxWriteScalarValue(scalar, ptr)


    # REFERENCE

    def reference(self, reference):
        if self._ffi.typeof(reference) not in self._reference_types:
            raise TypeError("Can't cast %r to vx_reference" % reference)
        return self._ffi.cast('vx_reference', reference)

    def from_reference(self, ref):
        s, data_type = self.QueryReference(ref, self.REF_ATTRIBUTE_TYPE, 'vx_enum')
        return self._ffi.cast(self._enum2ctype(data_type), ref)

    def QueryReference(self, reference, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryReference, reference, attribute, c_type, python_type)


    # DELAY

    def ReleaseDelay(self, delay):
        ref = self._ffi.new('vx_delay *', delay)
        return self._lib.vxReleaseDelay(ref)

    def QueryDelay(self, delay, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryDelay, delay, attribute, c_type, python_type)


    # LOGGING

    def RegisterLogCallback(self, context, callback, reentrant):
        def wrapper(context, ref, status, string):
            callback(context, ref, status, self._ffi.string(string))
        cb = self._callback('vx_log_callback_f', wrapper, context)
        self._lib.vxRegisterLogCallback(context, cb, reentrant)


    # LUT

    def ReleaseLUT(self, lut):
        ref = self._ffi.new('vx_lut *', lut)
        return self._lib.vxReleaseLUT(ref)

    def QueryLUT(self, lut, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryLUT, lut, attribute, c_type, python_type)

    def AccessLUT(self, lut, ptr, usage):
        if ptr is not None:
            ptr = self._ffi.from_buffer(ptr)
        ptr_p = self._ffi.new('void **', ptr)
        status = self._lib.vxAccessLUT(lut, ptr_p, usage)
        _, size = self.QueryLUT(lut, self.LUT_ATTRIBUTE_COUNT, 'vx_size')
        return (status, self._ffi.buffer(ptr_p[0], size))

    def CommitLUT(self, lut, ptr):
        ptr = self._ffi.from_buffer(ptr)
        return self._lib.vxCommitLUT(lut, ptr)


    # DISTRIBUTION

    def ReleaseDistribution(self, distribution):
        ref = self._ffi.new('vx_distribution *', distribution)
        return self._lib.vxReleaseDistribution(ref)

    def QueryDistribution(self, distribution, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryDistribution, distribution, attribute, c_type, python_type)

    def AccessDistribution(self, distribution, ptr, usage):
        if ptr is not None:
            ptr = self._ffi.from_buffer(ptr)
        ptr_p = self._ffi.new('void **', ptr)
        status = self._lib.vxAccessDistribution(distribution, ptr_p, usage)
        _, size = self.QueryDistribution(distribution, self.DISTRIBUTION_ATTRIBUTE_SIZE, 'vx_size')
        return (status, self._ffi.buffer(ptr_p[0], size))

    def CommitDistribution(self, distribution, ptr):
        ptr = self._ffi.from_buffer(ptr)
        return self._lib.vxCommitDistribution(distribution, ptr)


    # THRESHOLD

    def ReleaseThreshold(self, threshold):
        ref = self._ffi.new('vx_threshold *', threshold)
        return self._lib.vxReleaseThreshold(ref)

    def QueryThreshold(self, threshold, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryThreshold, threshold, attribute, c_type, python_type)

    def SetThresholdAttribute(self, threshold, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetThresholdAttribute, threshold, attribute, value, c_type)


    # MATRIX

    def ReleaseMatrix(self, matrix):
        ref = self._ffi.new('vx_matrix *', matrix)
        return self._lib.vxReleaseMatrix(ref)

    def QueryMatrix(self, matrix, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryMatrix, matrix, attribute, c_type, python_type)

    def ReadMatrix(self, mat, array):
        array = self._ffi.from_buffer(array)
        return self._lib.vxReadMatrix(mat, array)

    def WriteMatrix(self, mat, array):
        array = self._ffi.from_buffer(array)
        return self._lib.vxWriteMatrix(mat, array)


    # CONVOLUTION

    def ReleaseConvolution(self, convolution):
        ref = self._ffi.new('vx_convolution *', convolution)
        return self._lib.vxReleaseConvolution(ref)

    def QueryConvolution(self, convolution, attribute, c_type, python_type=None):
        return self._get_attribute(self._lib.vxQueryConvolution, convolution, attribute, c_type, python_type)

    def SetConvolutionAttribute(self, convolution, attribute, value, c_type=None):
        return self._set_attribute(self._lib.vxSetConvolutionAttribute, convolution, attribute, value, c_type)

    def WriteConvolutionCoefficients(self, conv, array):
        array = self._ffi.from_buffer(array)
        return self._lib.vxWriteConvolutionCoefficients(conv, array)

    def ReadConvolutionCoefficients(self, conv, array):
        array = self._ffi.from_buffer(array)
        return self._lib.vxReadConvolutionCoefficients(conv, array)
