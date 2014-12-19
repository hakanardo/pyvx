from pyvx.inc import vx
from pyvx.types import VxError


class attribute(object):

    def __init__(self, enum, vxtype, default=None):
        self.enum = enum
        self.vxtype = vxtype
        self.default = default

    def __get__(self, instance, owner):
        n = '_' + self.name
        if hasattr(instance, n):
            return getattr(instance, n)
        if hasattr(owner, n):
            return getattr(owner, n)
        return self.default

    def __set__(self, instance, value):
        setattr(instance, '_' + self.name, value)


class VxObjectMeta(type):

    def __new__(cls, name, bases, attrs):
        attributes = {}
        for b in bases:
            if hasattr(b, '_attributes'):
                attributes.update(b._attributes)
        for n, a in attrs.items():
            if isinstance(a, attribute):
                a.name = n
                attributes[a.enum] = a
        cls = type.__new__(cls, name, bases, attrs)
        cls._attributes = attributes
        return cls


class VxObject(object):
    __metaclass__ = VxObjectMeta


class api(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, fn):
        if not hasattr(fn, 'apis'):
            fn.apis = []
        fn.apis.append(self)
        return fn


class capi(object):

    def __init__(self, cdecl):
        self.cdecl = cdecl

    def __call__(self, fn):
        if not hasattr(fn, 'capis'):
            fn.capis = []
        fn.capis.append(self)
        return fn

##############################################################################


class Reference(VxObject):
    _type = vx.TYPE_REFERENCE

    count = attribute(vx.REF_ATTRIBUTE_COUNT, vx.TYPE_UINT32, 1)
    type = attribute(vx.REF_ATTRIBUTE_TYPE, vx.TYPE_ENUM, vx.TYPE_REFERENCE)

    def query(self, attribute):
        return vx.SUCCESS, getattr(self, self._attributes[attribute].name)

    def new_handle(self):
        h = vx.ffi.new_handle(self)
        self.context.keep_alive.add(h)
        return h

    def del_handle(self, ptr):
        self.context.keep_alive.remove(ptr)

    def add_log_entry(self, status, message):
        if status != vx.SUCCESS:
            print 'LOG:', status, self, message


@api('QueryContext')
@api('QueryImage')
@api('QueryKernel')
@api('QueryGraph')
@api('QueryNode')
@api('QueryParameter')
@api('QueryScalar')
@api('QueryReference')
@api('QueryDelay')
@api('QueryLUT')
@api('QueryDistribution')
@api('QueryThreshold')
@api('QueryMatrix')
@api('QueryConvolution')
@api('QueryPyramid')
@api('QueryRemap')
@api('QueryArray')
def query(ref, attribute):
    return ref.query(attribute)


@capi('vx_status vxQueryContext(vx_context context, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryImage(vx_image image, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryKernel(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryGraph(vx_graph graph, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryNode(vx_node node, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryParameter(vx_parameter param, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryScalar(vx_scalar scalar, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryReference(vx_reference ref, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryDelay(vx_delay delay, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryLUT(vx_lut lut, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryDistribution(vx_distribution distribution, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryThreshold(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryMatrix(vx_matrix mat, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryConvolution(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryPyramid(vx_pyramid pyr, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryRemap(vx_remap r, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxQueryArray(vx_array arr, vx_enum attribute, void *ptr, vx_size size)')
def c_query(ref, attribute, ptr, size):
    a = ref._attributes.get(attribute)
    if a is None:
        return vx.FAILURE
    if size != vx.ffi.sizeof(a.vxtype.ctype):
        ref.add_log_entry(vx.FAILURE, "Bad size %d in query, expected %d\n" % (
            size, vx.ffi.sizeof(a.vxtype.ctype)))
        return vx.FAILURE
    status, value = query(ref, attribute)
    ptr = vx.ffi.cast(a.vxtype.ctype + "*", ptr)
    if isinstance(value, VxObject):
        ptr[0] = ref.context.new_handle(value)
    else:
        ptr[0] = value
    return status


@api('SetContextAttribute')
@api('SetImageAttribute')
@api('SetKernelAttribute')
@api('SetGraphAttribute')
@api('SetNodeAttribute')
@api('SetThresholdAttribute')
@api('SetConvolutionAttribute')
@api('SetMetaFormatAttribute')
def set_attribute(ref, attribute):
    return ref.set_attribute(attribute)


@capi('vx_status vxSetContextAttribute(vx_context context, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetImageAttribute(vx_image image, vx_enum attribute, void *out, vx_size size)')
@capi('vx_status vxSetKernelAttribute(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetGraphAttribute(vx_graph graph, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetNodeAttribute(vx_node node, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetThresholdAttribute(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetConvolutionAttribute(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size)')
@capi('vx_status vxSetMetaFormatAttribute(vx_meta_format meta, vx_enum attribute, void *ptr, vx_size size)')
def c_set_attribute(ref, attribute, ptr, size):
    a = ref._attributes.get(attribute)
    if a is None:
        return vx.FAILURE
    if size != vx.ffi.sizeof(a.vxtype.ctype):
        ref.add_log_entry(vx.FAILURE, "Bad size %d in set attribute, expected %d\n" % (
            size, vx.ffi.sizeof(a.vxtype.ctype)))
        return vx.FAILURE
    ptr = vx.ffi.cast(a.vxtype.ctype + "*", ptr)
    return ref.set_attribute(ptr[0])


@api('ReleaseContext')
@api('ReleaseImage')
@api('ReleaseKernel')
@api('ReleaseGraph')
@api('ReleaseNode')
@api('ReleaseParameter')
@api('ReleaseScalar')
@api('ReleaseDelay')
@api('ReleaseLUT')
@api('ReleaseDistribution')
@api('ReleaseThreshold')
@api('ReleaseMatrix')
@api('ReleaseConvolution')
@api('ReleasePyramid')
@api('ReleaseRemap')
@api('ReleaseArray')
def release(ref):
    pass


@capi('vx_status vxReleaseContext(vx_context *context)')
@capi('vx_status vxReleaseImage(vx_image *image)')
@capi('vx_status vxReleaseKernel(vx_kernel *kernel)')
@capi('vx_status vxReleaseGraph(vx_graph *graph)')
@capi('vx_status vxReleaseNode(vx_node *node)')
@capi('vx_status vxReleaseParameter(vx_parameter *param)')
@capi('vx_status vxReleaseScalar(vx_scalar *scalar)')
@capi('vx_status vxReleaseDelay(vx_delay *delay)')
@capi('vx_status vxReleaseLUT(vx_lut *lut)')
@capi('vx_status vxReleaseDistribution(vx_distribution *distribution)')
@capi('vx_status vxReleaseThreshold(vx_threshold *thresh)')
@capi('vx_status vxReleaseMatrix(vx_matrix *mat)')
@capi('vx_status vxReleaseConvolution(vx_convolution *conv)')
@capi('vx_status vxReleasePyramid(vx_pyramid *pyr)')
@capi('vx_status vxReleaseRemap(vx_remap *table)')
@capi('vx_status vxReleaseArray(vx_array *arr)')
def c_release(ref):
    obj = vx.ffi.from_handle(vx.ffi.cast('void *', ref[0]))
    obj.context.del_handle(ref[0])
    ref[0] = vx.ffi.NULL
    return vx.SUCCESS

##############################################################################


class Context(Reference):
    _type = vx.TYPE_CONTEXT

    vendor_id = attribute(
        vx.CONTEXT_ATTRIBUTE_VENDOR_ID, vx.TYPE_UINT16, vx.ID_DEFAULT)
    version = attribute(
        vx.CONTEXT_ATTRIBUTE_VERSION, vx.TYPE_UINT16, vx.VERSION)
    unique_kernels = attribute(
        vx.CONTEXT_ATTRIBUTE_UNIQUE_KERNELS, vx.TYPE_UINT32)
    # FIXME: ...

    def __init__(self):
        self.keep_alive = set()
        self.context = self

    def create_image(self, width, height, color):
        raise NotImplementedError

    def create_graph(self, early_verify):
        raise NotImplementedError


@api('CreateContext')
@capi('vx_context vxCreateContext()')
def create_context():
    from pyvx.optimized_backend import Context
    return Context()


@api('GetContext')
@capi('vx_context vxGetContext(vx_reference reference)')
def get_context(reference):
    raise NotImplementedError


@api('Hint')
@capi('vx_status vxHint(vx_context context, vx_reference reference, vx_enum hint)')
def hint(context, reference, hint):
    raise NotImplementedError


@api('Directive')
@capi('vx_status vxDirective(vx_context context, vx_reference reference, vx_enum directive)')
def directive(context, reference, directive):
    raise NotImplementedError


@api('GetStatus')
@capi('vx_status vxGetStatus(vx_reference reference)')
def get_status(reference):
    raise NotImplementedError


@api('RegisterUserStruct')
@capi('vx_enum vxRegisterUserStruct(vx_context context, vx_size size)')
def register_user_struct(context, size):
    raise NotImplementedError


##############################################################################

class Image(Reference):
    _type = vx.TYPE_IMAGE


@api('CreateImage')
@capi('vx_image vxCreateImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color)')
def create_image(context, width, height, color):
    return context.create_image(width, height, color)


@api('CreateImageFromROI')
@capi('vx_image vxCreateImageFromROI(vx_image img, vx_rectangle_t *rect)')
def create_image_from_roi(img, rect):
    raise NotImplementedError


@api('CreateUniformImage')
@capi('vx_image vxCreateUniformImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color, void *value)')
def create_uniform_image(context, width, height, color, value):
    raise NotImplementedError


@api('CreateVirtualImage')
@capi('vx_image vxCreateVirtualImage(vx_graph graph, vx_uint32 width, vx_uint32 height, vx_df_image color)')
def create_virtual_image(graph, width, height, color):
    return graph.context.create_virtual_image(graph, width, height, color)


@api('CreateImageFromHandle')
@capi('vx_image vxCreateImageFromHandle(vx_context context, vx_df_image color, vx_imagepatch_addressing_t addrs[], void *ptrs[], vx_enum import_type)')
def create_image_from_handle(context, color, addrs[], ptrs[], import_type):
    raise NotImplementedError


@api('ComputeImagePatchSize')
@capi('vx_size vxComputeImagePatchSize(vx_image image, vx_rectangle_t *rect, vx_uint32 plane_index)')
def compute_image_patch_size(image, rect, plane_index):
    raise NotImplementedError


@api('AccessImagePatch')
@capi('vx_status vxAccessImagePatch(vx_image image, vx_rectangle_t *rect, vx_uint32 plane_index, vx_imagepatch_addressing_t *addr, void **ptr, vx_enum usage)')
def access_image_patch(image, rect, plane_index, addr, ptr, usage):
    raise NotImplementedError


@api('CommitImagePatch')
@capi('vx_status vxCommitImagePatch(vx_image image, vx_rectangle_t *rect, vx_uint32 plane_index, vx_imagepatch_addressing_t *addr, void *ptr)')
def commit_image_patch(image, rect, plane_index, addr, ptr):
    raise NotImplementedError


@api('FormatImagePatchAddress1d')
@capi('void *vxFormatImagePatchAddress1d(void *ptr, vx_uint32 index, vx_imagepatch_addressing_t *addr)')
def format_image_patch_address1d(ptr, index, addr):
    raise NotImplementedError


@api('FormatImagePatchAddress2d')
@capi('void *vxFormatImagePatchAddress2d(void *ptr, vx_uint32 x, vx_uint32 y, vx_imagepatch_addressing_t *addr)')
def format_image_patch_address2d(ptr, x, y, addr):
    raise NotImplementedError


@api('GetValidRegionImage')
@capi('vx_status vxGetValidRegionImage(vx_image image, vx_rectangle_t *rect)')
def get_valid_region_image(image, rect):
    raise NotImplementedError

##############################################################################


class Kernel(Reference):
    _type = vx.TYPE_KERNEL


@api('LoadKernels')
@capi('vx_status vxLoadKernels(vx_context context, vx_char *module)')
def load_kernels(context, module):
    raise NotImplementedError


@api('GetKernelByName')
@capi('vx_kernel vxGetKernelByName(vx_context context, vx_char *name)')
def get_kernel_by_name(context, name):
    raise NotImplementedError


@api('GetKernelByEnum')
@capi('vx_kernel vxGetKernelByEnum(vx_context context, vx_enum kernel)')
def get_kernel_by_enum(context, kernel):
    raise NotImplementedError


@api('AddKernel')
@capi('vx_kernel vxAddKernel(vx_context context, vx_char name[VX_MAX_KERNEL_NAME], vx_enum enumeration, vx_kernel_f func_ptr, vx_uint32 numParams, vx_kernel_input_validate_f input, vx_kernel_output_validate_f output, vx_kernel_initialize_f init, vx_kernel_deinitialize_f deinit)')
def add_kernel(context, name[VX_MAX_KERNEL_NAME], enumeration, func_ptr, numParams, input, output, init, deinit):
    raise NotImplementedError


@api('FinalizeKernel')
@capi('vx_status vxFinalizeKernel(vx_kernel kernel)')
def finalize_kernel(kernel):
    raise NotImplementedError


@api('AddParameterToKernel')
@capi('vx_status vxAddParameterToKernel(vx_kernel kernel, vx_uint32 index, vx_enum dir, vx_enum data_type, vx_enum state)')
def add_parameter_to_kernel(kernel, index, dir, data_type, state):
    raise NotImplementedError


@api('RemoveKernel')
@capi('vx_status vxRemoveKernel(vx_kernel kernel)')
def remove_kernel(kernel):
    raise NotImplementedError


@api('GetKernelParameterByIndex')
@capi('vx_parameter vxGetKernelParameterByIndex(vx_kernel kernel, vx_uint32 index)')
def get_kernel_parameter_by_index(kernel, index):
    raise NotImplementedError

##############################################################################


class Graph(Reference):
    _type = vx.TYPE_GRAPH

    def verify(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError


@api('CreateGraph')
@capi('vx_graph vxCreateGraph(vx_context context)')
def create_graph(context, early_verify=True):
    return context.create_graph(early_verify)


@api('VerifyGraph')
@capi('vx_status vxVerifyGraph(vx_graph graph)')
def verify_graph(graph):
    try:
        graph.verify()
    except VxError as e:
        import traceback
        graph.add_log_entry(e.errno, '\n' + traceback.format_exc())
        return e.errno
    return vx.SUCCESS


@api('ProcessGraph')
@capi('vx_status vxProcessGraph(vx_graph graph)')
def process_graph(graph):
    return graph.process()


@api('ScheduleGraph')
@capi('vx_status vxScheduleGraph(vx_graph graph)')
def schedule_graph(graph):
    raise NotImplementedError


@api('WaitGraph')
@capi('vx_status vxWaitGraph(vx_graph graph)')
def wait_graph(graph):
    raise NotImplementedError


@api('AddParameterToGraph')
@capi('vx_status vxAddParameterToGraph(vx_graph graph, vx_parameter parameter)')
def add_parameter_to_graph(graph, parameter):
    raise NotImplementedError


@api('SetGraphParameterByIndex')
@capi('vx_status vxSetGraphParameterByIndex(vx_graph graph, vx_uint32 index, vx_reference value)')
def set_graph_parameter_by_index(graph, index, value):
    raise NotImplementedError


@api('GetGraphParameterByIndex')
@capi('vx_parameter vxGetGraphParameterByIndex(vx_graph graph, vx_uint32 index)')
def get_graph_parameter_by_index(graph, index):
    raise NotImplementedError


@api('IsGraphVerified')
@capi('vx_bool vxIsGraphVerified(vx_graph graph)')
def is_graph_verified(graph):
    raise NotImplementedError

##############################################################################


class Node(Reference):
    _type = vx.TYPE_NODE


@api('CreateGenericNode')
@capi('vx_node vxCreateGenericNode(vx_graph graph, vx_kernel kernel)')
def create_generic_node(graph, kernel):
    raise NotImplementedError


@api('RemoveNode')
@capi('void vxRemoveNode(vx_node *node)')
def remove_node(node):
    raise NotImplementedError


@api('AssignNodeCallback')
@capi('vx_status vxAssignNodeCallback(vx_node node, vx_nodecomplete_f callback)')
def assign_node_callback(node, callback):
    raise NotImplementedError


@api('RetrieveNodeCallback')
@capi('vx_nodecomplete_f vxRetrieveNodeCallback(vx_node node)')
def retrieve_node_callback(node):
    raise NotImplementedError


##############################################################################

class Parameter(Reference):
    _type = vx.TYPE_PARAMETER


@api('GetParameterByIndex')
@capi('vx_parameter vxGetParameterByIndex(vx_node node, vx_uint32 index)')
def get_parameter_by_index(node, index):
    raise NotImplementedError


@api('SetParameterByIndex')
@capi('vx_status vxSetParameterByIndex(vx_node node, vx_uint32 index, vx_reference value)')
def set_parameter_by_index(node, index, value):
    raise NotImplementedError


@api('SetParameterByReference')
@capi('vx_status vxSetParameterByReference(vx_parameter parameter, vx_reference value)')
def set_parameter_by_reference(parameter, value):
    raise NotImplementedError


##############################################################################

class Scalar(Reference):
    _type = vx.TYPE_SCALAR


@api('CreateScalar')
@capi('vx_scalar vxCreateScalar(vx_context context, vx_enum data_type, void *ptr)')
def create_scalar(context, data_type, ptr):
    raise NotImplementedError


@api('AccessScalarValue')
@capi('vx_status vxAccessScalarValue(vx_scalar ref, void *ptr)')
def access_scalar_value(ref, ptr):
    raise NotImplementedError


@api('CommitScalarValue')
@capi('vx_status vxCommitScalarValue(vx_scalar ref, void *ptr)')
def commit_scalar_value(ref, ptr):
    raise NotImplementedError

##############################################################################


class Delay(Reference):
    _type = vx.TYPE_DELAY


@api('CreateDelay')
@capi('vx_delay vxCreateDelay(vx_context context, vx_reference exemplar, vx_size count)')
def create_delay(context, exemplar, count):
    raise NotImplementedError


@api('GetReferenceFromDelay')
@capi('vx_reference vxGetReferenceFromDelay(vx_delay delay, vx_int32 index)')
def get_reference_from_delay(delay, index):
    raise NotImplementedError


@api('AgeDelay')
@capi('vx_status vxAgeDelay(vx_delay delay)')
def age_delay(delay):
    raise NotImplementedError


##############################################################################

class Logging(Reference):
    _type = vx.TYPE_LOGGING


@api('AddLogEntry')
def add_log_entry(ref, status, message):
    ref.add_log_entry(status, message)

# @api('AddLogEntry')
# @capi('void vxAddLogEntry(vx_reference ref, vx_status status, const char *message, ...)')
# def add_log_entry(ref, status, message, ...):
#     raise NotImplementedError


@api('RegisterLogCallback')
@capi('void vxRegisterLogCallback(vx_context context, vx_log_callback_f callback, vx_bool reentrant)')
def register_log_callback(context, callback, reentrant):
    raise NotImplementedError

##############################################################################


class Lut(Reference):
    _type = vx.TYPE_LUT


@api('CreateLUT')
@capi('vx_lut vxCreateLUT(vx_context context, vx_enum data_type, vx_size count)')
def create_lut(context, data_type, count):
    raise NotImplementedError


@api('AccessLUT')
@capi('vx_status vxAccessLUT(vx_lut lut, void **ptr, vx_enum usage)')
def access_lut(lut, ptr, usage):
    raise NotImplementedError


@api('CommitLUT')
@capi('vx_status vxCommitLUT(vx_lut lut, void *ptr)')
def commit_lut(lut, ptr):
    raise NotImplementedError

##############################################################################


class Distribution(Reference):
    _type = vx.TYPE_DISTRIBUTION


@api('CreateDistribution')
@capi('vx_distribution vxCreateDistribution(vx_context context, vx_size numBins, vx_size offset, vx_size range)')
def create_distribution(context, numBins, offset, range):
    raise NotImplementedError


@api('AccessDistribution')
@capi('vx_status vxAccessDistribution(vx_distribution distribution, void **ptr, vx_enum usage)')
def access_distribution(distribution, ptr, usage):
    raise NotImplementedError


@api('CommitDistribution')
@capi('vx_status vxCommitDistribution(vx_distribution distribution, void * ptr)')
def commit_distribution(distribution, ptr):
    raise NotImplementedError

##############################################################################


class Threshold(Reference):
    _type = vx.TYPE_THRESHOLD


@api('CreateThreshold')
@capi('vx_threshold vxCreateThreshold(vx_context c, vx_enum thresh_type, vx_enum data_type)')
def create_threshold(c, thresh_type, data_type):
    raise NotImplementedError

##############################################################################


class Matrix(Reference):
    _type = vx.TYPE_MATRIX


@api('CreateMatrix')
@capi('vx_matrix vxCreateMatrix(vx_context c, vx_enum data_type, vx_size columns, vx_size rows)')
def create_matrix(c, data_type, columns, rows):
    raise NotImplementedError


@api('AccessMatrix')
@capi('vx_status vxAccessMatrix(vx_matrix mat, void *array)')
def access_matrix(mat, array):
    raise NotImplementedError


@api('CommitMatrix')
@capi('vx_status vxCommitMatrix(vx_matrix mat, void *array)')
def commit_matrix(mat, array):
    raise NotImplementedError

##############################################################################


class Convolution(Reference):
    _type = vx.TYPE_CONVOLUTION


@api('CreateConvolution')
@capi('vx_convolution vxCreateConvolution(vx_context context, vx_size columns, vx_size rows)')
def create_convolution(context, columns, rows):
    raise NotImplementedError


@api('AccessConvolutionCoefficients')
@capi('vx_status vxAccessConvolutionCoefficients(vx_convolution conv, vx_int16 *array)')
def access_convolution_coefficients(conv, array):
    raise NotImplementedError


@api('CommitConvolutionCoefficients')
@capi('vx_status vxCommitConvolutionCoefficients(vx_convolution conv, vx_int16 *array)')
def commit_convolution_coefficients(conv, array):
    raise NotImplementedError

##############################################################################


class Pyramid(Reference):
    _type = vx.TYPE_PYRAMID


@api('CreatePyramid')
@capi('vx_pyramid vxCreatePyramid(vx_context context, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format)')
def create_pyramid(context, levels, scale, width, height, format):
    raise NotImplementedError


@api('CreateVirtualPyramid')
@capi('vx_pyramid vxCreateVirtualPyramid(vx_graph graph, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format)')
def create_virtual_pyramid(graph, levels, scale, width, height, format):
    raise NotImplementedError


@api('GetPyramidLevel')
@capi('vx_image vxGetPyramidLevel(vx_pyramid pyr, vx_uint32 index)')
def get_pyramid_level(pyr, index):
    raise NotImplementedError

##############################################################################


class Remap(Reference):
    _type = vx.TYPE_REMAP


@api('CreateRemap')
@capi('vx_remap vxCreateRemap(vx_context context, vx_uint32 src_width, vx_uint32 src_height, vx_uint32 dst_width, vx_uint32 dst_height)')
def create_remap(context, src_width, src_height, dst_width, dst_height):
    raise NotImplementedError


@api('SetRemapPoint')
@capi('vx_status vxSetRemapPoint(vx_remap table, vx_uint32 dst_x, vx_uint32 dst_y, vx_float32 src_x, vx_float32 src_y)')
def set_remap_point(table, dst_x, dst_y, src_x, src_y):
    raise NotImplementedError


@api('GetRemapPoint')
@capi('vx_status vxGetRemapPoint(vx_remap table, vx_uint32 dst_x, vx_uint32 dst_y, vx_float32 *src_x, vx_float32 *src_y)')
def get_remap_point(table, dst_x, dst_y, src_x, src_y):
    raise NotImplementedError

##############################################################################


class Array(Reference):
    _type = vx.TYPE_ARRAY


@api('CreateArray')
@capi('vx_array vxCreateArray(vx_context context, vx_enum item_type, vx_size capacity)')
def create_array(context, item_type, capacity):
    raise NotImplementedError


@api('CreateVirtualArray')
@capi('vx_array vxCreateVirtualArray(vx_graph graph, vx_enum item_type, vx_size capacity)')
def create_virtual_array(graph, item_type, capacity):
    raise NotImplementedError


@api('AddArrayItems')
@capi('vx_status vxAddArrayItems(vx_array arr, vx_size count, void *ptr, vx_size stride)')
def add_array_items(arr, count, ptr, stride):
    raise NotImplementedError


@api('TruncateArray')
@capi('vx_status vxTruncateArray(vx_array arr, vx_size new_num_items)')
def truncate_array(arr, new_num_items):
    raise NotImplementedError


@api('AccessArrayRange')
@capi('vx_status vxAccessArrayRange(vx_array arr, vx_size start, vx_size end, vx_size *stride, void **ptr, vx_enum usage)')
def access_array_range(arr, start, end, stride, ptr, usage):
    raise NotImplementedError


@api('CommitArrayRange')
@capi('vx_status vxCommitArrayRange(vx_array arr, vx_size start, vx_size end, void *ptr)')
def commit_array_range(arr, start, end, ptr):
    raise NotImplementedError

##############################################################################


class MetaFormat(Reference):
    _type = vx.TYPE_META_FORMAT
