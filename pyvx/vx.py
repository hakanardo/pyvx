"""
:mod:`pyvx.vx` --- C-like Python API
==========================================

The functions specified by the `OpenVX`_ standard are provided in form of two
modules,  :mod:`pyvx.vx` that provide the vxXxxfunctions and :class:`pyvx.vxu`
that provide the vxuXxx functions. Pleaserefer to the `OpenVX speficication`_
for a description of the API. The modulenames vx and vxu is used instead of a
vx/vxu prefix on all symbols. The initialexample on page 12 of the
specification would in python look like this:

.. code-block:: python

    from pyvx import vx

    context = vx.CreateContext()
    images = [
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_UYVY),
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_S16),
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_U8),
    ]
    graph = vx.CreateGraph(context)
    virts = [
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
    ]
    vx.ChannelExtractNode(graph, images[0], vx.CHANNEL_Y, virts[0])
    vx.Gaussian3x3Node(graph, virts[0], virts[1])
    vx.Sobel3x3Node(graph, virts[1], virts[2], virts[3])
    vx.MagnitudeNode(graph, virts[2], virts[3], images[1])
    vx.PhaseNode(graph, virts[2], virts[3], images[2])
    status = vx.VerifyGraph(graph)
    print status
    if status == vx.SUCCESS:
        status = vx.ProcessGraph(graph)
    else:
        print("Verification failed.")
    vx.ReleaseContext(context)

For a compact example on how to call all the functions in the API check
out `test_vx.py`_.

.. _`OpenVX`: https://www.khronos.org/openvx
.. _`OpenVX speficication`: https://www.khronos.org/registry/vx/specs/OpenVX_1.0_Provisional_Specifications.zip
.. _`test_vx.py`: https://github.com/hakanardo/pyvx/tree/master/test/test_vx.py

The API is kept as
close as possible to the C API, but the few changes listed below were
made. Mostly due to the usage of pointers in C.

    * The vx prefix is removed for each function name. The module name
      forms a similar role in python.

    * The *ReleaseXxx* and *RemoveNode* functions take a normal object (as
      returned by the
      corresponding CreateXxx) as argument and not a pointer to a pointer.

    * Out arguments passed in as pointers are returned instead. The
      returned tuple will contain the original return value as it's
      first value and following it, the output arguments in the same
      order as they apear in the C signature.

    * In/Out arguemnts are passed in as values and then returned in the
      same manner as the out arguments.

    * Any python object implementing the buffer interface can be passed
      instead of pointers to blocks of data. This includes both
      *array.array* and *numpy.ndarray* objects.

    * Python buffer objects are returned instead of pointers to blocks
      of data.

    * *QueryXxx* functions have the signature
        .. code-block:: python

            (status, value) = vx.QueryXxx(context, attribute, c_type, python_type=None)

      where *c_type* is a string specifying the type of the attribute,
      for example "vx_uint32", and *python_type* can be set to *str* for
      string-valued attributes.

    * *SetXxxAttribute* functions have the signature
        .. code-block:: python

            status = vx.SetXxxAttribute(context, attribute, value, c_type=None)

      where *c_type* is a string specifying the type of the attribute,
      for example "vx_uint32".

    * *CreateUniformImage* have the signature
        .. code-block:: python

            image = vx.CreateUniformImage(context, width, height, color, value, c_type)

        where value is a python *int* and *c_type* a string specifying
        it's type. For example "vx_uint32".

    * Normal python functions can be used instead of function pointers.

    * *LoadKernels* can load python modules if it is passed a string that
      is the name of an importable python module. In that case it will
      import *PublishKernels* from it and call
      *PublishKernels(context)*.

    * *CreateScalar* and *WriteScalarValue* take a python int as value.

    * Objects are not implicitly casted to/from references. Use
      :func:`pyvx.vx.reference` and :func:`pyvx.vx.from_reference` instead.

    * The typedefed structures called vx_xxx_t can be allocated using
      vx.xxx_t(...). See below.

"""

from weakref import WeakKeyDictionary
import sys

from pyvx.types import *

keep_alive = WeakKeyDictionary()

_reference_types = {ffi.typeof(s)
                    for s in ['vx_context', 'vx_image', 'vx_graph', 'vx_node', 'vx_scalar',
                              'vx_delay', 'vx_lut', 'vx_distribution', 'vx_threshold', 'vx_kernel',
                              'vx_matrix', 'vx_convolution', 'vx_pyramid', 'vx_remap', 'vx_array',
                              'vx_parameter', 'vx_reference']}

def _get_attribute(func, ref, attribute, c_type, python_type):
    if ffi.typeof(c_type).kind != 'array':
        val = ffi.new(c_type + '*')
        status = func(ref, attribute, val, ffi.sizeof(c_type))
        val = val[0]
    else:
        val = ffi.new(c_type)
        status = func(ref, attribute, val, ffi.sizeof(c_type))

    if python_type is str:
        val = ffi.string(val).decode("utf8")
    elif python_type is not None:
        val = python_type(val)

    return status, val

def _set_attribute(func, ref, attribute, value, c_type):
    if c_type is not None:
        assert ffi.typeof(c_type).kind == 'primitive'
        value = ffi.new(c_type + '*', value)
    s = ffi.sizeof(ffi.typeof(value).item)
    return func(ref, attribute, value, s)

def _enum2ctype(data_type):
    data_type_name = ffi.string(ffi.cast("enum vx_type_e", data_type))
    assert data_type_name.startswith('VX_TYPE_')
    return 'vx_' + data_type_name[8:].lower()

def _callback(ctype, callback, parent, error):
    callback = ffi.callback(ctype, error=error)(callback)
    keep_alive.setdefault(parent, []).append(callback)
    return callback

# CONTEXT
def ReleaseContext(context):
    c = ffi.new('vx_context *', context)
    return lib.vxReleaseContext(c)

def QueryContext(context, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryContext, context, attribute, c_type, python_type)

def SetContextAttribute(context, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetContextAttribute, context, attribute, value, c_type)


# IMAGE

def ReleaseImage(image):
    ref = ffi.new('vx_image *', image)
    return lib.vxReleaseImage(ref)

def QueryImage(image, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryImage, image, attribute, c_type, python_type)

def SetImageAttribute(image, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetImageAttribute, image, attribute, value, c_type)

def CreateUniformImage(context, width, height, color, value, c_type):
    if ffi.typeof(c_type).kind != 'array':
        c_type += '*'
    value = ffi.new(c_type, value)
    return lib.vxCreateUniformImage(context, width, height, color, value)

def CreateImageFromHandle(context, color, addrs, ptrs, import_type):
    if not isinstance(addrs, (tuple, list)):
        addrs = (addrs,)
    if not isinstance(ptrs, (tuple, list)):
        ptrs = (ptrs,)

    addrs = ffi.new('vx_imagepatch_addressing_t[]', [a[0] for a in addrs])
    ptrs = ffi.new('void *[]', [ffi.from_buffer(p) for p in ptrs])
    return lib.vxCreateImageFromHandle(context, color, addrs, ptrs, import_type)

def AccessImagePatch(image, rect, plane_index, addr, ptr, usage):
    if addr is None:
        addr = ffi.new('vx_imagepatch_addressing_t *')
    if ptr is not None:
        ptr = ffi.from_buffer(ptr)
    ptr_p = ffi.new('void **', ptr)
    size = ComputeImagePatchSize(image, rect, plane_index)
    status = lib.vxAccessImagePatch(image, rect, plane_index, addr, ptr_p, usage)
    return status, addr, ffi.buffer(ptr_p[0], size)

def CommitImagePatch(image, rect, plane_index, addr, ptr):
    ptr = ffi.from_buffer(ptr)
    return lib.vxCommitImagePatch(image, rect, plane_index, addr, ptr)

def FormatImagePatchAddress1d(ptr, index, addr):
    ptr = ffi.from_buffer(ptr)
    p = lib.vxFormatImagePatchAddress1d(ptr, index, addr)
    return ffi.buffer(p, addr.stride_x)

def FormatImagePatchAddress2d(ptr, x, y, addr):
    ptr = ffi.from_buffer(ptr)
    p = lib.vxFormatImagePatchAddress2d(ptr, x, y, addr)
    return ffi.buffer(p, addr.stride_x)

def GetValidRegionImage(image):
    rect = rectangle_t(0,0,0,0)
    status = lib.vxGetValidRegionImage(image, rect)
    return status, rect


# KERNEL

def ReleaseKernel(kernel):
    ref = ffi.new('vx_kernel *', kernel)
    return lib.vxReleaseKernel(ref)

def QueryKernel(kernel, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryKernel, kernel, attribute, c_type, python_type)

def SetKernelAttribute(kernel, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetKernelAttribute, kernel, attribute, value, c_type)

def AddKernel(context, name, enumeration, func_ptr, numParams, input, output, init, deinit):
    func_ptr = _callback("vx_kernel_f", func_ptr, context, FAILURE)
    input = _callback("vx_kernel_input_validate_f", input, context, FAILURE)
    output = _callback("vx_kernel_output_validate_f", output, context, FAILURE)
    if init is None:
        init = ffi.NULL
    else:
        init = _callback("vx_kernel_initialize_f", init, context, FAILURE)
    if deinit is None:
        deinit = ffi.NULL
    else:
        deinit = _callback("vx_kernel_deinitialize_f", deinit, context, FAILURE)
    return lib.vxAddKernel(context, name, enumeration, func_ptr, numParams, input, output, init, deinit)

def SetMetaFormatAttribute(meta, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetMetaFormatAttribute, meta, attribute, value, c_type)

def LoadKernels(context, module):
    if sys.version_info > (3,) and not isinstance(module, bytes):
        s = lib.vxLoadKernels(context, bytes(module, "utf8"))
    else:
        s = lib.vxLoadKernels(context, module)
    if s == SUCCESS:
        return s
    try:
        d = {}
        exec("import %s as mod" % module, d)
        mod = d['mod']
    except ImportError:
        return FAILURE
    return mod.PublishKernels(context)


# GRAPH

def ReleaseGraph(graph):
    ref = ffi.new('vx_graph *', graph)
    return lib.vxReleaseGraph(ref)

def QueryGraph(graph, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryGraph, graph, attribute, c_type, python_type)

def SetGraphAttribute(graph, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetGraphAttribute, graph, attribute, value, c_type)


# NODE

def ReleaseNode(node):
    ref = ffi.new('vx_node *', node)
    return lib.vxReleaseNode(ref)

def QueryNode(node, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryNode, node, attribute, c_type, python_type)

def SetNodeAttribute(node, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetNodeAttribute, node, attribute, value, c_type)

def RemoveNode(node):
    ref = ffi.new('vx_node *', node)
    return lib.vxReleaseNode(ref)

def AssignNodeCallback(node, callback):
    if callback is not None:
        callback = _callback("vx_nodecomplete_f", callback, node, ACTION_ABANDON)
    else:
        callback = ffi.NULL
    return lib.vxAssignNodeCallback(node, callback)


# PARAMETER

def ReleaseParameter(parameter):
    ref = ffi.new('vx_parameter *', parameter)
    return lib.vxReleaseParameter(ref)

def QueryParameter(parameter, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryParameter, parameter, attribute, c_type, python_type)


# SCALAR

def CreateScalar(context, data_type, value):
    ptr = ffi.new(_enum2ctype(data_type) + '*', value)
    return lib.vxCreateScalar(context, data_type, ptr)

def ReleaseScalar(scalar):
    ref = ffi.new('vx_scalar *', scalar)
    return lib.vxReleaseScalar(ref)

def QueryScalar(scalar, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryScalar, scalar, attribute, c_type, python_type)

def ReadScalarValue(scalar):
    s, data_type = QueryScalar(scalar, SCALAR_ATTRIBUTE_TYPE, "vx_enum")
    ptr = ffi.new(_enum2ctype(data_type) + '*')
    s = lib.vxReadScalarValue(scalar, ptr)
    return s, ptr[0]

def WriteScalarValue(scalar, value):
    s, data_type = QueryScalar(scalar, SCALAR_ATTRIBUTE_TYPE, "vx_enum")
    ptr = ffi.new(_enum2ctype(data_type) + '*', value)
    return lib.vxWriteScalarValue(scalar, ptr)


# REFERENCE

def reference(reference):
    """
    Cast the object *reference* into a "vx_reference" object.
    """
    if ffi.typeof(reference) not in _reference_types:
        raise TypeError("Can't cast %r to vx_reference" % reference)
    return ffi.cast('vx_reference', reference)

def from_reference(ref):
    """
    Cast the "vx_reference" object *ref* into it's specific type (i.e.
    "vx_image" or "vx_graqph" or ...).
    """
    s, data_type = QueryReference(ref, REF_ATTRIBUTE_TYPE, 'vx_enum')
    return ffi.cast(_enum2ctype(data_type), ref)

def QueryReference(reference, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryReference, reference, attribute, c_type, python_type)


# DELAY

def ReleaseDelay(delay):
    ref = ffi.new('vx_delay *', delay)
    return lib.vxReleaseDelay(ref)

def QueryDelay(delay, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryDelay, delay, attribute, c_type, python_type)


# LOGGING

def RegisterLogCallback(context, callback, reentrant):
    def wrapper(context, ref, status, string):
        callback(context, ref, status, ffi.string(string))
    cb = _callback('vx_log_callback_f', wrapper, context, None)
    lib.vxRegisterLogCallback(context, cb, reentrant)


# LUT

def ReleaseLUT(lut):
    ref = ffi.new('vx_lut *', lut)
    return lib.vxReleaseLUT(ref)

def QueryLUT(lut, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryLUT, lut, attribute, c_type, python_type)

def AccessLUT(lut, ptr, usage):
    if ptr is not None:
        ptr = ffi.from_buffer(ptr)
    ptr_p = ffi.new('void **', ptr)
    status = lib.vxAccessLUT(lut, ptr_p, usage)
    _, size = QueryLUT(lut, LUT_ATTRIBUTE_COUNT, 'vx_size')
    return (status, ffi.buffer(ptr_p[0], size))

def CommitLUT(lut, ptr):
    ptr = ffi.from_buffer(ptr)
    return lib.vxCommitLUT(lut, ptr)


# DISTRIBUTION

def ReleaseDistribution(distribution):
    ref = ffi.new('vx_distribution *', distribution)
    return lib.vxReleaseDistribution(ref)

def QueryDistribution(distribution, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryDistribution, distribution, attribute, c_type, python_type)

def AccessDistribution(distribution, ptr, usage):
    if ptr is not None:
        ptr = ffi.from_buffer(ptr)
    ptr_p = ffi.new('void **', ptr)
    status = lib.vxAccessDistribution(distribution, ptr_p, usage)
    _, size = QueryDistribution(distribution, DISTRIBUTION_ATTRIBUTE_SIZE, 'vx_size')
    return (status, ffi.buffer(ptr_p[0], size))

def CommitDistribution(distribution, ptr):
    ptr = ffi.from_buffer(ptr)
    return lib.vxCommitDistribution(distribution, ptr)


# THRESHOLD

def ReleaseThreshold(threshold):
    ref = ffi.new('vx_threshold *', threshold)
    return lib.vxReleaseThreshold(ref)

def QueryThreshold(threshold, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryThreshold, threshold, attribute, c_type, python_type)

def SetThresholdAttribute(threshold, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetThresholdAttribute, threshold, attribute, value, c_type)


# MATRIX

def ReleaseMatrix(matrix):
    ref = ffi.new('vx_matrix *', matrix)
    return lib.vxReleaseMatrix(ref)

def QueryMatrix(matrix, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryMatrix, matrix, attribute, c_type, python_type)

def ReadMatrix(mat, array):
    array = ffi.from_buffer(array)
    return lib.vxReadMatrix(mat, array)

def WriteMatrix(mat, array):
    array = ffi.from_buffer(array)
    return lib.vxWriteMatrix(mat, array)


# CONVOLUTION

def ReleaseConvolution(convolution):
    ref = ffi.new('vx_convolution *', convolution)
    return lib.vxReleaseConvolution(ref)

def QueryConvolution(convolution, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryConvolution, convolution, attribute, c_type, python_type)

def SetConvolutionAttribute(convolution, attribute, value, c_type=None):
    return _set_attribute(lib.vxSetConvolutionAttribute, convolution, attribute, value, c_type)

def WriteConvolutionCoefficients(conv, array):
    array = ffi.from_buffer(array)
    return lib.vxWriteConvolutionCoefficients(conv, array)

def ReadConvolutionCoefficients(conv, array):
    array = ffi.from_buffer(array)
    return lib.vxReadConvolutionCoefficients(conv, array)


# PYRAMID

def ReleasePyramid(pyramid):
    ref = ffi.new('vx_pyramid *', pyramid)
    return lib.vxReleasePyramid(ref)

def QueryPyramid(pyramid, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryPyramid, pyramid, attribute, c_type, python_type)


# REMAP

def ReleaseRemap(remap):
    ref = ffi.new('vx_remap *', remap)
    return lib.vxReleaseRemap(ref)

def QueryRemap(remap, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryRemap, remap, attribute, c_type, python_type)

def GetRemapPoint(table, dst_x, dst_y):
    src_x = ffi.new('vx_float32 *')
    src_y = ffi.new('vx_float32 *')
    status = lib.vxGetRemapPoint(table, dst_x, dst_y, src_x, src_y)
    return status, src_x[0], src_y[0]


# ARRAY

def ReleaseArray(array):
    ref = ffi.new('vx_array *', array)
    return lib.vxReleaseArray(ref)

def QueryArray(array, attribute, c_type, python_type=None):
    return _get_attribute(lib.vxQueryArray, array, attribute, c_type, python_type)

def FormatArrayPointer(ptr, index, stride):
    if sys.version_info > (3,):
        return memoryview(ptr)[index * stride:]
    else:
        return buffer(ptr, index * stride)

def ArrayItem(type, ptr, index, stride):
    return ffi.cast(type + '*', ffi.from_buffer(FormatArrayPointer(ptr, index, stride)))

def AddArrayItems(arr, count, ptr, stride):
    if not isinstance(ptr, ffi.CData):
        ptr = ffi.from_buffer(ptr)
    return lib.vxAddArrayItems(arr, count, ptr, stride)

def AccessArrayRange(arr, start, end, stride, ptr, usage):
    if ptr is not None:
        ptr = ffi.from_buffer(ptr)
    ptr_p = ffi.new('void **', ptr)
    stride_p = ffi.new('vx_size *', stride)
    status = lib.vxAccessArrayRange(arr, start, end, stride_p, ptr_p, usage)
    _, item_size = QueryArray(arr, ARRAY_ATTRIBUTE_ITEMSIZE, 'vx_size')
    return (status, stride_p[0], ffi.buffer(ptr_p[0], item_size * (end - start + 1)))

def CommitArrayRange(arr, start, end, ptr):
    ptr = ffi.from_buffer(ptr)
    return lib.vxCommitArrayRange(arr, start, end, ptr)

