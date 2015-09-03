from pyvx.backend import lib, ffi
ACTION_ABANDON = lib.VX_ACTION_ABANDON
ACTION_CONTINUE = lib.VX_ACTION_CONTINUE
ARRAY_ATTRIBUTE_CAPACITY = lib.VX_ARRAY_ATTRIBUTE_CAPACITY
ARRAY_ATTRIBUTE_ITEMSIZE = lib.VX_ARRAY_ATTRIBUTE_ITEMSIZE
ARRAY_ATTRIBUTE_ITEMTYPE = lib.VX_ARRAY_ATTRIBUTE_ITEMTYPE
ARRAY_ATTRIBUTE_NUMITEMS = lib.VX_ARRAY_ATTRIBUTE_NUMITEMS
ATTRIBUTE_ID_MASK = lib.VX_ATTRIBUTE_ID_MASK
BIDIRECTIONAL = lib.VX_BIDIRECTIONAL
BORDER_MODE_CONSTANT = lib.VX_BORDER_MODE_CONSTANT
BORDER_MODE_REPLICATE = lib.VX_BORDER_MODE_REPLICATE
BORDER_MODE_UNDEFINED = lib.VX_BORDER_MODE_UNDEFINED
CHANNEL_0 = lib.VX_CHANNEL_0
CHANNEL_1 = lib.VX_CHANNEL_1
CHANNEL_2 = lib.VX_CHANNEL_2
CHANNEL_3 = lib.VX_CHANNEL_3
CHANNEL_A = lib.VX_CHANNEL_A
CHANNEL_B = lib.VX_CHANNEL_B
CHANNEL_G = lib.VX_CHANNEL_G
CHANNEL_R = lib.VX_CHANNEL_R
CHANNEL_RANGE_FULL = lib.VX_CHANNEL_RANGE_FULL
CHANNEL_RANGE_RESTRICTED = lib.VX_CHANNEL_RANGE_RESTRICTED
CHANNEL_U = lib.VX_CHANNEL_U
CHANNEL_V = lib.VX_CHANNEL_V
CHANNEL_Y = lib.VX_CHANNEL_Y
COLOR_SPACE_BT601_525 = lib.VX_COLOR_SPACE_BT601_525
COLOR_SPACE_BT601_625 = lib.VX_COLOR_SPACE_BT601_625
COLOR_SPACE_BT709 = lib.VX_COLOR_SPACE_BT709
COLOR_SPACE_DEFAULT = lib.VX_COLOR_SPACE_DEFAULT
COLOR_SPACE_NONE = lib.VX_COLOR_SPACE_NONE
CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION = lib.VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION
CONTEXT_ATTRIBUTE_EXTENSIONS = lib.VX_CONTEXT_ATTRIBUTE_EXTENSIONS
CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE = lib.VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE
CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE = lib.VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE
CONTEXT_ATTRIBUTE_IMPLEMENTATION = lib.VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION
CONTEXT_ATTRIBUTE_MODULES = lib.VX_CONTEXT_ATTRIBUTE_MODULES
CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION = lib.VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION
CONTEXT_ATTRIBUTE_REFERENCES = lib.VX_CONTEXT_ATTRIBUTE_REFERENCES
CONTEXT_ATTRIBUTE_UNIQUE_KERNELS = lib.VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS
CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE = lib.VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE
CONTEXT_ATTRIBUTE_VENDOR_ID = lib.VX_CONTEXT_ATTRIBUTE_VENDOR_ID
CONTEXT_ATTRIBUTE_VERSION = lib.VX_CONTEXT_ATTRIBUTE_VERSION
CONVERT_POLICY_SATURATE = lib.VX_CONVERT_POLICY_SATURATE
CONVERT_POLICY_WRAP = lib.VX_CONVERT_POLICY_WRAP
CONVOLUTION_ATTRIBUTE_COLUMNS = lib.VX_CONVOLUTION_ATTRIBUTE_COLUMNS
CONVOLUTION_ATTRIBUTE_ROWS = lib.VX_CONVOLUTION_ATTRIBUTE_ROWS
CONVOLUTION_ATTRIBUTE_SCALE = lib.VX_CONVOLUTION_ATTRIBUTE_SCALE
CONVOLUTION_ATTRIBUTE_SIZE = lib.VX_CONVOLUTION_ATTRIBUTE_SIZE
DELAY_ATTRIBUTE_SLOTS = lib.VX_DELAY_ATTRIBUTE_SLOTS
DELAY_ATTRIBUTE_TYPE = lib.VX_DELAY_ATTRIBUTE_TYPE
DF_IMAGE_IYUV = lib.VX_DF_IMAGE_IYUV
DF_IMAGE_NV12 = lib.VX_DF_IMAGE_NV12
DF_IMAGE_NV21 = lib.VX_DF_IMAGE_NV21
DF_IMAGE_RGB = lib.VX_DF_IMAGE_RGB
DF_IMAGE_RGBX = lib.VX_DF_IMAGE_RGBX
DF_IMAGE_S16 = lib.VX_DF_IMAGE_S16
DF_IMAGE_S32 = lib.VX_DF_IMAGE_S32
DF_IMAGE_U16 = lib.VX_DF_IMAGE_U16
DF_IMAGE_U32 = lib.VX_DF_IMAGE_U32
DF_IMAGE_U8 = lib.VX_DF_IMAGE_U8
DF_IMAGE_UYVY = lib.VX_DF_IMAGE_UYVY
DF_IMAGE_VIRT = lib.VX_DF_IMAGE_VIRT
DF_IMAGE_YUV4 = lib.VX_DF_IMAGE_YUV4
DF_IMAGE_YUYV = lib.VX_DF_IMAGE_YUYV
DIRECTIVE_DISABLE_LOGGING = lib.VX_DIRECTIVE_DISABLE_LOGGING
DIRECTIVE_ENABLE_LOGGING = lib.VX_DIRECTIVE_ENABLE_LOGGING
DISTRIBUTION_ATTRIBUTE_BINS = lib.VX_DISTRIBUTION_ATTRIBUTE_BINS
DISTRIBUTION_ATTRIBUTE_DIMENSIONS = lib.VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS
DISTRIBUTION_ATTRIBUTE_OFFSET = lib.VX_DISTRIBUTION_ATTRIBUTE_OFFSET
DISTRIBUTION_ATTRIBUTE_RANGE = lib.VX_DISTRIBUTION_ATTRIBUTE_RANGE
DISTRIBUTION_ATTRIBUTE_SIZE = lib.VX_DISTRIBUTION_ATTRIBUTE_SIZE
DISTRIBUTION_ATTRIBUTE_WINDOW = lib.VX_DISTRIBUTION_ATTRIBUTE_WINDOW
ENUM_ACCESSOR = lib.VX_ENUM_ACCESSOR
ENUM_ACTION = lib.VX_ENUM_ACTION
ENUM_BORDER_MODE = lib.VX_ENUM_BORDER_MODE
ENUM_CHANNEL = lib.VX_ENUM_CHANNEL
ENUM_COLOR_RANGE = lib.VX_ENUM_COLOR_RANGE
ENUM_COLOR_SPACE = lib.VX_ENUM_COLOR_SPACE
ENUM_COMPARISON = lib.VX_ENUM_COMPARISON
ENUM_CONVERT_POLICY = lib.VX_ENUM_CONVERT_POLICY
ENUM_DIRECTION = lib.VX_ENUM_DIRECTION
ENUM_DIRECTIVE = lib.VX_ENUM_DIRECTIVE
ENUM_HINT = lib.VX_ENUM_HINT
ENUM_IMPORT_MEM = lib.VX_ENUM_IMPORT_MEM
ENUM_INTERPOLATION = lib.VX_ENUM_INTERPOLATION
ENUM_MASK = lib.VX_ENUM_MASK
ENUM_NORM_TYPE = lib.VX_ENUM_NORM_TYPE
ENUM_OVERFLOW = lib.VX_ENUM_OVERFLOW
ENUM_PARAMETER_STATE = lib.VX_ENUM_PARAMETER_STATE
ENUM_ROUND_POLICY = lib.VX_ENUM_ROUND_POLICY
ENUM_TERM_CRITERIA = lib.VX_ENUM_TERM_CRITERIA
ENUM_THRESHOLD_TYPE = lib.VX_ENUM_THRESHOLD_TYPE
ENUM_TYPE_MASK = lib.VX_ENUM_TYPE_MASK
ERROR_GRAPH_ABANDONED = lib.VX_ERROR_GRAPH_ABANDONED
ERROR_GRAPH_SCHEDULED = lib.VX_ERROR_GRAPH_SCHEDULED
ERROR_INVALID_DIMENSION = lib.VX_ERROR_INVALID_DIMENSION
ERROR_INVALID_FORMAT = lib.VX_ERROR_INVALID_FORMAT
ERROR_INVALID_GRAPH = lib.VX_ERROR_INVALID_GRAPH
ERROR_INVALID_LINK = lib.VX_ERROR_INVALID_LINK
ERROR_INVALID_MODULE = lib.VX_ERROR_INVALID_MODULE
ERROR_INVALID_NODE = lib.VX_ERROR_INVALID_NODE
ERROR_INVALID_PARAMETERS = lib.VX_ERROR_INVALID_PARAMETERS
ERROR_INVALID_REFERENCE = lib.VX_ERROR_INVALID_REFERENCE
ERROR_INVALID_SCOPE = lib.VX_ERROR_INVALID_SCOPE
ERROR_INVALID_TYPE = lib.VX_ERROR_INVALID_TYPE
ERROR_INVALID_VALUE = lib.VX_ERROR_INVALID_VALUE
ERROR_MULTIPLE_WRITERS = lib.VX_ERROR_MULTIPLE_WRITERS
ERROR_NOT_ALLOCATED = lib.VX_ERROR_NOT_ALLOCATED
ERROR_NOT_COMPATIBLE = lib.VX_ERROR_NOT_COMPATIBLE
ERROR_NOT_IMPLEMENTED = lib.VX_ERROR_NOT_IMPLEMENTED
ERROR_NOT_SUFFICIENT = lib.VX_ERROR_NOT_SUFFICIENT
ERROR_NOT_SUPPORTED = lib.VX_ERROR_NOT_SUPPORTED
ERROR_NO_MEMORY = lib.VX_ERROR_NO_MEMORY
ERROR_NO_RESOURCES = lib.VX_ERROR_NO_RESOURCES
ERROR_OPTIMIZED_AWAY = lib.VX_ERROR_OPTIMIZED_AWAY
ERROR_REFERENCE_NONZERO = lib.VX_ERROR_REFERENCE_NONZERO
FAILURE = lib.VX_FAILURE
GRAPH_ATTRIBUTE_NUMNODES = lib.VX_GRAPH_ATTRIBUTE_NUMNODES
GRAPH_ATTRIBUTE_NUMPARAMETERS = lib.VX_GRAPH_ATTRIBUTE_NUMPARAMETERS
GRAPH_ATTRIBUTE_PERFORMANCE = lib.VX_GRAPH_ATTRIBUTE_PERFORMANCE
GRAPH_ATTRIBUTE_STATUS = lib.VX_GRAPH_ATTRIBUTE_STATUS
HINT_SERIALIZE = lib.VX_HINT_SERIALIZE
ID_AMD = lib.VX_ID_AMD
ID_ARM = lib.VX_ID_ARM
ID_AXIS = lib.VX_ID_AXIS
ID_BDTI = lib.VX_ID_BDTI
ID_BROADCOM = lib.VX_ID_BROADCOM
ID_CEVA = lib.VX_ID_CEVA
ID_COGNIVUE = lib.VX_ID_COGNIVUE
ID_DEFAULT = lib.VX_ID_DEFAULT
ID_FREESCALE = lib.VX_ID_FREESCALE
ID_IMAGINATION = lib.VX_ID_IMAGINATION
ID_INTEL = lib.VX_ID_INTEL
ID_ITSEEZ = lib.VX_ID_ITSEEZ
ID_KHRONOS = lib.VX_ID_KHRONOS
ID_MARVELL = lib.VX_ID_MARVELL
ID_MAX = lib.VX_ID_MAX
ID_MEDIATEK = lib.VX_ID_MEDIATEK
ID_MOVIDIUS = lib.VX_ID_MOVIDIUS
ID_NVIDIA = lib.VX_ID_NVIDIA
ID_QUALCOMM = lib.VX_ID_QUALCOMM
ID_RENESAS = lib.VX_ID_RENESAS
ID_SAMSUNG = lib.VX_ID_SAMSUNG
ID_ST = lib.VX_ID_ST
ID_SYNOPSYS = lib.VX_ID_SYNOPSYS
ID_TI = lib.VX_ID_TI
ID_VIDEANTIS = lib.VX_ID_VIDEANTIS
ID_VIVANTE = lib.VX_ID_VIVANTE
ID_XILINX = lib.VX_ID_XILINX
IMAGE_ATTRIBUTE_FORMAT = lib.VX_IMAGE_ATTRIBUTE_FORMAT
IMAGE_ATTRIBUTE_HEIGHT = lib.VX_IMAGE_ATTRIBUTE_HEIGHT
IMAGE_ATTRIBUTE_PLANES = lib.VX_IMAGE_ATTRIBUTE_PLANES
IMAGE_ATTRIBUTE_RANGE = lib.VX_IMAGE_ATTRIBUTE_RANGE
IMAGE_ATTRIBUTE_SIZE = lib.VX_IMAGE_ATTRIBUTE_SIZE
IMAGE_ATTRIBUTE_SPACE = lib.VX_IMAGE_ATTRIBUTE_SPACE
IMAGE_ATTRIBUTE_WIDTH = lib.VX_IMAGE_ATTRIBUTE_WIDTH
IMPORT_TYPE_HOST = lib.VX_IMPORT_TYPE_HOST
IMPORT_TYPE_NONE = lib.VX_IMPORT_TYPE_NONE
INPUT = lib.VX_INPUT
INTERPOLATION_TYPE_AREA = lib.VX_INTERPOLATION_TYPE_AREA
INTERPOLATION_TYPE_BILINEAR = lib.VX_INTERPOLATION_TYPE_BILINEAR
INTERPOLATION_TYPE_NEAREST_NEIGHBOR = lib.VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR
KERNEL_ABSDIFF = lib.VX_KERNEL_ABSDIFF
KERNEL_ACCUMULATE = lib.VX_KERNEL_ACCUMULATE
KERNEL_ACCUMULATE_SQUARE = lib.VX_KERNEL_ACCUMULATE_SQUARE
KERNEL_ACCUMULATE_WEIGHTED = lib.VX_KERNEL_ACCUMULATE_WEIGHTED
KERNEL_ADD = lib.VX_KERNEL_ADD
KERNEL_AND = lib.VX_KERNEL_AND
KERNEL_ATTRIBUTE_ENUM = lib.VX_KERNEL_ATTRIBUTE_ENUM
KERNEL_ATTRIBUTE_LOCAL_DATA_PTR = lib.VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR
KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE = lib.VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE
KERNEL_ATTRIBUTE_NAME = lib.VX_KERNEL_ATTRIBUTE_NAME
KERNEL_ATTRIBUTE_PARAMETERS = lib.VX_KERNEL_ATTRIBUTE_PARAMETERS
KERNEL_BOX_3x3 = lib.VX_KERNEL_BOX_3x3
KERNEL_CANNY_EDGE_DETECTOR = lib.VX_KERNEL_CANNY_EDGE_DETECTOR
KERNEL_CHANNEL_COMBINE = lib.VX_KERNEL_CHANNEL_COMBINE
KERNEL_CHANNEL_EXTRACT = lib.VX_KERNEL_CHANNEL_EXTRACT
KERNEL_COLOR_CONVERT = lib.VX_KERNEL_COLOR_CONVERT
KERNEL_CONVERTDEPTH = lib.VX_KERNEL_CONVERTDEPTH
KERNEL_CUSTOM_CONVOLUTION = lib.VX_KERNEL_CUSTOM_CONVOLUTION
KERNEL_DILATE_3x3 = lib.VX_KERNEL_DILATE_3x3
KERNEL_EQUALIZE_HISTOGRAM = lib.VX_KERNEL_EQUALIZE_HISTOGRAM
KERNEL_ERODE_3x3 = lib.VX_KERNEL_ERODE_3x3
KERNEL_FAST_CORNERS = lib.VX_KERNEL_FAST_CORNERS
KERNEL_GAUSSIAN_3x3 = lib.VX_KERNEL_GAUSSIAN_3x3
KERNEL_GAUSSIAN_PYRAMID = lib.VX_KERNEL_GAUSSIAN_PYRAMID
KERNEL_HALFSCALE_GAUSSIAN = lib.VX_KERNEL_HALFSCALE_GAUSSIAN
KERNEL_HARRIS_CORNERS = lib.VX_KERNEL_HARRIS_CORNERS
KERNEL_HISTOGRAM = lib.VX_KERNEL_HISTOGRAM
KERNEL_INTEGRAL_IMAGE = lib.VX_KERNEL_INTEGRAL_IMAGE
KERNEL_INVALID = lib.VX_KERNEL_INVALID
KERNEL_MAGNITUDE = lib.VX_KERNEL_MAGNITUDE
KERNEL_MASK = lib.VX_KERNEL_MASK
KERNEL_MAX_1_0 = lib.VX_KERNEL_MAX_1_0
KERNEL_MEAN_STDDEV = lib.VX_KERNEL_MEAN_STDDEV
KERNEL_MEDIAN_3x3 = lib.VX_KERNEL_MEDIAN_3x3
KERNEL_MINMAXLOC = lib.VX_KERNEL_MINMAXLOC
KERNEL_MULTIPLY = lib.VX_KERNEL_MULTIPLY
KERNEL_NOT = lib.VX_KERNEL_NOT
KERNEL_OPTICAL_FLOW_PYR_LK = lib.VX_KERNEL_OPTICAL_FLOW_PYR_LK
KERNEL_OR = lib.VX_KERNEL_OR
KERNEL_PHASE = lib.VX_KERNEL_PHASE
KERNEL_REMAP = lib.VX_KERNEL_REMAP
KERNEL_SCALE_IMAGE = lib.VX_KERNEL_SCALE_IMAGE
KERNEL_SOBEL_3x3 = lib.VX_KERNEL_SOBEL_3x3
KERNEL_SUBTRACT = lib.VX_KERNEL_SUBTRACT
KERNEL_TABLE_LOOKUP = lib.VX_KERNEL_TABLE_LOOKUP
KERNEL_THRESHOLD = lib.VX_KERNEL_THRESHOLD
KERNEL_WARP_AFFINE = lib.VX_KERNEL_WARP_AFFINE
KERNEL_WARP_PERSPECTIVE = lib.VX_KERNEL_WARP_PERSPECTIVE
KERNEL_XOR = lib.VX_KERNEL_XOR
LIBRARY_KHR_BASE = lib.VX_LIBRARY_KHR_BASE
LIBRARY_MASK = lib.VX_LIBRARY_MASK
LUT_ATTRIBUTE_COUNT = lib.VX_LUT_ATTRIBUTE_COUNT
LUT_ATTRIBUTE_SIZE = lib.VX_LUT_ATTRIBUTE_SIZE
LUT_ATTRIBUTE_TYPE = lib.VX_LUT_ATTRIBUTE_TYPE
MATRIX_ATTRIBUTE_COLUMNS = lib.VX_MATRIX_ATTRIBUTE_COLUMNS
MATRIX_ATTRIBUTE_ROWS = lib.VX_MATRIX_ATTRIBUTE_ROWS
MATRIX_ATTRIBUTE_SIZE = lib.VX_MATRIX_ATTRIBUTE_SIZE
MATRIX_ATTRIBUTE_TYPE = lib.VX_MATRIX_ATTRIBUTE_TYPE
MAX_IMPLEMENTATION_NAME = lib.VX_MAX_IMPLEMENTATION_NAME
MAX_KERNEL_NAME = lib.VX_MAX_KERNEL_NAME
MAX_LOG_MESSAGE_LEN = lib.VX_MAX_LOG_MESSAGE_LEN
META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE = lib.VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE
NODE_ATTRIBUTE_BORDER_MODE = lib.VX_NODE_ATTRIBUTE_BORDER_MODE
NODE_ATTRIBUTE_LOCAL_DATA_PTR = lib.VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR
NODE_ATTRIBUTE_LOCAL_DATA_SIZE = lib.VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE
NODE_ATTRIBUTE_PERFORMANCE = lib.VX_NODE_ATTRIBUTE_PERFORMANCE
NODE_ATTRIBUTE_STATUS = lib.VX_NODE_ATTRIBUTE_STATUS
NORM_L1 = lib.VX_NORM_L1
NORM_L2 = lib.VX_NORM_L2
OUTPUT = lib.VX_OUTPUT
PARAMETER_ATTRIBUTE_DIRECTION = lib.VX_PARAMETER_ATTRIBUTE_DIRECTION
PARAMETER_ATTRIBUTE_INDEX = lib.VX_PARAMETER_ATTRIBUTE_INDEX
PARAMETER_ATTRIBUTE_REF = lib.VX_PARAMETER_ATTRIBUTE_REF
PARAMETER_ATTRIBUTE_STATE = lib.VX_PARAMETER_ATTRIBUTE_STATE
PARAMETER_ATTRIBUTE_TYPE = lib.VX_PARAMETER_ATTRIBUTE_TYPE
PARAMETER_STATE_OPTIONAL = lib.VX_PARAMETER_STATE_OPTIONAL
PARAMETER_STATE_REQUIRED = lib.VX_PARAMETER_STATE_REQUIRED
PYRAMID_ATTRIBUTE_FORMAT = lib.VX_PYRAMID_ATTRIBUTE_FORMAT
PYRAMID_ATTRIBUTE_HEIGHT = lib.VX_PYRAMID_ATTRIBUTE_HEIGHT
PYRAMID_ATTRIBUTE_LEVELS = lib.VX_PYRAMID_ATTRIBUTE_LEVELS
PYRAMID_ATTRIBUTE_SCALE = lib.VX_PYRAMID_ATTRIBUTE_SCALE
PYRAMID_ATTRIBUTE_WIDTH = lib.VX_PYRAMID_ATTRIBUTE_WIDTH
READ_AND_WRITE = lib.VX_READ_AND_WRITE
READ_ONLY = lib.VX_READ_ONLY
REF_ATTRIBUTE_COUNT = lib.VX_REF_ATTRIBUTE_COUNT
REF_ATTRIBUTE_TYPE = lib.VX_REF_ATTRIBUTE_TYPE
REMAP_ATTRIBUTE_DESTINATION_HEIGHT = lib.VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT
REMAP_ATTRIBUTE_DESTINATION_WIDTH = lib.VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH
REMAP_ATTRIBUTE_SOURCE_HEIGHT = lib.VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT
REMAP_ATTRIBUTE_SOURCE_WIDTH = lib.VX_REMAP_ATTRIBUTE_SOURCE_WIDTH
ROUND_POLICY_TO_NEAREST_EVEN = lib.VX_ROUND_POLICY_TO_NEAREST_EVEN
ROUND_POLICY_TO_ZERO = lib.VX_ROUND_POLICY_TO_ZERO
SCALAR_ATTRIBUTE_TYPE = lib.VX_SCALAR_ATTRIBUTE_TYPE
SCALE_UNITY = lib.VX_SCALE_UNITY
STATUS_MIN = lib.VX_STATUS_MIN
SUCCESS = lib.VX_SUCCESS
TERM_CRITERIA_BOTH = lib.VX_TERM_CRITERIA_BOTH
TERM_CRITERIA_EPSILON = lib.VX_TERM_CRITERIA_EPSILON
TERM_CRITERIA_ITERATIONS = lib.VX_TERM_CRITERIA_ITERATIONS
THRESHOLD_ATTRIBUTE_DATA_TYPE = lib.VX_THRESHOLD_ATTRIBUTE_DATA_TYPE
THRESHOLD_ATTRIBUTE_FALSE_VALUE = lib.VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE
THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER = lib.VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER
THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER = lib.VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER
THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE = lib.VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE
THRESHOLD_ATTRIBUTE_TRUE_VALUE = lib.VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE
THRESHOLD_ATTRIBUTE_TYPE = lib.VX_THRESHOLD_ATTRIBUTE_TYPE
THRESHOLD_TYPE_BINARY = lib.VX_THRESHOLD_TYPE_BINARY
THRESHOLD_TYPE_RANGE = lib.VX_THRESHOLD_TYPE_RANGE
TYPE_ARRAY = lib.VX_TYPE_ARRAY
TYPE_BOOL = lib.VX_TYPE_BOOL
TYPE_CHAR = lib.VX_TYPE_CHAR
TYPE_CONTEXT = lib.VX_TYPE_CONTEXT
TYPE_CONVOLUTION = lib.VX_TYPE_CONVOLUTION
TYPE_COORDINATES2D = lib.VX_TYPE_COORDINATES2D
TYPE_COORDINATES3D = lib.VX_TYPE_COORDINATES3D
TYPE_DELAY = lib.VX_TYPE_DELAY
TYPE_DF_IMAGE = lib.VX_TYPE_DF_IMAGE
TYPE_DISTRIBUTION = lib.VX_TYPE_DISTRIBUTION
TYPE_ENUM = lib.VX_TYPE_ENUM
TYPE_ERROR = lib.VX_TYPE_ERROR
TYPE_FLOAT32 = lib.VX_TYPE_FLOAT32
TYPE_FLOAT64 = lib.VX_TYPE_FLOAT64
TYPE_GRAPH = lib.VX_TYPE_GRAPH
TYPE_IMAGE = lib.VX_TYPE_IMAGE
TYPE_INT16 = lib.VX_TYPE_INT16
TYPE_INT32 = lib.VX_TYPE_INT32
TYPE_INT64 = lib.VX_TYPE_INT64
TYPE_INT8 = lib.VX_TYPE_INT8
TYPE_INVALID = lib.VX_TYPE_INVALID
TYPE_KERNEL = lib.VX_TYPE_KERNEL
TYPE_KEYPOINT = lib.VX_TYPE_KEYPOINT
TYPE_LUT = lib.VX_TYPE_LUT
TYPE_MASK = lib.VX_TYPE_MASK
TYPE_MATRIX = lib.VX_TYPE_MATRIX
TYPE_META_FORMAT = lib.VX_TYPE_META_FORMAT
TYPE_NODE = lib.VX_TYPE_NODE
TYPE_OBJECT_MAX = lib.VX_TYPE_OBJECT_MAX
TYPE_PARAMETER = lib.VX_TYPE_PARAMETER
TYPE_PYRAMID = lib.VX_TYPE_PYRAMID
TYPE_RECTANGLE = lib.VX_TYPE_RECTANGLE
TYPE_REFERENCE = lib.VX_TYPE_REFERENCE
TYPE_REMAP = lib.VX_TYPE_REMAP
TYPE_SCALAR = lib.VX_TYPE_SCALAR
TYPE_SCALAR_MAX = lib.VX_TYPE_SCALAR_MAX
TYPE_SIZE = lib.VX_TYPE_SIZE
TYPE_STRUCT_MAX = lib.VX_TYPE_STRUCT_MAX
TYPE_THRESHOLD = lib.VX_TYPE_THRESHOLD
TYPE_UINT16 = lib.VX_TYPE_UINT16
TYPE_UINT32 = lib.VX_TYPE_UINT32
TYPE_UINT64 = lib.VX_TYPE_UINT64
TYPE_UINT8 = lib.VX_TYPE_UINT8
TYPE_USER_STRUCT_END = lib.VX_TYPE_USER_STRUCT_END
TYPE_USER_STRUCT_START = lib.VX_TYPE_USER_STRUCT_START
TYPE_VENDOR_OBJECT_END = lib.VX_TYPE_VENDOR_OBJECT_END
TYPE_VENDOR_OBJECT_START = lib.VX_TYPE_VENDOR_OBJECT_START
TYPE_VENDOR_STRUCT_END = lib.VX_TYPE_VENDOR_STRUCT_END
TYPE_VENDOR_STRUCT_START = lib.VX_TYPE_VENDOR_STRUCT_START
VENDOR_MASK = lib.VX_VENDOR_MASK
VERSION = lib.VX_VERSION
VERSION_1_0 = lib.VX_VERSION_1_0
WRITE_ONLY = lib.VX_WRITE_ONLY
false_e = lib.vx_false_e
true_e = lib.vx_true_e

def CreateContext():
    '''
:brief: Creates a *vx_context*.
:details: This creates a top-level object context for OpenVX.
:note: This is required to do anything else.
:returns: The reference to the implementation context *vx_context*. Any possible errors 
preventing a successful creation should be checked using *vxGetStatus*.
:ingroup: group_context
:post: *vxReleaseContext*
    '''
    return lib.vxCreateContext()
    
def ReleaseContext(context):
    '''
:brief: Releases the OpenVX object context.
:details: All reference counted objects are garbage-collected by the return of this call.
No calls are possible using the parameter context after the context has been
released until a new reference from *vxCreateContext* is returned.
All outstanding references to OpenVX objects from this context are invalid
after this call.
:param: [in] context The pointer to the reference to the context.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If context is not a *vx_context*.
:ingroup: group_context
:pre: *vxCreateContext*
    '''
    return lib.vxReleaseContext(context)
    
def GetContext(reference):
    '''
:brief: Retrieves the context from any reference from within a context.
:param: [in] reference The reference from which to extract the context.
:ingroup: group_context
:return: The overall context that created the particular
reference.
    '''
    return lib.vxGetContext(reference)
    
def QueryContext(context, attribute, ptr, size):
    '''
:brief: Queries the context for some specific information.
:param: [in] context The reference to the context.
:param: [in] attribute The attribute to query. Use a *vx_context_attribute_e*.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the context is not a *vx_context*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:retval: VX_ERROR_NOT_SUPPORTED If the attribute is not supported on this implementation.
:ingroup: group_context
    '''
    return lib.vxQueryContext(context, attribute, ptr, size)
    
def SetContextAttribute(context, attribute, ptr, size):
    '''
:brief: Sets an attribute on the context.
:param: [in] context The handle to the overall context.
:param: [in] attribute The attribute to set from *vx_context_attribute_e*.
:param: [in] ptr The pointer to the data to which to set the attribute.
:param: [in] size The size in bytes of the data to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the context is not a *vx_context*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:retval: VX_ERROR_NOT_SUPPORTED If the attribute is not settable.
:ingroup: group_context
    '''
    return lib.vxSetContextAttribute(context, attribute, ptr, size)
    
def Hint(reference, hint):
    '''
:brief: Provides a generic API to give platform-specific hints to the implementation.
:param: [in] reference The reference to the object to hint at.
This could be *vx_context*, *vx_graph*, *vx_node*, *vx_image*, *vx_array*, or any other reference.
:param: [in] hint A *vx_hint_e* :a: hint to give the OpenVX context. This is a platform-specific optimization or implementation mechanism.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No error.
:retval: VX_ERROR_INVALID_REFERENCE If context or reference is invalid.
:retval: VX_ERROR_NOT_SUPPORTED If the hint is not supported.
:ingroup: group_hint
    '''
    return lib.vxHint(reference, hint)
    
def Directive(reference, directive):
    '''
:brief: Provides a generic API to give platform-specific directives to the implementations.
:param: [in] reference The reference to the object to set the directive on.
This could be *vx_context*, *vx_graph*, *vx_node*, *vx_image*, *vx_array*, or any other reference.
:param: [in] directive The directive to set.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No error.
:retval: VX_ERROR_INVALID_REFERENCE If context or reference is invalid.
:retval: VX_ERROR_NOT_SUPPORTED If the directive is not supported.
:ingroup: group_directive
    '''
    return lib.vxDirective(reference, directive)
    
def GetStatus(reference):
    '''
:brief: Provides a generic API to return status values from Object constructors if they
fail.
:note: Users do not need to strictly check every object creator as the errors
should properly propogate and be detected during verification time or run-time.
:code:
vx_image img = vxCreateImage(context, 639, 480, VX_DF_IMAGE_UYVY);
vx_status status = vxGetStatus((vx_reference)img);
// status == VX_ERROR_INVALID_DIMENSIONS
vxReleaseImage(&img);
:endcode:
:pre: Appropriate Object Creator function.
:post: Appropriate Object Release function.
:param: [in] reference The reference to check for construction errors.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No error.
:retval:Some error occurred, please check enumeration list and constructor.
:ingroup: group_basic_features
    '''
    return lib.vxGetStatus(reference)
    
def RegisterUserStruct(context, size):
    '''
:brief: Registers user-defined structures to the context.
:param: [in] context  The reference to the implementation context.
:param: [in] size     The size of user struct in bytes.
:return: A *vx_enum* value that is a type given to the User
to refer to their custom structure when declaring a *vx_array*
of that structure.
:retval: VX_TYPE_INVALID If the namespace of types has been exhausted.
:note: This call should only be used once within the lifetime of a context for
a specific structure.

:snippet: vx_arrayrange.c array define
:ingroup: group_adv_array
    '''
    return lib.vxRegisterUserStruct(context, size)
    
def CreateImage(context, width, height, color):
    '''
:brief: Creates an opaque reference to an image buffer.
:details: Not guaranteed to exist until the *vx_graph* containing it has been verified.
:param: [in] context The reference to the implementation context.
:param: [in] width The image width in pixels.
:param: [in] height The image height in pixels.
:param: [in] color The VX_DF_IMAGE (*vx_df_image_e*) code that represents the format of the image and the color space.
:returns: An image reference *vx_image*. Any possible errors preventing a successful
creation should be checked using *vxGetStatus*.
:see: vxAccessImagePatch to obtain direct memory access to the image data.
:ingroup: group_image
    '''
    return lib.vxCreateImage(context, width, height, color)
    
def CreateImageFromROI(img, rect):
    '''
:brief: Creates an image from another image given a rectangle. This second
reference refers to the data in the original image. Updates to this image
updates the parent image. The rectangle must be defined within the pixel space
of the parent image.
:param: [in] img The reference to the parent image.
:param: [in] rect The region of interest rectangle. Must contain points within
the parent image pixel space.
:returns: An image reference *vx_image* to the sub-image. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_image
    '''
    return lib.vxCreateImageFromROI(img, rect)
    
def CreateUniformImage(context, width, height, color, value):
    '''
:brief: Creates a reference to an image object that has a singular,
uniform value in all pixels.
:details: The value pointer must reflect the specific format of the desired
image. For example:
| Color       | Value Ptr  |
|:------------|:-----------|
| *VX_DF_IMAGE_U8*   | vx_uint8|
| *VX_DF_IMAGE_S16*  | vx_int16|
| *VX_DF_IMAGE_U16*  | vx_uint16|
| *VX_DF_IMAGE_S32*  | vx_int32|
| *VX_DF_IMAGE_U32*  | vx_uint32|
| *VX_DF_IMAGE_RGB*  | vx_uint8 pixel[3] in R, G, B order |
| *VX_DF_IMAGE_RGBX* | vx_uint8 pixels[4] |
| Any YUV     | vx_uint8 pixel[3] in Y, U, V order |

:param: [in] context The reference to the implementation context.
:param: [in] width The image width in pixels.
:param: [in] height The image height in pixels.
:param: [in] color The VX_DF_IMAGE (vx_df_image_e) code that represents the format of the image and the color space.
:param: [in] value The pointer to the pixel value to which to set all pixels.
:returns: An image reference *vx_image*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
*:see: vxAccessImagePatch* to obtain direct memory access to the image data.
:note: *vxAccessImagePatch* and *vxCommitImagePatch* may be called with
a uniform image reference.
:ingroup: group_image
    '''
    return lib.vxCreateUniformImage(context, width, height, color, value)
    
def CreateVirtualImage(graph, width, height, color):
    '''
:brief: Creates an opaque reference to an image buffer with no direct
user access. This function allows setting the image width, height, or format.
:details: Virtual data objects allow users to connect various nodes within a
graph via data references without access to that data, but they also permit the
implementation to take maximum advantage of possible optimizations. Use this
API to create a data reference to link two or more nodes together when the
intermediate data are not required to be accessed by outside entities. This API
in particular allows the user to define the image format of the data without
requiring the exact dimensions. Virtual objects are scoped within the graph
they are declared a part of, and can't be shared outside of this scope.
All of the following constructions of virtual images are valid.
:code:
vx_context context = vxCreateContext();
vx_graph graph = vxCreateGraph(context);
vx_image virt[] = {
    vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_U8), // no specified dimension
    vxCreateVirtualImage(graph, 320, 240, VX_DF_IMAGE_VIRT), // no specified format
    vxCreateVirtualImage(graph, 640, 480, VX_DF_IMAGE_U8), // no user access
};
:endcode:
:param: [in] graph The reference to the parent graph.
:param: [in] width The width of the image in pixels. A value of zero informs the interface that the value is unspecified.
:param: [in] height The height of the image in pixels. A value of zero informs the interface that the value is unspecified.
:param: [in] color The VX_DF_IMAGE (*vx_df_image_e*) code that represents the format of the image and the color space. A value of *VX_DF_IMAGE_VIRT* informs the interface that the format is unspecified.
:returns: An image reference *vx_image*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:note: Passing this reference to *vxAccessImagePatch* will return an error.
:ingroup: group_image
    '''
    return lib.vxCreateVirtualImage(graph, width, height, color)
    
def CreateImageFromHandle(context, color, addrs, ptrs, import_type):
    '''
:brief: Creates a reference to an image object that was externally allocated.
:param: [in] context The reference to the implementation context.
:param: [in] color See the *vx_df_image_e* codes. This mandates the
number of planes needed to be valid in the :a: addrs and :a: ptrs arrays based on the format given.
:param: [in] addrs[] The array of image patch addressing structures that
define the dimension and stride of the array of pointers.
:param: [in] ptrs[] The array of platform-defined references to each plane.
:param: [in] import_type *vx_import_type_e*. When giving *VX_IMPORT_TYPE_HOST*
the :a: ptrs array is assumed to be HOST accessible pointers to memory.
:returns: An image reference *vx_image*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:note: The user must call vxAccessImagePatch prior to accessing the pixels of an image, even if the 
image was created via *vxCreateImageFromHandle*. Reads or writes to memory referenced 
by ptrs[ ] after calling *vxCreateImageFromHandle* without first calling 
*vxAccessImagePatch* will result in undefined behavior.
:ingroup: group_image
    '''
    return lib.vxCreateImageFromHandle(context, color, addrs, ptrs, import_type)
    
def QueryImage(image, attribute, ptr, size):
    '''
:brief: Retrieves various attributes of an image.
:param: [in] image The reference to the image to query.
:param: [in] attribute The attribute to query. Use a *vx_image_attribute_e*.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the image is not a *vx_image*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:retval: VX_ERROR_NOT_SUPPORTED If the attribute is not supported on this implementation.
:ingroup: group_image
    '''
    return lib.vxQueryImage(image, attribute, ptr, size)
    
def SetImageAttribute(image, attribute, ptr, size):
    '''
:brief: Allows setting attributes on the image.
:param: [in] image The reference to the image on which to set the attribute.
:param: [in] attribute The attribute to set. Use a *vx_image_attribute_e* enumeration.
:param: [in] ptr The pointer to the location from which to read the value.
:param: [in] size The size in bytes of the object pointed to by :a: ptr.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the image is not a *vx_image*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:ingroup: group_image
    '''
    return lib.vxSetImageAttribute(image, attribute, ptr, size)
    
def ReleaseImage(image):
    '''
:brief: Releases a reference to an image object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] image The pointer to the image to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If image is not a *vx_image*.
:ingroup: group_image
    '''
    return lib.vxReleaseImage(image)
    
def ComputeImagePatchSize(image, rect, plane_index):
    '''
:brief: This computes the size needed to retrieve an image patch from an image.
:param: [in] image The reference to the image from which to extract the patch.
:param: [in] rect The coordinates. Must be 0 <= start < end <= dimension where
dimension is width for x and height for y.
:param: [in] plane_index The plane index from which to get the data.
:return: vx_size
:ingroup: group_image
    '''
    return lib.vxComputeImagePatchSize(image, rect, plane_index)
    
def AccessImagePatch(image, rect, plane_index, addr, ptr, usage):
    '''
:brief: Allows the User to extract a rectangular patch (subset) of an image from a single plane.
:param: [in] image The reference to the image from which to extract the patch.
:param: [in] rect The coordinates from which to get the patch. Must be 0 <= start < end.
:param: [in] plane_index The plane index from which to get the data.
:param: [in, out] addr A pointer to a structure describing the addressing information of the 
image patch to accessed.
:arg: Input case: ptr is a pointer to a non-NULL pointer. The addr parameter must be the 
address of an addressing 
structure that describes how the user will access the requested image data at address (*ptr).
:arg: Output case: ptr is a pointer to a NULL pointer. The function fills the structure pointed by 
addr with the 
addressing information that the user must consult to access the pixel data at address (*ptr). 
If the image being accessed was created via *vxCreateImageFromHandle*, then the
returned addressing information will be the identical to that of the addressing structure provided 
when *vxCreateImageFromHandle* was called.
 
:param: [in, out] ptr A pointer to a pointer to a location to store the requested data.
:arg: Input case: ptr is a pointer to a non-NULL pointer to a valid pixel buffer. This buffer 
will be used in one 
of two ways, depending on the value of the usage parameter. If usage is VX_WRITE_ONLY, then the 
buffer must contain pixel data that the user wants to replace the image's pixel data with.
Otherwise (i.e., usage is not VX_WRITE_ONLY), the image's current pixel data will be written to the 
memory starting at address (*ptr) as storage memory for the access request. The caller must ensure 
enough memory has been allocated for the requested patch with the requested addressing.
If image was created via *vxCreateImageFromHandle*, and the pixel buffer pointed to by (*ptr) overlaps 
the original pixel buffer provided when image was created, then the results of such a call to 
*vxAccessImagePatch* are undefined.
:arg: Output case: ptr is a pointer to a NULL pointer. This NULL pointer will be overwritten 
with a pointer to the 
address where the requested data can be accessed. If image was created via 
*vxCreateImageFromHandle* 
then the overwriting pointer must be within the original pixel buffer provided when image was created.
:arg: (*ptr) must eventually be provided as the ptr parameter of a call to 
*vxCommitImagePatch*.

:param: [in] usage This declares the intended usage of the pointer using the *vx_accessor_e* enumeration. For uniform images Only VX_READ_ONLY is supported.
:note: The addr and ptr parameters must both be input, or both be output, otherwise the behavior is undefined.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_OPTIMIZED_AWAY The reference is a virtual image and cannot be accessed or committed.
:retval: VX_ERROR_INVALID_PARAMETERS The :a: start, :a: end, :a: plane_index, :a: stride_x, or :a: stride_y pointer is incorrect.
:retval: VX_ERROR_INVALID_REFERENCE The image reference is not actually an image reference.
:note: The user may ask for data outside the bounds of the valid region, but
such data has an undefined value.
:note: Users must be cautious to prevent passing in :e: uninitialized pointers or
addresses of uninitialized pointers to this function.
:pre: *vxComputeImagePatchSize* if users wish to allocate their own memory.
:post: *vxCommitImagePatch* with same (*ptr) value.
:ingroup: group_image
:include: vx_imagepatch.c
    '''
    return lib.vxAccessImagePatch(image, rect, plane_index, addr, ptr, usage)
    
def CommitImagePatch(image, rect, plane_index, addr, ptr):
    '''
:brief: This allows the User to commit a rectangular patch (subset) of an image from a single plane.
:param: [in] image The reference to the image from which to extract the patch.
:param: [in] rect The coordinates to which to set the patch. Must be 0 <= start <= end.
This may be 0 or a rectangle of zero area in order to indicate that the commit
must only decrement the reference count.
:param: [in] plane_index The plane index to which to set the data.
:param: [in] addr The addressing information for the image patch.
:param: [in] ptr A pointer to a pixel buffer to be committed. If the user previously provided a 
pointer to this buffer to *vxAccessImagePatch*, the buffer can be
freed or re-used after *vxCommitImagePatch* completes. If the pointer was returned by 
*vxAccessImagePatch*, reads or writes to the location pointed by ptr after 
*vxCommitImagePatch* completes will result in undefined behavior.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_OPTIMIZED_AWAY The reference is a virtual image and cannot be accessed or committed.
:retval: VX_ERROR_INVALID_PARAMETERS The :a: start, :a: end, :a: plane_index, :a: stride_x, or :a: stride_y pointer is incorrect.
:retval: VX_ERROR_INVALID_REFERENCE The image reference is not actually an image reference.
:ingroup: group_image
:include: vx_imagepatch.c
:note: If the implementation gives the client a pointer from
*vxAccessImagePatch* then implementation-specific behavior may occur.
If not, then a copy occurs from the users pointer to the internal data of the object.
:note: If the rectangle intersects bounds of the current valid region, the
valid region grows to the union of the two rectangles as long as they occur
within the bounds of the original image dimensions.
    '''
    return lib.vxCommitImagePatch(image, rect, plane_index, addr, ptr)
    
def FormatImagePatchAddress1d(ptr, index, addr):
    '''
:brief: Accesses a specific indexed pixel in an image patch.
:param: [in] ptr The base pointer of the patch as returned from *vxAccessImagePatch*.
:param: [in] index The 0 based index of the pixel count in the patch. Indexes increase horizontally by 1 then wrap around to the next row.
:param: [in] addr The pointer to the addressing mode information returned from *vxAccessImagePatch*.
:return: voidReturns the pointer to the specified pixel.
:pre: *vxAccessImagePatch*
:include: vx_imagepatch.c
:ingroup: group_image
    '''
    return lib.vxFormatImagePatchAddress1d(ptr, index, addr)
    
def FormatImagePatchAddress2d(ptr, x, y, addr):
    '''
:brief: Accesses a specific pixel at a 2d coordinate in an image patch.
:param: [in] ptr The base pointer of the patch as returned from *vxAccessImagePatch*.
:param: [in] x The x dimension within the patch.
:param: [in] y The y dimension within the patch.
:param: [in] addr The pointer to the addressing mode information returned from *vxAccessImagePatch*.
:return: voidReturns the pointer to the specified pixel.
:pre: *vxAccessImagePatch*
:include: vx_imagepatch.c
:ingroup: group_image
    '''
    return lib.vxFormatImagePatchAddress2d(ptr, x, y, addr)
    
def GetValidRegionImage(image, rect):
    '''
:brief: Retrieves the valid region of the image as a rectangle.
:details: After the image is allocated but has not been written to this
returns the full rectangle of the image so that functions do not have to manage
a case for uninitialized data. The image still retains an uninitialized
value, but once the image is written to via any means such as *vxCommitImagePatch*,
the valid region is altered to contain the maximum bounds of the written
area.
:param: [in] image The image from which to retrieve the valid region.
:param: [out] rect The destination rectangle.
:return: vx_status
:retval: VX_ERROR_INVALID_REFERENCE Invalid image.
:retval: VX_ERROR_INVALID_PARAMETERS Invalid rect.
:retval: VX_SUCCESS Valid image.
:note: This rectangle can be passed directly to *vxAccessImagePatch* to get
the full valid region of the image. Modifications from *vxCommitImagePatch*
grows the valid region.
:ingroup: group_image
    '''
    return lib.vxGetValidRegionImage(image, rect)
    
def LoadKernels(context, module):
    '''
:brief: Loads one or more kernels into the OpenVX context. This is the interface
by which OpenVX is extensible. Once the set of kernels is loaded new kernels
and their parameters can be queried.
:note: When all references to loaded kernels are released, the module
may be automatically unloaded.
:param: [in] context The reference to the implementation context.
:param: [in] module The short name of the module to load. On systems where
there are specific naming conventions for modules, the name passed
should ignore such conventions. For example: :c: libxyz.so should be
passed as just :c: xyz and the implementation will <i>do the right thing</i> that
the platform requires.
:note: This API uses the system pre-defined paths for modules.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the context is not a *vx_context*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:ingroup: group_user_kernels
:see: vxGetKernelByName
    '''
    return lib.vxLoadKernels(context, module)
    
def GetKernelByName(context, name):
    '''
:brief: Obtains a reference to a kernel using a string to specify the name.
:details: User Kernels follow a "dotted" heirarchical syntax. For example:
"com.company.example.xyz". The following are strings specifying the kernel names:

org.khronos.openvx.color_convert

org.khronos.openvx.channel_extract

org.khronos.openvx.channel_combine

org.khronos.openvx.sobel_3x3

org.khronos.openvx.magnitude

org.khronos.openvx.phase

org.khronos.openvx.scale_image

org.khronos.openvx.table_lookup

org.khronos.openvx.histogram

org.khronos.openvx.equalize_histogram

org.khronos.openvx.absdiff

org.khronos.openvx.mean_stddev

org.khronos.openvx.threshold

org.khronos.openvx.integral_image

org.khronos.openvx.dilate_3x3

org.khronos.openvx.erode_3x3

org.khronos.openvx.median_3x3

org.khronos.openvx.box_3x3

org.khronos.openvx.gaussian_3x3

org.khronos.openvx.custom_convolution

org.khronos.openvx.gaussian_pyramid

org.khronos.openvx.accumulate

org.khronos.openvx.accumulate_weighted

org.khronos.openvx.accumulate_square

org.khronos.openvx.minmaxloc

org.khronos.openvx.convertdepth

org.khronos.openvx.canny_edge_detector

org.khronos.openvx.and

org.khronos.openvx.or

org.khronos.openvx.xor

org.khronos.openvx.not

org.khronos.openvx.multiply

org.khronos.openvx.add

org.khronos.openvx.subtract

org.khronos.openvx.warp_affine

org.khronos.openvx.warp_perspective

org.khronos.openvx.harris_corners

org.khronos.openvx.fast_corners

org.khronos.openvx.optical_flow_pyr_lk

org.khronos.openvx.remap

org.khronos.openvx.halfscale_gaussian 

:param: [in] context The reference to the implementation context.
:param: [in] name The string of the name of the kernel to get.
:return: A kernel reference or zero if an error occurred.
:retval: 0 The kernel name is not found in the context.
:ingroup: group_kernel
:pre: *vxLoadKernels* if the kernel is not provided by the
OpenVX implementation.
:note: User Kernels should follow a "dotted" heirarchical syntax. For example:
"com.company.example.xyz".
    '''
    return lib.vxGetKernelByName(context, name)
    
def GetKernelByEnum(context, kernel):
    '''
:brief: Obtains a reference to the kernel using the *vx_kernel_e* enumeration.
:details: Enum values above the standard set are assumed to apply to
loaded libraries.
:param: [in] context The reference to the implementation context.
:param: [in] kernel A value from *vx_kernel_e* or a vendor or client-defined value.
:return: A *vx_kernel*.
:retval: 0 The kernel enumeration is not found in the context.
:ingroup: group_kernel
:pre: *vxLoadKernels* if the kernel is not provided by the
OpenVX implementation.
    '''
    return lib.vxGetKernelByEnum(context, kernel)
    
def QueryKernel(kernel, attribute, ptr, size):
    '''
:brief: This allows the client to query the kernel to get information about
the number of parameters, enum values, etc.
:param: [in] kernel The kernel reference to query.
:param: [in] attribute The attribute to query. Use a *vx_kernel_attribute_e*.
:param: [out] ptr The pointer to the location at which to store the resulting value.
:param: [in] size The size of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If the kernel is not a *vx_kernel*.
:retval: VX_ERROR_INVALID_PARAMETERS If any of the other parameters are incorrect.
:retval: VX_ERROR_NOT_SUPPORTED If the attribute value is not supported in this implementation.
:ingroup: group_kernel
    '''
    return lib.vxQueryKernel(kernel, attribute, ptr, size)
    
def ReleaseKernel(kernel):
    '''
:brief: Release the reference to the kernel.
The object may not be garbage collected until its total reference count is zero.
:param: [in] kernel The pointer to the kernel reference to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If kernel is not a *vx_kernel*.
:ingroup: group_kernel
    '''
    return lib.vxReleaseKernel(kernel)
    
def AddKernel(context, name, enumeration, func_ptr, numParams, input, output, init, deinit):
    '''
:brief: Allows users to add custom kernels to the known kernel
database in OpenVX at run-time. This would primarily be used by the module function
:c: vxPublishKernels.
:param: [in] context The reference to the implementation context.
:param: [in] name The string to use to match the kernel.
:param: [in] enumeration The enumerated value of the kernel to be used by clients.
:param: [in] func_ptr The process-local function pointer to be invoked.
:param: [in] numParams The number of parameters for this kernel.
:param: [in] input The pointer to *vx_kernel_input_validate_f*, which validates the
input parameters to this kernel.
:param: [in] output The pointer to *vx_kernel_output_validate_f *, which validates the
output parameters to this kernel.
:param: [in] init The kernel initialization function.
:param: [in] deinit The kernel de-initialization function.
:ingroup: group_user_kernels
:return: *vx_kernel*
:retval: 0 Indicates that an error occurred when adding the kernel.
:retval:Kernel added to OpenVX.
    '''
    return lib.vxAddKernel(context, name, enumeration, func_ptr, numParams, input, output, init, deinit)
    
def FinalizeKernel(kernel):
    '''
:brief: This API is called after all parameters have been added to the
kernel and the kernel is :e: ready to be used. Notice that the reference to the kernel created 
by vxAddKernel is still valid after the call to vxFinalizeKernel.
:param: [in] kernel The reference to the loaded kernel from *vxAddKernel*.
:return: A *vx_status_e* enumeration. If an error occurs, the kernel is not available
for usage by the clients of OpenVX. Typically this is due to a mismatch
between the number of parameters requested and given.
:pre: *vxAddKernel* and *vxAddParameterToKernel*
:ingroup: group_user_kernels
    '''
    return lib.vxFinalizeKernel(kernel)
    
def AddParameterToKernel(kernel, index, dir, data_type, state):
    '''
:brief: Allows users to set the signatures of the custom kernel.
:param: [in] kernel The reference to the kernel added with *vxAddKernel*.
:param: [in] index The index of the parameter to add.
:param: [in] dir The direction of the parameter. This must be either *VX_INPUT* or 
*VX_OUTPUT*. *VX_BIDIRECTIONAL* is not supported for this function. 
:param: [in] data_type The type of parameter. This must be a value from *vx_type_e*.
:param: [in] state The state of the parameter (required or not). This must be a value from *vx_parameter_state_e*.
:return: A *vx_status_e* enumerated value.
:retval: VX_SUCCESS Parameter is successfully set on kernel.
:retval: VX_ERROR_INVALID_REFERENCE The value passed as kernel was not a :c: vx_kernel.
:pre: *vxAddKernel*
:ingroup: group_user_kernels
    '''
    return lib.vxAddParameterToKernel(kernel, index, dir, data_type, state)
    
def RemoveKernel(kernel):
    '''
:brief: Removes a non-finalized *vx_kernel* from the *vx_context* 
and releases it. Once a *vx_kernel* has been finalized it cannot be removed.
:param: [in] kernel The reference to the kernel to remove. Returned from *vxAddKernel*.
:note: Any kernel enumerated in the base standard
cannot be removed; only kernels added through *vxAddKernel* can
be removed.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_INVALID_REFERENCE If an invalid kernel is passed in.
:retval: VX_ERROR_INVALID_PARAMETER If a base kernel is passed in.
:ingroup: group_user_kernels
    '''
    return lib.vxRemoveKernel(kernel)
    
def SetKernelAttribute(kernel, attribute, ptr, size):
    '''
:brief: Sets kernel attributes.
:param: [in] kernel The reference to the kernel.
:param: [in] attribute The enumeration of the attributes. See *vx_kernel_attribute_e*.
:param: [in] ptr The pointer to the location from which to read the attribute.
:param: [in] size The size in bytes of the data area indicated by :a: ptr in bytes.
:note: After a kernel has been passed to *vxFinalizeKernel*, no attributes
can be altered.
:return: A *vx_status_e* enumeration.
:ingroup: group_user_kernels
    '''
    return lib.vxSetKernelAttribute(kernel, attribute, ptr, size)
    
def GetKernelParameterByIndex(kernel, index):
    '''
:brief: Retrieves a *vx_parameter* from a *vx_kernel*.
:param: [in] kernel The reference to the kernel.
:param: [in] index The index of the parameter.
:return: A *vx_parameter*.
:retval: 0 Either the kernel or index is invalid.
:retval:The parameter reference.
:ingroup: group_parameter
    '''
    return lib.vxGetKernelParameterByIndex(kernel, index)
    
def CreateGraph(context):
    '''
:brief: Creates an empty graph.
:param: [in] context The reference to the implementation context.
:returns: A graph reference *vx_graph*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_graph
    '''
    return lib.vxCreateGraph(context)
    
def ReleaseGraph(graph):
    '''
:brief: Releases a reference to a graph.
The object may not be garbage collected until its total reference count is zero.
Once the reference count is zero, all node references in the graph are automatically
released as well. Data referenced by those nodes may not be released as
the user may have external references to the data.
:param: [in] graph The pointer to the graph to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If graph is not a *vx_graph*.
:ingroup: group_graph
    '''
    return lib.vxReleaseGraph(graph)
    
def VerifyGraph(graph):
    '''
:brief: Verifies the state of the graph before it is executed.
This is useful to catch programmer errors and contract errors. If not verified,
the graph verifies before being processed.
:pre: Memory for data objects is not guarenteed to exist before
this call. :post: After this call data objects exist unless
the implementation optimized them out.
:param: [in] graph The reference to the graph to verify.
:return: A status code for graphs with more than one error; it is
undefined which error will be returned. Register a log callback using *vxRegisterLogCallback*
to receive each specific error in the graph.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If graph is not a *vx_graph*.
:retval: VX_ERROR_MULTIPLE_WRITERS If the graph contains more than one writer
to any data object.
:retval: VX_ERROR_INVALID_NODE If a node in the graph is invalid or failed be created.
:retval: VX_ERROR_INVALID_GRAPH If the graph contains cycles or some other invalid topology.
:retval: VX_ERROR_INVALID_TYPE If any parameter on a node is given the wrong type.
:retval: VX_ERROR_INVALID_VALUE If any value of any parameter is out of bounds of specification.
:retval: VX_ERROR_INVALID_FORMAT If the image format is not compatible.
:ingroup: group_graph
:see: vxProcessGraph
    '''
    return lib.vxVerifyGraph(graph)
    
def ProcessGraph(graph):
    '''
:brief: This function causes the synchronous processing of a graph. If the graph
has not been verified, then the implementation verifies the graph
immediately. If verification fails this function returns a status
identical to what *vxVerifyGraph* would return. After
the graph verfies successfully then processing occurs. If the graph was
previously verified via *vxVerifyGraph* or *vxProcessGraph*
then the graph is processed. This function blocks until the graph is completed.
:param: [in] graph The graph to execute.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Graph has been processed.
:retval: VX_FAILURE A catastrophic error occurred during processing.
:retval:See *vxVerifyGraph*.
:pre: *vxVerifyGraph* must return *VX_SUCCESS* before this function will pass.
:ingroup: group_graph
:see: vxVerifyGraph
    '''
    return lib.vxProcessGraph(graph)
    
def ScheduleGraph(graph):
    '''
:brief: Schedules a graph for future execution.
:param: [in] graph The graph to schedule.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_NO_RESOURCES The graph cannot be scheduled now.
:retval: VX_ERROR_NOT_SUFFICIENT The graph is not verified and has failed
forced verification.
:retval: VX_SUCCESS The graph has been scheduled.
:pre: *vxVerifyGraph* must return *VX_SUCCESS* before this function will pass.
:ingroup: group_graph
    '''
    return lib.vxScheduleGraph(graph)
    
def WaitGraph(graph):
    '''
:brief: Waits for a specific graph to complete. If the graph has been scheduled multiple 
times since the last call to vxWaitGraph, then vxWaitGraph returns only when the last 
scheduled execution completes.
:param: [in] graph The graph to wait on.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS The graph has successfully completed execution and its outputs are the 
valid results of the most recent execution. 
:retval: VX_FAILURE An error occurred or the graph was never scheduled.  Use vxQueryGraph 
for the VX_GRAPH_ATTRIBUTE_STATUS attribute to determine the details.  Output data of the 
graph is undefined. 
:pre: *vxScheduleGraph*
:ingroup: group_graph
    '''
    return lib.vxWaitGraph(graph)
    
def QueryGraph(graph, attribute, ptr, size):
    '''
:brief: Allows the user to query attributes of the Graph.
:param: [in] graph The reference to the created graph.
:param: [in] attribute The *vx_graph_attribute_e* type needed.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_graph
    '''
    return lib.vxQueryGraph(graph, attribute, ptr, size)
    
def SetGraphAttribute(graph, attribute, ptr, size):
    '''
:brief: Allows the set to attributes on the Graph.
:param: [in] graph The reference to the graph.
:param: [in] attribute The *vx_graph_attribute_e* type needed.
:param: [in] ptr The location from which to read the value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_graph
    '''
    return lib.vxSetGraphAttribute(graph, attribute, ptr, size)
    
def AddParameterToGraph(graph, parameter):
    '''
:brief: Adds the given parameter extracted from a *vx_node* to the graph.
:param: [in] graph The graph reference that contains the node.
:param: [in] parameter The parameter reference to add to the graph from the node.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Parameter added to Graph.
:retval: VX_ERROR_INVALID_REFERENCE The parameter is not a valid *vx_parameter*.
:retval: VX_ERROR_INVALID_PARAMETER The parameter is of a node not in this
graph.
:ingroup: group_graph_parameters
    '''
    return lib.vxAddParameterToGraph(graph, parameter)
    
def SetGraphParameterByIndex(graph, index, value):
    '''
:brief: Sets a reference to the parameter on the graph. The implementation
must set this parameter on the originating node as well.
:param: [in] graph The graph reference.
:param: [in] index The parameter index.
:param: [in] value The reference to set to the parameter.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Parameter set to Graph.
:retval: VX_ERROR_INVALID_REFERENCE The value is not a valid *vx_reference*.
:retval: VX_ERROR_INVALID_PARAMETER The parameter index is out of bounds or the
dir parameter is incorrect.
:ingroup: group_graph_parameters
    '''
    return lib.vxSetGraphParameterByIndex(graph, index, value)
    
def GetGraphParameterByIndex(graph, index):
    '''
:brief: Retrieves a *vx_parameter* from a *vx_graph*.
:param: [in] graph The graph.
:param: [in] index The index of the parameter.
:return: *vx_parameter* reference.
:retval: 0 if the index is out of bounds.
:retval:The parameter reference.
:ingroup: group_graph_parameters
    '''
    return lib.vxGetGraphParameterByIndex(graph, index)
    
def IsGraphVerified(graph):
    '''
:brief: Returns a Boolean to indicate the state of graph verification.
:param: [in] graph The reference to the graph to check.
:return: A *vx_bool* value.
:retval: vx_true_e The graph is verified.
:retval: vx_false_e The graph is not verified. It must be verified before
execution either through *vxVerifyGraph* or automatically through
*vxProcessGraph* or *vxScheduleGraph*.
:ingroup: group_graph
    '''
    return lib.vxIsGraphVerified(graph)
    
def CreateGenericNode(graph, kernel):
    '''
:brief: Creates a reference to a node object for a given kernel.
:details: This node has no references assigned as parameters after completion.
The client is then required to set these parameters manually by *vxSetParameterByIndex*.
When clients supply their own node creation functions (for use with User Kernels), this is the API
to use along with the parameter setting API.
:param: [in] graph The reference to the graph in which this node exists.
:param: [in] kernel The kernel reference to associate with this new node.
:returns: A node reference *vx_node*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_adv_node
:post: Call *vxSetParameterByIndex* for as many parameters as needed to be set.
    '''
    return lib.vxCreateGenericNode(graph, kernel)
    
def QueryNode(node, attribute, ptr, size):
    '''
:brief: Allows a user to query information out of a node.
:param: [in] node The reference to the node to query.
:param: [in] attribute Use *vx_node_attribute_e* value to query for information.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytesin bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Successful
:retval: VX_ERROR_INVALID_PARAMETERS The type or size is incorrect.
:ingroup: group_node
    '''
    return lib.vxQueryNode(node, attribute, ptr, size)
    
def SetNodeAttribute(node, attribute, ptr, size):
    '''
:brief: Allows a user to set attribute of a node before Graph Validation.
:param: [in] node The reference to the node to set.
:param: [in] attribute Use *vx_node_attribute_e* value to query for information.
:param: [out] ptr The output pointer to where to send the value.
:param: [in] size The size in bytes of the objects to which :a: ptr points.
:note: Some attributes are inherited from the *vx_kernel*, which was used
to create the node. Some of these can be overridden using this API, notably
VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE and VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR.
:ingroup: group_node
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS The attribute was set.
:retval: VX_ERROR_INVALID_REFERENCE node is not a vx_node.
:retval: VX_ERROR_INVALID_PARAMETER size is not correct for the type needed.
    '''
    return lib.vxSetNodeAttribute(node, attribute, ptr, size)
    
def ReleaseNode(node):
    '''
:brief: Releases a reference to a Node object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] node The pointer to the reference of the node to release.
:ingroup: group_node
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If node is not a *vx_node*.
    '''
    return lib.vxReleaseNode(node)
    
def RemoveNode(node):
    '''
:brief: Removes a Node from its parent Graph and releases it.
:param: [in] node The pointer to the node to remove and release.
:ingroup: group_node
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If node is not a *vx_node*.
    '''
    return lib.vxRemoveNode(node)
    
def AssignNodeCallback(node, callback):
    '''
:brief: Assigns a callback to a node.
If a callback already exists in this node, this function must return an error
and the user may clear the callback by passing a NULL pointer as the callback.
:param: [in] node The reference to the node.
:param: [in] callback The callback to associate with completion of this
specific node.
:warning: This must be used with <b><i>extreme</i></b> caution as it can :e: ruin
optimizations in the power/performance efficiency of a graph.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Callback assigned.
:retval: VX_ERROR_INVALID_REFERENCE The value passed as node was not a *vx_node*.
:ingroup: group_node_callback
    '''
    return lib.vxAssignNodeCallback(node, callback)
    
def RetrieveNodeCallback(node):
    '''
:brief: Retrieves the current node callback function pointer set on the node.
:param: [in] node The reference to the *vx_node* object.
:ingroup: group_node_callback
:return: vx_nodecomplete_f The pointer to the callback function.
:retval: NULL No callback is set.
:retval:The node callback function.
    '''
    return lib.vxRetrieveNodeCallback(node)
    
def GetParameterByIndex(node, index):
    '''
:brief: Retrieves a *vx_parameter* from a *vx_node*.
:param: [in] node The node from which to extract the parameter.
:param: [in] index The index of the parameter to which to get a reference.
:return: *vx_parameter*
:ingroup: group_parameter
    '''
    return lib.vxGetParameterByIndex(node, index)
    
def ReleaseParameter(param):
    '''
:brief: Releases a reference to a parameter object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] param The pointer to the parameter to release.
:ingroup: group_parameter
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If param is not a *vx_parameter*.
    '''
    return lib.vxReleaseParameter(param)
    
def SetParameterByIndex(node, index, value):
    '''
:brief: Sets the specified parameter data for a kernel on the node.
:param: [in] node The node that contains the kernel.
:param: [in] index The index of the parameter desired.
:param: [in] value The reference to the parameter.
:return: A *vx_status_e* enumeration.
:ingroup: group_parameter
:see: vxSetParameterByReference
    '''
    return lib.vxSetParameterByIndex(node, index, value)
    
def SetParameterByReference(parameter, value):
    '''
:brief: Associates a parameter reference and a data reference with a kernel
on a node.
:param: [in] parameter The reference to the kernel parameter.
:param: [in] value The value to associate with the kernel parameter.
:return: A *vx_status_e* enumeration.
:ingroup: group_parameter
:see: vxGetParameterByIndex
    '''
    return lib.vxSetParameterByReference(parameter, value)
    
def QueryParameter(param, attribute, ptr, size):
    '''
:brief: Allows the client to query a parameter to determine its meta-information.
:param: [in] param The reference to the parameter.
:param: [in] attribute The attribute to query. Use a *vx_parameter_attribute_e*.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_parameter
    '''
    return lib.vxQueryParameter(param, attribute, ptr, size)
    
def CreateScalar(context, data_type, ptr):
    '''
:brief: Creates a reference to a scalar object. Also see sub_node_parameters.
:param: [in] context The reference to the system context.
:param: [in] data_type The *vx_type_e* of the scalar. Must be greater than
*VX_TYPE_INVALID* and less than *VX_TYPE_SCALAR_MAX*.
:param: [in] ptr The pointer to the initial value of the scalar.
:ingroup: group_scalar
:returns: A scaler reference *vx_scalar*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
    '''
    return lib.vxCreateScalar(context, data_type, ptr)
    
def ReleaseScalar(scalar):
    '''
:brief: Releases a reference to a scalar object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] scalar The pointer to the scalar to release.
:ingroup: group_scalar
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If scalar is not a *vx_scalar*.
    '''
    return lib.vxReleaseScalar(scalar)
    
def QueryScalar(scalar, attribute, ptr, size):
    '''
:brief: Queries attributes from a scalar.
:param: [in] scalar The scalar object.
:param: [in] attribute The enumeration to query. Use a *vx_scalar_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_scalar
    '''
    return lib.vxQueryScalar(scalar, attribute, ptr, size)
    
def ReadScalarValue(ref, ptr):
    '''
:brief: Gets the scalar value out of a reference.
:note: Use this in conjunction with Query APIs that return references which
should be converted into values.
:ingroup: group_scalar
:param: [in] ref The reference from which to get the scalar value.
:param: [out] ptr An appropriate typed pointer that points to a location to which to copy
the scalar value.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_INVALID_REFERENCE If the ref is not a valid
reference.
:retval: VX_ERROR_INVALID_PARAMETERS If :a: ptr is NULL.
:retval: VX_ERROR_INVALID_TYPE If the type does not match the type in the reference or is a bad value.
    '''
    return lib.vxReadScalarValue(ref, ptr)
    
def WriteScalarValue(ref, ptr):
    '''
:brief: Sets the scalar value in a reference.
:note: Use this in conjunction with Parameter APIs that return references
to parameters that need to be altered.
:ingroup: group_scalar
:param: [in] ref The reference from which to get the scalar value.
:param: [in] ptr An appropriately typed pointer that points to a location to which to copy
the scalar value.
:return: A *vx_status_e* enumeration.
:retval: VX_ERROR_INVALID_REFERENCE If the ref is not a valid
reference.
:retval: VX_ERROR_INVALID_PARAMETERS If :a: ptr is NULL.
:retval: VX_ERROR_INVALID_TYPE If the type does not match the type in the reference or is a bad value.
    '''
    return lib.vxWriteScalarValue(ref, ptr)
    
def QueryReference(ref, attribute, ptr, size):
    '''
:brief: Queries any reference type for some basic information (count, type).
:param: [in] ref The reference to query.
:param: [in] attribute The value for which to query. Use *vx_reference_attribute_e*.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_reference
    '''
    return lib.vxQueryReference(ref, attribute, ptr, size)
    
def QueryDelay(delay, attribute, ptr, size):
    '''
:brief: Queries a *vx_delay* object attribute.
:param: [in] delay A pointer to a delay object.
:param: [in] attribute The attribute to query. Use a *vx_delay_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_delay
    '''
    return lib.vxQueryDelay(delay, attribute, ptr, size)
    
def ReleaseDelay(delay):
    '''
:brief: Releases a reference to a delay object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] delay The pointer to the delay to release.
:post: After returning from this function the reference is zeroed.
:ingroup: group_delay
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If delay is not a *vx_delay*.
    '''
    return lib.vxReleaseDelay(delay)
    
def CreateDelay(context, exemplar, slots):
    '''
:brief: Creates a Delay object.
:details: This function uses a subset of the attributes defining the metadata of 
the exemplar, ignoring the object. It does not alter the exemplar or keep or release 
the reference to the exemplar. For the definition of supported attributes
see vxSetMetaFormatAttribute.

:param: [in] context The reference to the system context.
:param: [in] exemplar The exemplar object.
:param: [in] slots The number of reference in the delay.
:returns: A delay reference *vx_delay*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_delay
    '''
    return lib.vxCreateDelay(context, exemplar, slots)
    
def GetReferenceFromDelay(delay, index):
    '''
:brief: Retrieves a reference from a delay object.
:param: [in] delay The reference to the delay object.
:param: [in] index An index into the delay from which to extract the
reference.
:return: *vx_reference*
:note: The delay index is in the range :f:$ [-count+1,0] :f:$. 0 is always the
:e: current object.
:ingroup: group_delay
:note: A reference from a delay object must not be given to its associated
release API (e.g. *vxReleaseImage*). Use the *vxReleaseDelay* only.
    '''
    return lib.vxGetReferenceFromDelay(delay, index)
    
def AgeDelay(delay):
    '''
:brief: Ages the internal delay ring by one. This means that once this API is
called the reference from index 0 will go to index -1 and so forth until
:f:$ -count+1 :f:$ is reached. This last object will become 0. Once the delay has
been aged, it updates the reference in any associated nodes.
:param: [in] delay
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Delay was aged.
:retval: VX_ERROR_INVALID_REFERENCE The value passed as delay was not a *vx_delay*.
:ingroup: group_delay
    '''
    return lib.vxAgeDelay(delay)
    
def AddLogEntry(ref, status, message):
    '''
:brief: Adds a line to the log.
:param: [in] ref The reference to add the log entry against. Some valid value must be provided.
:param: [in] status The status code. *VX_SUCCESS* status entries are ignored and not added.
:param: [in] message The human readable message to add to the log.
:param: [in] ... a list of variable arguments to the message.
:note: Messages may not exceed *VX_MAX_LOG_MESSAGE_LEN* bytes and will be truncated in the log if they exceed this limit.
:ingroup: group_log
    '''
    return lib.vxAddLogEntry(ref, status, message)
    
def RegisterLogCallback(context, callback, reentrant):
    '''
:brief: Registers a callback facility to the OpenVX implementation to receive error logs.
:param: [in] context The overall context to OpenVX.
:param: [in] callback The callback function. If NULL, the previous callback is removed.
:param: [in] reentrant If reentrancy flag is *vx_true_e*, then the callback may be entered from multiple
simultaneous tasks or threads (if the host OS supports this).
:ingroup: group_log
    '''
    return lib.vxRegisterLogCallback(context, callback, reentrant)
    
def CreateLUT(context, data_type, count):
    '''
:brief: Creates LUT object of a given type.
:param: [in] context The reference to the context.
:param: [in] data_type The type of data stored in the LUT.
:param: [in] count The number of entries desired.
:if: OPENVX_STRICT_1_0
:note: For OpenVX 1.0, count must be equal to 256 and data_type can only be VX_TYPE_UINT8.
:endif:
:returns: An LUT reference *vx_lut*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_lut
    '''
    return lib.vxCreateLUT(context, data_type, count)
    
def ReleaseLUT(lut):
    '''
:brief: Releases a reference to a LUT object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] lut The pointer to the LUT to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If lut is not a *vx_lut*.
:ingroup: group_lut
    '''
    return lib.vxReleaseLUT(lut)
    
def QueryLUT(lut, attribute, ptr, size):
    '''
:brief: Queries attributes from a LUT.
:param: [in] lut The LUT to query.
:param: [in] attribute The attribute to query. Use a *vx_lut_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_lut
    '''
    return lib.vxQueryLUT(lut, attribute, ptr, size)
    
def AccessLUT(lut, ptr, usage):
    '''
:brief: Grants access to a LUT table and increments the object reference count in case of success.
:details: There are several variations of call methodology:
:arg: If :a: ptr is NULL (which means the current data of the LUT is not desired),
the LUT reference count is incremented.
:arg: If :a: ptr is not NULL but (*ptr) is NULL, (*ptr) will contain the address of the LUT data when the function returns and
the reference count will be incremented. Whether the (*ptr) address is mapped
or allocated is undefined. (*ptr) must be returned to *vxCommitLUT*.
:arg: If :a: ptr is not NULL and (*ptr) is not NULL, the user is signalling the implementation to copy the LUT data into the location specified
by (*ptr). Users must use *vxQueryLUT* with *VX_LUT_ATTRIBUTE_SIZE* to
determine how much memory to allocate for the LUT data.

In any case, *vxCommitLUT* must be called after LUT access is complete.
:param: [in] lut The LUT from which to get the data.
:param: [in,out] ptr ptr The user-supplied address to a pointer, via which the requested contents 
are returned.
:arg: If ptr is NULL, an error occurs.
:arg: If ptr is not NULL and (*ptr) is NULL, (*ptr) will be set to the address of a memory area 
managed by the OpenVX framework containing the requested data.
:arg: If both ptr and (*ptr) are not NULL, requested data will be copied to (*ptr) (optionally in 
case of write-only access).
:param: [in] usage This declares the intended usage of the pointer using the*vx_accessor_e* enumeration.
:return: A *vx_status_e* enumeration.
:post: *vxCommitLUT*
:ingroup: group_lut
    '''
    return lib.vxAccessLUT(lut, ptr, usage)
    
def CommitLUT(lut, ptr):
    '''
:brief: Commits the Lookup Table and decrements the object reference count in case of success.
:details: Commits the data back to the LUT object and decrements the reference count.
There are several variations of call methodology:
:arg: If a user should allocated their own memory for the LUT data copy, the user is
obligated to free this memory.
:arg: If :a: ptr is not NULL and the (*ptr) for *vxAccessLUT* was NULL,
it is undefined whether the implementation will unmap or copy and free the memory.
:param: [in] lut The LUT to modify.
:param: [in] ptr The pointer provided or returned by *vxAccessLUT*. This cannot be NULL.
:return: A *vx_status_e* enumeration.
:pre: *vxAccessLUT*.
:ingroup: group_lut
    '''
    return lib.vxCommitLUT(lut, ptr)
    
def CreateDistribution(context, numBins, offset, range):
    '''
:brief: Creates a reference to a 1D Distribution of a consecutive interval [offset, offset + range - 1] 
defined by a start offset and valid range, divided equally into numBins parts.
:param: [in] context The reference to the overall context.
:param: [in] numBins The number of bins in the distribution.
:param: [in] offset The start offset into the range value that marks the begining of the 1D Distribution.
:param: [in] range The total number of the values.
:returns: A distribution reference *vx_distribution*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_distribution
    '''
    return lib.vxCreateDistribution(context, numBins, offset, range)
    
def ReleaseDistribution(distribution):
    '''
:brief: Releases a reference to a distribution object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] distribution The reference to the distribution to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If distribution is not a *vx_distribution*.
:ingroup: group_distribution
    '''
    return lib.vxReleaseDistribution(distribution)
    
def QueryDistribution(distribution, attribute, ptr, size):
    '''
:brief: Queries a Distribution object.
:param: [in] distribution The reference to the distribution to query.
:param: [in] attribute The attribute to query. Use a *vx_distribution_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_distribution
    '''
    return lib.vxQueryDistribution(distribution, attribute, ptr, size)
    
def AccessDistribution(distribution, ptr, usage):
    '''
:brief: Grants access to a distribution object and increments the object reference count in 
case of success.
:param: [in] distribution The reference to the distribution to access.
:param: [in, out] ptr The user-supplied address to a pointer, via which the requested contents 
are returned.
:arg: If ptr is NULL, an error occurs.
:arg: If ptr is not NULL and (*ptr) is NULL, (*ptr) will be set to the address of a memory area 
managed by the OpenVX framework containing the requested data.
:arg: If both ptr and (*ptr) are not NULL, requested data will be copied to (*ptr) (optionally in 
case of write-only access).
:param: [in] usage The *vx_accessor_e* value to describe the access of the object.
:return: A *vx_status_e* enumeration.
:post: *vxCommitDistribution*
:ingroup: group_distribution
    '''
    return lib.vxAccessDistribution(distribution, ptr, usage)
    
def CommitDistribution(distribution, ptr):
    '''
:brief: Commits the distribution objec> and decrements the object reference count in case of success. 
The memory must be a vx_uint32 array of a value at least as big as the value returned via 
*VX_DISTRIBUTION_ATTRIBUTE_BINS*.
:param: [in] distribution The Distribution to modify.
:param: [in] ptr The pointer provided or returned by *vxAccessDistribution*. The ptr cannot
be NULL.
:return: A *vx_status_e* enumeration.
:pre: *vxAccessDistribution*.
:ingroup: group_distribution
    '''
    return lib.vxCommitDistribution(distribution, ptr)
    
def CreateThreshold(c, thresh_type, data_type):
    '''
:brief: Creates a reference to a threshold object of a given type.
:param: [in] c The reference to the overall context.
:param: [in] thresh_type The type of threshold to create.
:param: [in] data_type The data type of the threshold's value(s).
:if: OPENVX_STRICT_1_0
:note: For OpenVX 1.0, data_type can only be *VX_TYPE_UINT8*.
:endif:
:returns: An threshold reference *vx_threshold*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_threshold
    '''
    return lib.vxCreateThreshold(c, thresh_type, data_type)
    
def ReleaseThreshold(thresh):
    '''
:brief: Releases a reference to a threshold object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] thresh The pointer to the threshold to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If thresh is not a *vx_threshold*.
:ingroup: group_threshold
    '''
    return lib.vxReleaseThreshold(thresh)
    
def SetThresholdAttribute(thresh, attribute, ptr, size):
    '''
:brief: Sets attributes on the threshold object.
:param: [in] thresh The threshold object to set.
:param: [in] attribute The attribute to modify. Use a *vx_threshold_attribute_e* enumeration.
:param: [in] ptr The pointer to the value to which to set the attribute.
:param: [in] size The size of the data pointed to by :a: ptr.
:return: A *vx_status_e* enumeration.
:ingroup: group_threshold
    '''
    return lib.vxSetThresholdAttribute(thresh, attribute, ptr, size)
    
def QueryThreshold(thresh, attribute, ptr, size):
    '''
:brief: Queries an attribute on the threshold object.
:param: [in] thresh The threshold object to set.
:param: [in] attribute The attribute to query. Use a *vx_threshold_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_threshold
    '''
    return lib.vxQueryThreshold(thresh, attribute, ptr, size)
    
def CreateMatrix(c, data_type, columns, rows):
    '''
:brief: Creates a reference to a matrix object.
:param: [in] c The reference to the overall context.
:param: [in] data_type The unit format of the matrix. *VX_TYPE_INT32* or *VX_TYPE_FLOAT32*.
:param: [in] columns The first dimensionality.
:param: [in] rows The second dimensionality.
:returns: An matrix reference *vx_matrix*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_matrix
    '''
    return lib.vxCreateMatrix(c, data_type, columns, rows)
    
def ReleaseMatrix(mat):
    '''
:brief: Releases a reference to a matrix object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] mat The matrix reference to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If mat is not a *vx_matrix*.
:ingroup: group_matrix
    '''
    return lib.vxReleaseMatrix(mat)
    
def QueryMatrix(mat, attribute, ptr, size):
    '''
:brief: Queries an attribute on the matrix object.
:param: [in] mat The matrix object to set.
:param: [in] attribute The attribute to query. Use a *vx_matrix_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_matrix
    '''
    return lib.vxQueryMatrix(mat, attribute, ptr, size)
    
def ReadMatrix(mat, array):
    '''
:brief: Gets the matrix data (copy).
:param: [in] mat The reference to the matrix.
:param: [out] array The array in which to place the matrix.
:see: vxQueryMatrix and *VX_MATRIX_ATTRIBUTE_COLUMNS* and *VX_MATRIX_ATTRIBUTE_ROWS*
to get the needed number of elements of the array.
:return: A *vx_status_e* enumeration.
:ingroup: group_matrix
    '''
    return lib.vxReadMatrix(mat, array)
    
def WriteMatrix(mat, array):
    '''
:brief: Sets the matrix data (copy)
:param: [in] mat The reference to the matrix.
:param: [in] array The array containing the matrix to be written.
:see: vxQueryMatrix and *VX_MATRIX_ATTRIBUTE_COLUMNS* and *VX_MATRIX_ATTRIBUTE_ROWS*
to get the needed number of elements of the array.'
:return: A *vx_status_e* enumeration.
:ingroup: group_matrix
    '''
    return lib.vxWriteMatrix(mat, array)
    
def CreateConvolution(context, columns, rows):
    '''
:brief: Creates a reference to a convolution matrix object.
:param: [in] context The reference to the overall context.
:param: [in] columns The columns dimension of the convolution.
Must be odd and greater than or equal to 3 and less than the value returned
from *VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION*.
:param: [in] rows The rows dimension of the convolution.
Must be odd and greater than or equal to 3 and less than the value returned
from *VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION*.
:returns: A convolution reference *vx_convolution*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_convolution
    '''
    return lib.vxCreateConvolution(context, columns, rows)
    
def ReleaseConvolution(conv):
    '''
:brief: Releases the reference to a convolution matrix.
The object may not be garbage collected until its total reference count is zero.
:param: [in] conv The pointer to the convolution matrix to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If conv is not a *vx_convolution*.
:ingroup: group_convolution
    '''
    return lib.vxReleaseConvolution(conv)
    
def QueryConvolution(conv, attribute, ptr, size):
    '''
:brief: Queries an attribute on the convolution matrix object.
:param: [in] conv The convolution matrix object to set.
:param: [in] attribute The attribute to query. Use a *vx_convolution_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_convolution
    '''
    return lib.vxQueryConvolution(conv, attribute, ptr, size)
    
def SetConvolutionAttribute(conv, attribute, ptr, size):
    '''
:brief: Sets attributes on the convolution object.
:param: [in] conv The coordinates object to set.
:param: [in] attribute The attribute to modify. Use a *vx_convolution_attribute_e* enumeration.
:param: [in] ptr The pointer to the value to which to set the attribute.
:param: [in] size The size in bytes of the data pointed to by :a: ptr.
:return: A *vx_status_e* enumeration.
:ingroup: group_convolution
    '''
    return lib.vxSetConvolutionAttribute(conv, attribute, ptr, size)
    
def ReadConvolutionCoefficients(conv, array):
    '''
:brief: Gets the convolution data (copy).
:param: [in] conv The reference to the convolution.
:param: [out] array The array to place the convolution.
:see: vxQueryConvolution and *VX_CONVOLUTION_ATTRIBUTE_SIZE* to get the
needed number of bytes of the array.
:return: A *vx_status_e* enumeration.
:ingroup: group_convolution
    '''
    return lib.vxReadConvolutionCoefficients(conv, array)
    
def WriteConvolutionCoefficients(conv, array):
    '''
:brief: Sets the convolution data (copy)
:param: [in] conv The reference to the convolution.
:param: [in] array The array containing the convolution to be written.
:see: *vxQueryConvolution* and *VX_CONVOLUTION_ATTRIBUTE_SIZE* to get the
needed number of bytes of the array.
:return: A *vx_status_e* enumeration.
:ingroup: group_convolution
    '''
    return lib.vxWriteConvolutionCoefficients(conv, array)
    
def CreatePyramid(context, levels, scale, width, height, format):
    '''
:brief: Creates a reference to a pyramid object of the supplied number of levels.
:param: [in] context The reference to the overall context.
:param: [in] levels The number of levels desired. This is required to be a non-zero value.
:param: [in] scale Used to indicate the scale between pyramid levels. This is required to be a non-zero positive value.
:if: OPENVX_STRICT_1_0
In OpenVX 1.0, the only permissible values are *VX_SCALE_PYRAMID_HALF* or *VX_SCALE_PYRAMID_ORB*.
:endif:
:param: [in] width The width of the 0th level image in pixels.
:param: [in] height The height of the 0th level image in pixels.
:param: [in] format The format of all images in the pyramid. NV12, NV21, IYUV, UYVY and YUYV formats are not supported.
:returns: A pyramid reference *vx_pyramid* to the sub-image. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:ingroup: group_pyramid
    '''
    return lib.vxCreatePyramid(context, levels, scale, width, height, format)
    
def CreateVirtualPyramid(graph, levels, scale, width, height, format):
    '''
:brief: Creates a reference to a virtual pyramid object of the supplied number of levels.
:details: Virtual Pyramids can be used to connect Nodes together when the contents of the pyramids will
not be accessed by the user of the API.
All of the following constructions are valid:
:code:
vx_context context = vxCreateContext();
vx_graph graph = vxCreateGraph(context);
vx_pyramid virt[] = {
    vxCreateVirtualPyramid(graph, 4, VX_SCALE_PYRAMID_HALF, 0, 0, VX_DF_IMAGE_VIRT), // no dimension and format specified for level 0
    vxCreateVirtualPyramid(graph, 4, VX_SCALE_PYRAMID_HALF, 640, 480, VX_DF_IMAGE_VIRT), // no format specified.
    vxCreateVirtualPyramid(graph, 4, VX_SCALE_PYRAMID_HALF, 640, 480, VX_DF_IMAGE_U8), // no access
};
:endcode:
:param: [in] graph The reference to the parent graph.
:param: [in] levels The number of levels desired. This is required to be a non-zero value.
:param: [in] scale Used to indicate the scale between pyramid levels. This is required to be a non-zero positive value.
:if: OPENVX_STRICT_1_0
In OpenVX 1.0, the only permissible values are *VX_SCALE_PYRAMID_HALF* or *VX_SCALE_PYRAMID_ORB*.
:endif:
:param: [in] width The width of the 0th level image in pixels. This may be set to zero to indicate to the interface that the value is unspecified.
:param: [in] height The height of the 0th level image in pixels. This may be set to zero to indicate to the interface that the value is unspecified.
:param: [in] format The format of all images in the pyramid. This may be set to *VX_DF_IMAGE_VIRT* to indicate that the format is unspecified.
:returns: A pyramid reference *vx_pyramid*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
:note: Images extracted with *vxGetPyramidLevel* behave as Virtual Images and
cause *vxAccessImagePatch* to return errors.
:ingroup: group_pyramid
    '''
    return lib.vxCreateVirtualPyramid(graph, levels, scale, width, height, format)
    
def ReleasePyramid(pyr):
    '''
:brief: Releases a reference to a pyramid object.
The object may not be garbage collected until its total reference count is zero.
:param: [in] pyr The pointer to the pyramid to release.
:ingroup: group_pyramid
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If pyr is not a *vx_pyramid*.
:post: After returning from this function the reference is zeroed.
    '''
    return lib.vxReleasePyramid(pyr)
    
def QueryPyramid(pyr, attribute, ptr, size):
    '''
:brief: Queries an attribute from an image pyramid.
:param: [in] pyr The pyramid to query.
:param: [in] attribute The attribute for which to query. Use a *vx_pyramid_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_pyramid
    '''
    return lib.vxQueryPyramid(pyr, attribute, ptr, size)
    
def GetPyramidLevel(pyr, index):
    '''
:brief: Retrieves a level of the pyramid as a *vx_image*, which can be used
elsewhere in OpenVX. A call to vxReleaseImage is necessary to release an image for each 
call of vxGetPyramidLevel.
:param: [in] pyr The pyramid object.
:param: [in] index The index of the level, such that index is less than levels.
:return: A *vx_image* reference.
:retval: 0 Indicates that the index or the object is invalid.
:ingroup: group_pyramid
    '''
    return lib.vxGetPyramidLevel(pyr, index)
    
def CreateRemap(context, src_width, src_height, dst_width, dst_height):
    '''
:brief: Creates a remap table object.
:param: [in] context The reference to the overall context.
:param: [in] src_width Width of the source image in pixel.
:param: [in] src_height Height of the source image in pixels.
:param: [in] dst_width Width of the destination image in pixels.
:param: [in] dst_height Height of the destination image in pixels.
:ingroup: group_remap
:returns: A remap reference *vx_remap*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.
    '''
    return lib.vxCreateRemap(context, src_width, src_height, dst_width, dst_height)
    
def ReleaseRemap(table):
    '''
:brief: Releases a reference to a remap table object. The object may not be
garbage collected until its total reference count is zero.
:param: [in] table The pointer to the remap table to release.
:post: After returning from this function the reference is zeroed.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If table is not a *vx_remap*.
:ingroup: group_remap
    '''
    return lib.vxReleaseRemap(table)
    
def SetRemapPoint(table, dst_x, dst_y, src_x, src_y):
    '''
:brief: Assigns a destination pixel mapping to the source pixel.
:param: [in] table The remap table reference.
:param: [in] dst_x The destination x coordinate.
:param: [in] dst_y The destination y coordinate.
:param: [in] src_x The source x coordinate in float representation to allow interpolation.
:param: [in] src_y The source y coordinate in float representation to allow interpolation.
:ingroup: group_remap
:return: A *vx_status_e* enumeration.
    '''
    return lib.vxSetRemapPoint(table, dst_x, dst_y, src_x, src_y)
    
def GetRemapPoint(table, dst_x, dst_y, src_x, src_y):
    '''
:brief: Retrieves the source pixel point from a destination pixel.
:param: [in] table The remap table reference.
:param: [in] dst_x The destination x coordinate.
:param: [in] dst_y The destination y coordinate.
:param: [out] src_x The pointer to the location to store the source x coordinate in float representation to allow interpolation.
:param: [out] src_y The pointer to the location to store the source y coordinate in float representation to allow interpolation.
:ingroup: group_remap
:return: A *vx_status_e* enumeration.
    '''
    return lib.vxGetRemapPoint(table, dst_x, dst_y, src_x, src_y)
    
def QueryRemap(r, attribute, ptr, size):
    '''
:brief: Queries attributes from a Remap table.
:param: [in] r The remap to query.
:param: [in] attribute The attribute to query. Use a *vx_remap_attribute_e* enumeration.
:param: [out] ptr The location at which to store the resulting value.
:param: [in] size The size in bytes of the container to which :a: ptr points.
:return: A *vx_status_e* enumeration.
:ingroup: group_remap
    '''
    return lib.vxQueryRemap(r, attribute, ptr, size)
    
def CreateArray(context, item_type, capacity):
    '''
:brief: Creates a reference to an Array object.

User must specify the Array capacity (i.e., the maximal number of items that the array can hold).

:param: [in] context      The reference to the overall Context.
:param: [in] item_type    The type of objects to hold. Use:
                         :arg: *VX_TYPE_RECTANGLE* for *vx_rectangle_t*.
                         :arg: *VX_TYPE_KEYPOINT* for *vx_keypoint_t*.
                         :arg: *VX_TYPE_COORDINATES2D* for *vx_coordinates2d_t*.
                         :arg: *VX_TYPE_COORDINATES3D* for *vx_coordinates3d_t*.
                         :arg: *vx_enum* Returned from *vxRegisterUserStruct*.
:param: [in] capacity     The maximal number of items that the array can hold.

:returns: An array reference *vx_array*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.

:ingroup: group_array
    '''
    return lib.vxCreateArray(context, item_type, capacity)
    
def CreateVirtualArray(graph, item_type, capacity):
    '''
:brief: Creates an opaque reference to a virtual Array with no direct user access.

Virtual Arrays are useful when item type or capacity are unknown ahead of time
and the Array is used as internal graph edge. Virtual arrays are scoped within the parent graph only.

All of the following constructions are allowed.
:code:
vx_context context = vxCreateContext();
vx_graph graph = vxCreateGraph(context);
vx_array virt[] = {
    vxCreateVirtualArray(graph, 0, 0), // totally unspecified
    vxCreateVirtualArray(graph, VX_TYPE_KEYPOINT, 0), // unspecified capacity
    vxCreateVirtualArray(graph, VX_TYPE_KEYPOINT, 1000), // no access
};
:endcode:

:param: [in] graph        The reference to the parent graph.
:param: [in] item_type    The type of objects to hold.
                         This may to set to zero to indicate an unspecified item type.
:param: [in] capacity     The maximal number of items that the array can hold.
                         This may be to set to zero to indicate an unspecified capacity.
:see: vxCreateArray for a type list.
:returns: A array reference *vx_array*. Any possible errors preventing a 
successful creation should be checked using *vxGetStatus*.

:ingroup: group_array
    '''
    return lib.vxCreateVirtualArray(graph, item_type, capacity)
    
def ReleaseArray(arr):
    '''
:brief: Releases a reference of an Array object.
The object may not be garbage collected until its total reference count is zero.
After returning from this function the reference is zeroed.
:param: [in] arr          The pointer to the Array to release.
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS No errors.
:retval: VX_ERROR_INVALID_REFERENCE If arr is not a *vx_array*.
:ingroup: group_array
    '''
    return lib.vxReleaseArray(arr)
    
def QueryArray(arr, attribute, ptr, size):
    '''
:brief: Queries the Array for some specific information.

:param: [in] arr          The reference to the Array.
:param: [in] attribute    The attribute to query. Use a *vx_array_attribute_e*.
:param: [out] ptr         The location at which to store the resulting value.
:param: [in] size         The size in bytes of the container to which :a: ptr points.

:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS                   No errors.
:retval: VX_ERROR_INVALID_REFERENCE   If the :a: arr is not a *vx_array*.
:retval: VX_ERROR_NOT_SUPPORTED       If the :a: attribute is not a value supported on this implementation.
:retval: VX_ERROR_INVALID_PARAMETERS  If any of the other parameters are incorrect.

:ingroup: group_array
    '''
    return lib.vxQueryArray(arr, attribute, ptr, size)
    
def AddArrayItems(arr, count, ptr, stride):
    '''
:brief: Adds items to the Array.

This function increases the container size.

By default, the function does not reallocate memory,
so if the container is already full (number of elements is equal to capacity)
or it doesn't have enough space,
the function returns *VX_FAILURE* error code.

:param: [in] arr          The reference to the Array.
:param: [in] count        The total number of elements to insert.
:param: [in] ptr          The location at which to store the input values.
:param: [in] stride       The number of bytes between the beginning of two consecutive elements.

:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS                   No errors.
:retval: VX_ERROR_INVALID_REFERENCE   If the :a: arr is not a *vx_array*.
:retval: VX_FAILURE                   If the Array is full.
:retval: VX_ERROR_INVALID_PARAMETERS  If any of the other parameters are incorrect.

:ingroup: group_array
    '''
    return lib.vxAddArrayItems(arr, count, ptr, stride)
    
def TruncateArray(arr, new_num_items):
    '''
:brief: Truncates an Array (remove items from the end).

:param: [in,out] arr          The reference to the Array.
:param: [in] new_num_items    The new number of items for the Array.

:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS                   No errors.
:retval: VX_ERROR_INVALID_REFERENCE   If the :a: arr is not a *vx_array*.
:retval: VX_ERROR_INVALID_PARAMETERS  The :a: new_size is greater than the current size.

:ingroup: group_array
    '''
    return lib.vxTruncateArray(arr, new_num_items)
    
def AccessArrayRange(arr, start, end, stride, ptr, usage):
    '''
:brief: Grants access to a sub-range of an Array. The number of elements in the sub-range is given by (end - start).

:param: [in] arr          The reference to the Array.
:param: [in] start        The start index.
:param: [in] end          The end index. (end - start) elements are accessed from start.
:param: [in, out] stride  A pointer to 'number of bytes' between the beginning of two consequent 
elements. 
:arg: Input case: ptr is a pointer to a non-NULL pointer. The stride parameter must be the address 
of a vx_size scalar that describes how the user will access the requested array data at address 
(*ptr).
:arg: Output Case: ptr is a pointer to a NULL pointer. The function fills the vx_size scalar 
pointed by stride with the element stride information that the user must consult to access the 
array elements at address (*ptr).
:param: [out] ptr        A pointer to a pointer to a location to store the requested data.
:arg: Input Case: ptr is a pointer to a non-NULL pointer to a valid buffer. This buffer will be 
used in one of two ways, depending on the value of the usage parameter. If usage is 
VX_WRITE_ONLY, then the buffer must contain element data that the user wants to replace the 
array's element data with. Otherwise (i.e., usage is not VX_WRITE_ONLY), the array's current 
element data will be written to the memory starting at address (*ptr) as storage memory for the 
access request. The caller must ensure enough memory has been allocated for the requested array 
range with the requested stride.
:arg: Output Case: ptr is a pointer to a NULL pointer.  This NULL pointer will be overwritten with 
a pointer to the address where the requested data can be accessed. (*ptr) must eventually be provided 
as the ptr parameter of a call to vxCommitArrayRange. 
:param: [in] usage        This declares the intended usage of the pointer using the *vx_accessor_e* enumeration.

:note: The stride and ptr parameters must both be input, or both be output, otherwise the behavior 
is undefined.

:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS                   No errors.
:retval: VX_ERROR_OPTIMIZED_AWAY      If the reference is a virtual array and cannot be accessed or committed.
:retval: VX_ERROR_INVALID_REFERENCE   If the :a: arr is not a *vx_array*.
:retval: VX_ERROR_INVALID_PARAMETERS  If any of the other parameters are incorrect.
:post: *vxCommitArrayRange*
:ingroup: group_array
    '''
    return lib.vxAccessArrayRange(arr, start, end, stride, ptr, usage)
    
def CommitArrayRange(arr, start, end, ptr):
    '''
:brief: Commits data back to the Array object.

:details: This allows a user to commit data to a sub-range of an Array. The number of elements in the sub-range is given by (end - start).

:param: [in] arr          The reference to the Array.
:param: [in] start        The start index.
:param: [in] end          The end index. (end - start) elements are accessed from start.
:param: [in] ptr          The user supplied pointer.

:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS                   No errors.
:retval: VX_ERROR_OPTIMIZED_AWAY      If the reference is a virtual array and cannot be accessed or committed.
:retval: VX_ERROR_INVALID_REFERENCE   If the :a: arr is not a *vx_array*.
:retval: VX_ERROR_INVALID_PARAMETERS  If any of the other parameters are incorrect.

:ingroup: group_array
    '''
    return lib.vxCommitArrayRange(arr, start, end, ptr)
    
def SetMetaFormatAttribute(meta, attribute, ptr, size):
    '''
:brief: This function allows a user to set the attributes of a *vx_meta_format* object in a kernel output validator.

The vx_meta_format object contains two types of information : data object meta data and 
some specific information that defines how the valid region of an image changes

The meta data attributes that can be set are identified by this list:
- vx_image : VX_IMAGE_ATTRIBUTE_FORMAT, VX_IMAGE_ATTRIBUTE_HEIGHT, VX_IMAGE_ATTRIBUTE_WIDTH
- vx_array : VX_ARRAY_ATTRIBUTE_CAPACITY, VX_ARRAY_ATTRIBUTE_ITEMTYPE
- vx_pyramid : VX_PYRAMID_ATTRIBUTE_FORMAT, VX_PYRAMID_ATTRIBUTE_HEIGHT, VX_PYRAMID_ATTRIBUTE_WIDTH, VX_PYRAMID_ATTRIBUTE_LEVELS, VX_PYRAMID_ATTRIBUTE_SCALE
- vx_scalar : VX_SCALAR_ATTRIBUTE_TYPE
- vx_matrix : VX_MATRIX_ATTRIBUTE_TYPE, VX_MATRIX_ATTRIBUTE_ROWS, VX_MATRIX_ATTRIBUTE_COLUMNS
- vx_distribution : VX_DISTRIBUTION_ATTRIBUTE_BINS, VX_DISTRIBUTION_ATTRIBUTE_OFFSET, VX_DISTRIBUTION_ATTRIBUTE_RANGE
- vx_remap : VX_REMAP_ATTRIBUTE_SOURCE_WIDTH, VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT, VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH, VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT
- vx_lut : VX_LUT_ATTRIBUTE_TYPE, VX_LUT_ATTRIBUTE_COUNT
- vx_threshold : VX_THRESHOLD_ATTRIBUTE_TYPE
- VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE
:note: For vx_image, a specific attribute can be used to specify the valid region evolution. This information is not a meta data.

:param: [in] meta The reference to the vx_meta_format struct to set 
:param: [in] attribute Use the subset of data object attributes that define the meta data of this object or attributes from *vx_meta_format_attribute_e*.
:param: [in] ptr The input pointer of the value to set on the meta format object.
:param: [in] size The size in bytes of the object to which :a: ptr points.
:ingroup: group_user_kernels
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS The attribute was set.
:retval: VX_ERROR_INVALID_REFERENCE meta was not a *vx_meta_format*.
:retval: VX_ERROR_INVALID_PARAMETER size was not correct for the type needed.
:retval: VX_ERROR_NOT_SUPPORTED the object attribute was not supported on the meta format object.
:retval: VX_ERROR_INVALID_TYPE attribute type did not match known meta format type.
    '''
    return lib.vxSetMetaFormatAttribute(meta, attribute, ptr, size)
    
def ColorConvertNode(graph, input, output):
    '''
:brief: [Graph] Creates a color conversion node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image from which to convert.
:param: [out] output The output image to which to convert.
:see: *VX_KERNEL_COLOR_CONVERT*
:ingroup: group_vision_function_colorconvert
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxColorConvertNode(graph, input, output)
    
def ChannelExtractNode(graph, input, channel, output):
    '''
:brief: [Graph] Creates a channel extract node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image. Must be one of the defined vx_df_image_e multi-planar formats.
:param: [in] channel The *vx_channel_e* channel to extract.
:param: [out] output The output image. Must be *VX_DF_IMAGE_U8*.
*:see: VX_KERNEL_CHANNEL_EXTRACT*
:ingroup: group_vision_function_channelextract
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxChannelExtractNode(graph, input, channel, output)
    
def ChannelCombineNode(graph, plane0, plane1, plane2, plane3, output):
    '''
:brief: [Graph] Creates a channel combine node.
:param: [in] graph The graph reference.
:param: [in] plane0 The plane that forms channel 0. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane1 The plane that forms channel 1. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane2 [optional] The plane that forms channel 2. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane3 [optional] The plane that forms channel 3. Must be *VX_DF_IMAGE_U8*.
:param: [out] output The output image. The format of the image must be defined, even if the image is virtual.
:see: *VX_KERNEL_CHANNEL_COMBINE*
:ingroup: group_vision_function_channelcombine
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxChannelCombineNode(graph, plane0, plane1, plane2, plane3, output)
    
def PhaseNode(graph, grad_x, grad_y, orientation):
    '''
:brief: [Graph] Creates a Phase node.
:param: [in] graph The reference to the graph.
:param: [in] grad_x The input x image. This must be in *VX_DF_IMAGE_S16* format.
:param: [in] grad_y The input y image. This must be in *VX_DF_IMAGE_S16* format.
:param: [out] orientation The phase image. This is in *VX_DF_IMAGE_U8* format.
:see: *VX_KERNEL_PHASE*
:ingroup: group_vision_function_phase
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxPhaseNode(graph, grad_x, grad_y, orientation)
    
def Sobel3x3Node(graph, input, output_x, output_y):
    '''
:brief: [Graph] Creates a Sobel3x3 node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output_x [optional] The output gradient in the x direction in *VX_DF_IMAGE_S16*.
:param: [out] output_y [optional] The output gradient in the y direction in *VX_DF_IMAGE_S16*.
:see: *VX_KERNEL_SOBEL_3x3*
:ingroup: group_vision_function_sobel3x3
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxSobel3x3Node(graph, input, output_x, output_y)
    
def MagnitudeNode(graph, grad_x, grad_y, mag):
    '''
:brief: [Graph] Create a Magnitude node.
:param: [in] graph The reference to the graph.
:param: [in] grad_x The input x image. This must be in *VX_DF_IMAGE_S16* format.
:param: [in] grad_y The input y image. This must be in *VX_DF_IMAGE_S16* format.
:param: [out] mag The magnitude image. This is in *VX_DF_IMAGE_S16* format.
:see: *VX_KERNEL_MAGNITUDE*
:ingroup: group_vision_function_magnitude
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxMagnitudeNode(graph, grad_x, grad_y, mag)
    
def ScaleImageNode(graph, src, dst, type):
    '''
:brief: [Graph] Creates a Scale Image Node.
:param: [in] graph The reference to the graph.
:param: [in] src The source image of type *VX_DF_IMAGE_U8*.
:param: [out] dst The destination image of type *VX_DF_IMAGE_U8*.
:param: [in] type The interpolation type to use. :see: vx_interpolation_type_e.
:ingroup: group_vision_function_scale_image
:note: The destination image must have a defined size and format. Only 
 *VX_NODE_ATTRIBUTE_BORDER_MODE* value *VX_BORDER_MODE_UNDEFINED*, 
 *VX_BORDER_MODE_REPLICATE* or *VX_BORDER_MODE_CONSTANT* is supported.
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxScaleImageNode(graph, src, dst, type)
    
def TableLookupNode(graph, input, lut, output):
    '''
:brief: [Graph] Creates a Table Lookup node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8*.
:param: [in] lut The LUT which is of type *VX_TYPE_UINT8*.
:param: [out] output The output image of type *VX_DF_IMAGE_U8*.
:ingroup: group_vision_function_lut
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxTableLookupNode(graph, input, lut, output)
    
def HistogramNode(graph, input, distribution):
    '''
:brief: [Graph] Creates a Histogram node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8*.
:param: [out] distribution The output distribution.
:ingroup: group_vision_function_histogram
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxHistogramNode(graph, input, distribution)
    
def EqualizeHistNode(graph, input, output):
    '''
:brief: [Graph] Creates a Histogram Equalization node.
:param: [in] graph The reference to the graph.
:param: [in] input The grayscale input image in *VX_DF_IMAGE_U8*.
:param: [out] output The grayscale output image of type *VX_DF_IMAGE_U8* with equalized brightness and contrast.
:ingroup: group_vision_function_equalize_hist
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxEqualizeHistNode(graph, input, output)
    
def AbsDiffNode(graph, in1, in2, out):
    '''
:brief: [Graph] Creates an AbsDiff node.
:param: [in] graph The reference to the graph.
:param: [in] in1 An input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [in] in2 An input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [out] out The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_absdiff
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAbsDiffNode(graph, in1, in2, out)
    
def MeanStdDevNode(graph, input, mean, stddev):
    '''
:brief: [Graph] Creates a mean value and standard deviation node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image. *VX_DF_IMAGE_U8* is supported.
:param: [out] mean The *VX_TYPE_FLOAT32* average pixel value.
:param: [out] stddev The *VX_TYPE_FLOAT32* standard deviation of the pixel values.
:ingroup: group_vision_function_meanstddev
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxMeanStdDevNode(graph, input, mean, stddev)
    
def ThresholdNode(graph, input, thresh, output):
    '''
:brief: [Graph] Creates a Threshold node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image. *VX_DF_IMAGE_U8* is supported.
:param: [in] thresh The thresholding object that defines the parameters of
the operation.
:param: [out] output The output Boolean image. Values are either 0 or 255.
:ingroup: group_vision_function_threshold
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxThresholdNode(graph, input, thresh, output)
    
def IntegralImageNode(graph, input, output):
    '''
:brief: [Graph] Creates an Integral Image Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U32* format.
:ingroup: group_vision_function_integral_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxIntegralImageNode(graph, input, output)
    
def Erode3x3Node(graph, input, output):
    '''
:brief: [Graph] Creates an Erosion Image Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_erode_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxErode3x3Node(graph, input, output)
    
def Dilate3x3Node(graph, input, output):
    '''
:brief: [Graph] Creates a Dilation Image Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_dilate_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxDilate3x3Node(graph, input, output)
    
def Median3x3Node(graph, input, output):
    '''
:brief: [Graph] Creates a Median Image Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_median_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxMedian3x3Node(graph, input, output)
    
def Box3x3Node(graph, input, output):
    '''
:brief: [Graph] Creates a Box Filter Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_box_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxBox3x3Node(graph, input, output)
    
def Gaussian3x3Node(graph, input, output):
    '''
:brief: [Graph] Creates a Gaussian Filter Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_gaussian_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxGaussian3x3Node(graph, input, output)
    
def ConvolveNode(graph, input, conv, output):
    '''
:brief: [Graph] Creates a custom convolution node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [in] conv The vx_int16 convolution matrix.
:param: [out] output The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_custom_convolution
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxConvolveNode(graph, input, conv, output)
    
def GaussianPyramidNode(graph, input, gaussian):
    '''
:brief: [Graph] Creates a node for a Gaussian Image Pyramid.
:param: [in] graph The reference to the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] gaussian The Gaussian pyramid with *VX_DF_IMAGE_U8* to construct.
:ingroup: group_vision_function_gaussian_pyramid
:see: group_pyramid
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxGaussianPyramidNode(graph, input, gaussian)
    
def AccumulateImageNode(graph, input, accum):
    '''
:brief: [Graph] Creates an accumulate node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in,out] accum The accumulation image in *VX_DF_IMAGE_S16*.
:ingroup: group_vision_function_accumulate
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAccumulateImageNode(graph, input, accum)
    
def AccumulateWeightedImageNode(graph, input, alpha, accum):
    '''
:brief: [Graph] Creates a weighted accumulate node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] alpha The input *VX_TYPE_FLOAT32* scalar value with a value in the range of :f:$ 0.0 :le: :alpha: :le: 1.0 :f:$.
:param: [in,out] accum The *VX_DF_IMAGE_U8* accumulation image.
:ingroup: group_vision_function_accumulate_weighted
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAccumulateWeightedImageNode(graph, input, alpha, accum)
    
def AccumulateSquareImageNode(graph, input, shift, accum):
    '''
:brief: [Graph] Creates an accumulate square node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] shift The input *VX_TYPE_UINT32* with a value in the range of :f:$ 0 :le: shift :le: 15 :f:$.
:param: [in,out] accum The accumulation image in *VX_DF_IMAGE_S16*.
:ingroup: group_vision_function_accumulate_square
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAccumulateSquareImageNode(graph, input, shift, accum)
    
def MinMaxLocNode(graph, input, minVal, maxVal, minLoc, maxLoc, minCount, maxCount):
    '''
:brief: [Graph] Creates a min,max,loc node.
:param: [in] graph The reference to create the graph.
:param: [in] input The input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [out] minVal The minimum value in the image, which corresponds to the type of the input.
:param: [out] maxVal The maximum value in the image, which corresponds to the type of the input.
:param: [out] minLoc The minimum *VX_TYPE_COORDINATES2D* locations (optional). If the input image has several minimums, the kernel will return up to the capacity of the array.
:param: [out] maxLoc The maximum *VX_TYPE_COORDINATES2D* locations (optional). If the input image has several maximums, the kernel will return up to the capacity of the array.
:param: [out] minCount The total number of detected minimums in image (optional). Use a *VX_TYPE_UINT32* scalar.
:param: [out] maxCount The total number of detected maximums in image (optional). Use a *VX_TYPE_UINT32* scalar.
:ingroup: group_vision_function_minmaxloc
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxMinMaxLocNode(graph, input, minVal, maxVal, minLoc, maxLoc, minCount, maxCount)
    
def AndNode(graph, in1, in2, out):
    '''
:brief: [Graph] Creates a bitwise AND node.
:param: [in] graph The reference to the graph.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image.
:param: [in] in2 A *VX_DF_IMAGE_U8* input image.
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_and
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAndNode(graph, in1, in2, out)
    
def OrNode(graph, in1, in2, out):
    '''
:brief: [Graph] Creates a bitwise INCLUSIVE OR node.
:param: [in] graph The reference to the graph.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image.
:param: [in] in2 A *VX_DF_IMAGE_U8* input image.
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_or
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxOrNode(graph, in1, in2, out)
    
def XorNode(graph, in1, in2, out):
    '''
:brief: [Graph] Creates a bitwise EXCLUSIVE OR node.
:param: [in] graph The reference to the graph.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image.
:param: [in] in2 A *VX_DF_IMAGE_U8* input image.
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_xor
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxXorNode(graph, in1, in2, out)
    
def NotNode(graph, input, output):
    '''
:brief: [Graph] Creates a bitwise NOT node.
:param: [in] graph The reference to the graph.
:param: [in] input A *VX_DF_IMAGE_U8* input image.
:param: [out] output The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_not
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxNotNode(graph, input, output)
    
def MultiplyNode(graph, in1, in2, scale, overflow_policy, rounding_policy, out):
    '''
:brief: [Graph] Creates an pixelwise-multiplication node.
:param: [in] graph The reference to the graph.
:param: [in] in1 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*.
:param: [in] in2 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*.
:param: [in] scale A non-negative *VX_TYPE_FLOAT32* multiplied to each product before overflow handling.
:param: [in] overflow_policy A *VX_TYPE_ENUM* of the *vx_convert_policy_e* enumeration.
:param: [in] rounding_policy A *VX_TYPE_ENUM* of the *vx_round_policy_e* enumeration.
:param: [out] out The output image, a *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* image.
:ingroup: group_vision_function_mult
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxMultiplyNode(graph, in1, in2, scale, overflow_policy, rounding_policy, out)
    
def AddNode(graph, in1, in2, policy, out):
    '''
:brief: [Graph] Creates an arithmetic addition node.
:param: [in] graph The reference to the graph.
:param: [in] in1 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*.
:param: [in] in2 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*.
:param: [in] policy A *VX_TYPE_ENUM* of the vx_convert_policy_e enumeration.
:param: [out] out The output image, a *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* image.
:ingroup: group_vision_function_add
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxAddNode(graph, in1, in2, policy, out)
    
def SubtractNode(graph, in1, in2, policy, out):
    '''
:brief: [Graph] Creates an arithmetic subtraction node.
:param: [in] graph The reference to the graph.
:param: [in] in1 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*, the minuend.
:param: [in] in2 An input image, *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16*, the subtrahend.
:param: [in] policy A *VX_TYPE_ENUM* of the vx_convert_policy_e enumeration.
:param: [out] out The output image, a *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* image.
:ingroup: group_vision_function_sub
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxSubtractNode(graph, in1, in2, policy, out)
    
def ConvertDepthNode(graph, input, output, policy, shift):
    '''
:brief: [Graph] Creates a bit-depth conversion node.
:param: [in] graph The reference to the graph.
:param: [in] input The input image.
:param: [out] output The output image.
:param: [in] policy A scalar containing a *VX_TYPE_ENUM* of the vx_convert_policy_e enumeration.
:param: [in] shift A scalar containing a *VX_TYPE_INT32* of the shift value.
:ingroup: group_vision_function_convertdepth
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxConvertDepthNode(graph, input, output, policy, shift)
    
def CannyEdgeDetectorNode(graph, input, hyst, gradient_size, norm_type, output):
    '''
:brief: [Graph] Creates a Canny Edge Detection Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] hyst The double threshold for hysteresis.
:param: [in] gradient_size The size of the Sobel filter window, must support at least 3, 5, and 7.
:param: [in] norm_type A flag indicating the norm used to compute the gradient, *VX_NORM_L1* or VX_NORM_L2.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format with values either 0 or 255.
:ingroup: group_vision_function_canny
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxCannyEdgeDetectorNode(graph, input, hyst, gradient_size, norm_type, output)
    
def WarpAffineNode(graph, input, matrix, type, output):
    '''
:brief: [Graph] Creates an Affine Warp Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] matrix The affine matrix. Must be 2x3 of type VX_TYPE_FLOAT32.
:param: [in] type The interpolation type from *vx_interpolation_type_e*.
*VX_INTERPOLATION_TYPE_AREA* is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:ingroup: group_vision_function_warp_affine
:note: Only *VX_NODE_ATTRIBUTE_BORDER_MODE* value *VX_BORDER_MODE_UNDEFINED* or
*VX_BORDER_MODE_CONSTANT* is supported.
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxWarpAffineNode(graph, input, matrix, type, output)
    
def WarpPerspectiveNode(graph, input, matrix, type, output):
    '''
:brief: [Graph] Creates a Perspective Warp Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] matrix The perspective matrix. Must be 3x3 of type *VX_TYPE_FLOAT32*.
:param: [in] type The interpolation type from *vx_interpolation_type_e*.
*VX_INTERPOLATION_TYPE_AREA* is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:ingroup: group_vision_function_warp_perspective
:note: Only *VX_NODE_ATTRIBUTE_BORDER_MODE* value *VX_BORDER_MODE_UNDEFINED* or
*VX_BORDER_MODE_CONSTANT* is supported.
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxWarpPerspectiveNode(graph, input, matrix, type, output)
    
def HarrisCornersNode(graph, input, strength_thresh, min_distance, sensitivity, gradient_size, block_size, corners, num_corners):
    '''
:brief: [Graph] Creates a Harris Corners Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] strength_thresh The *VX_TYPE_FLOAT32* minimum threshold with which to eliminate Harris Corner scores (computed using the normalized Sobel kernel).
:param: [in] min_distance The *VX_TYPE_FLOAT32* radial Euclidean distance for non-maximum suppression.
:param: [in] sensitivity The *VX_TYPE_FLOAT32* scalar sensitivity threshold :f:$ k :f:$ from the Harris-Stephens equation.
:param: [in] gradient_size The gradient window size to use on the input. The
implementation must support at least 3, 5, and 7.
:param: [in] block_size The block window size used to compute the Harris Corner score.
The implementation must support at least 3, 5, and 7.
:param: [out] corners The array of *VX_TYPE_KEYPOINT* objects.
:param: [out] num_corners The total number of detected corners in image (optional). Use a VX_TYPE_SIZE scalar.
:ingroup: group_vision_function_harris
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxHarrisCornersNode(graph, input, strength_thresh, min_distance, sensitivity, gradient_size, block_size, corners, num_corners)
    
def FastCornersNode(graph, input, strength_thresh, nonmax_suppression, corners, num_corners):
    '''
:brief: [Graph] Creates a FAST Corners Node.
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] strength_thresh Threshold on difference between intensity of the central pixel and pixels on Bresenham's circle of radius 3 (*VX_TYPE_FLOAT32* scalar).
:param: [in] nonmax_suppression If true, non-maximum suppression is applied to
detected corners before being placed in the *vx_array* of *VX_TYPE_KEYPOINT* objects.
:param: [out] corners Output corner *vx_array* of *VX_TYPE_KEYPOINT*.
:param: [out] num_corners The total number of detected corners in image (optional). Use a VX_TYPE_SIZE scalar.
:ingroup: group_vision_function_fast
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxFastCornersNode(graph, input, strength_thresh, nonmax_suppression, corners, num_corners)
    
def OpticalFlowPyrLKNode(graph, old_images, new_images, old_points, new_points_estimates, new_points, termination, epsilon, num_iterations, use_initial_estimate, window_dimension):
    '''
:brief: [Graph] Creates a Lucas Kanade Tracking Node.
:param: [in] graph The reference to the graph.
:param: [in] old_images Input of first (old) image pyramid in *VX_DF_IMAGE_U8*.
:param: [in] new_images Input of destination (new) image pyramid *VX_DF_IMAGE_U8*.
:param: [in] old_points An array of key points in a *vx_array* of *VX_TYPE_KEYPOINT*; those key points are defined at
 the :a: old_images high resolution pyramid.
:param: [in] new_points_estimates An array of estimation on what is the output key points in a *vx_array* of
 *VX_TYPE_KEYPOINT*; those keypoints are defined at the :a: new_images high resolution pyramid.
:param: [out] new_points An output array of key points in a *vx_array* of *VX_TYPE_KEYPOINT*; those key points are
 defined at the :a: new_images high resolution pyramid.
:param: [in] termination The termination can be *VX_TERM_CRITERIA_ITERATIONS* or *VX_TERM_CRITERIA_EPSILON* or
*VX_TERM_CRITERIA_BOTH*.
:param: [in] epsilon The *vx_float32* error for terminating the algorithm.
:param: [in] num_iterations The number of iterations. Use a *VX_TYPE_UINT32* scalar.
:param: [in] use_initial_estimate Use a *VX_TYPE_BOOL* scalar.
:param: [in] window_dimension The size of the window on which to perform the algorithm. See 
 *VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION*
:ingroup: group_vision_function_opticalflowpyrlk
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxOpticalFlowPyrLKNode(graph, old_images, new_images, old_points, new_points_estimates, new_points, termination, epsilon, num_iterations, use_initial_estimate, window_dimension)
    
def RemapNode(graph, input, table, policy, output):
    '''
:brief: [Graph] Creates a Remap Node.
:param: [in] graph The reference to the graph that will contain the node.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] table The remap table object.
:param: [in] policy An interpolation type from *vx_interpolation_type_e*.
*VX_INTERPOLATION_TYPE_AREA* is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:note: Only *VX_NODE_ATTRIBUTE_BORDER_MODE* value *VX_BORDER_MODE_UNDEFINED* or
*VX_BORDER_MODE_CONSTANT* is supported.
:return: A *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*  
:ingroup: group_vision_function_remap
    '''
    return lib.vxRemapNode(graph, input, table, policy, output)
    
def HalfScaleGaussianNode(graph, input, output, kernel_size):
    '''
:brief: [Graph] Performs a Gaussian Blur on an image then half-scales it.
:details: The output image size is determined by:
:f:[
W_{output} = :frac:{W_{input} + 1}{2} \\
,
H_{output} = :frac:{H_{input} + 1}{2}
:f:]
:param: [in] graph The reference to the graph.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:param: [in] kernel_size The input size of the Gaussian filter. Supported values are 3 and 5. 
:ingroup: group_vision_function_scale_image
:return: *vx_node*.
:retval: vx_node A node reference. Any possible errors preventing a successful creation should be checked using *vxGetStatus*
    '''
    return lib.vxHalfScaleGaussianNode(graph, input, output, kernel_size)
    