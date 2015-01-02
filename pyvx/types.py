from cffi import FFI
import numpy
from pyvx.inc.vx import *

class ExtraChannel(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'vx.' + self.name
    __str__ = __repr__

CHANNEL_R = ExtraChannel('CHANNEL_R')
CHANNEL_G = ExtraChannel('CHANNEL_G')
CHANNEL_B = ExtraChannel('CHANNEL_B')
CHANNEL_A = ExtraChannel('CHANNEL_A')
CHANNEL_Y = ExtraChannel('CHANNEL_Y')
CHANNEL_U = ExtraChannel('CHANNEL_U')
CHANNEL_V = ExtraChannel('CHANNEL_V')

channel_char = {
    CHANNEL_0: '0',
    CHANNEL_1: '1',
    CHANNEL_2: '2',
    CHANNEL_3: '3',
    CHANNEL_R: 'r',
    CHANNEL_G: 'g',
    CHANNEL_B: 'b',
    CHANNEL_A: 'a',
    CHANNEL_Y: 'y',
    CHANNEL_U: 'u',
    CHANNEL_V: 'v',
}

class ImageFormatMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        if cls.dtype is not None:
            ImageFormat.color2image_format[cls.color] = cls
            cls.dtype = numpy.dtype(cls.dtype)
            if not cls.ctype:
                cls.ctype = cls.dtype.name + '_t'
            assert FFI().sizeof(cls.ctype) == cls.dtype.itemsize
            if cls.items == 1:
                assert cls.dtype not in ImageFormat.dtype2color
                ImageFormat.dtype2color[cls.dtype] = cls.color
            try:
                cls.maxval = numpy.iinfo(cls.dtype).max
                cls.minval = numpy.iinfo(cls.dtype).min
                cls.inttype = True
            except ValueError:
                cls.maxval = numpy.finfo(cls.dtype).max
                cls.minval = numpy.finfo(cls.dtype).min
                cls.inttype = False
        return cls

class ImageFormat(object):
    __metaclass__ = ImageFormatMeta
    dtype2color = {}
    color2image_format = {}

    items = 1
    channels = [CHANNEL_0]
    channel_offsets = [0]
    channel_subsamp = [False]
    dtype = None
    ctype = None

    @classmethod
    def subsamp(cls, channel):
        if cls.channel_subsamp[cls.channels.index(channel)]:
            return 'subsample'
        return ''

    @classmethod
    def offset(cls, channel):
        return cls.channel_offsets[cls.channels.index(channel)]

    @classmethod
    def imagepatch_addressing(cls, width, height):
        stride = len(cls.channels)
        ss = cls.channel_subsamp[:cls.items]
        steps = [2 if s else 1 for s in ss]
        return [imagepatch_addressing(dim_x=width, dim_y=height,
                                      stride_x=stride, stride_y=stride*width,
                                      step_x=st, step_y=1,
                                      scale_x=SCALE_UNITY/st, scale_y=SCALE_UNITY)
                for st in steps]

class ImageFormatVIRT(ImageFormat): 
    color = DF_IMAGE_VIRT

class ImageFormatRGB(ImageFormat):
    items = 3
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 2] * 2
    channel_subsamp = [False, False, False] * 2
    color = DF_IMAGE_RGB

class ImageFormatRGBX(ImageFormat):
    items = 4
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3]
    channel_offsets = [0, 1, 2, 0, 1, 2, 3]
    channel_subsamp = [False, False, False, False, False, False, False] 
    color = DF_IMAGE_RGBX

class ImageFormatUYVY(ImageFormat):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [1, 0, 2] * 2
    channel_subsamp = [False, True, True] * 2
    color = DF_IMAGE_UYVY

class ImageFormatYUYV(ImageFormat):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 3] * 2
    channel_subsamp = [False, True, True] * 2
    color = DF_IMAGE_YUYV

class ImageFormatU8(ImageFormat): 
    dtype = 'uint8'
    color = DF_IMAGE_U8

class ImageFormatS8(ImageFormat): 
    dtype = 'int8'
    color = DF_IMAGE_S8

class ImageFormatU16(ImageFormat): 
    dtype = 'uint16'
    color = DF_IMAGE_U16

class ImageFormatS16(ImageFormat): 
    dtype = 'int16'
    color = DF_IMAGE_S16

class ImageFormatU32(ImageFormat): 
    dtype = 'uint32'
    color = DF_IMAGE_U32

class ImageFormatS32(ImageFormat): 
    dtype = 'int32'
    color = DF_IMAGE_S32

class ImageFormatU64(ImageFormat): 
    dtype = 'uint64'
    color = DF_IMAGE_U64

class ImageFormatS64(ImageFormat): 
    dtype = 'int64'
    color = DF_IMAGE_S64

class ImageFormatF32(ImageFormat): 
    dtype = 'float32'
    ctype = 'float'
    color = DF_IMAGE_F32

class ImageFormatF64(ImageFormat): 
    dtype = 'float64'
    ctype = 'double'
    color = DF_IMAGE_F64

try:
    class ImageFormatF128(ImageFormat):
        dtype = 'float128'
        ctype = 'long double'
        color = DF_IMAGE_F128
except TypeError:
    pass

def result_color(t0, *formats):
    if numpy.result_type is None:
        return t0 # FIXME
    dt = numpy.result_type(*[c.dtype for c in formats])
    return ImageFormat.dtype2color[dt]

def value_color_type(val):
    dt = numpy.array([val]).dtype
    return ImageFormat.dtype2color[dt]

def signed_format(col):
    return {ImageFormatU8: ImageFormatS8,
            ImageFormatS8: ImageFormatS8,
            ImageFormatU16: ImageFormatS16,
            ImageFormatS16: ImageFormatS16,
            ImageFormatU32: ImageFormatS32,
            ImageFormatS32: ImageFormatS32,
            ImageFormatU64: ImageFormatS64,
            ImageFormatS64: ImageFormatS64,
            ImageFormatF32: ImageFormatF32,
            ImageFormatF64: ImageFormatF64,
            ImageFormatF128: ImageFormatF128,
           }[col]

def image_format(color):
    return ImageFormat.color2image_format[color]

class VxError(Exception):
    errno = FAILURE

    def __init__(self, msg='', ref=None):
        Exception.__init__(self, '%s: %s' % (ref, msg))
        if ref is not None:
            ref.add_log_entry(self.errno, msg)


class MultipleWritersError(VxError): errno = ERROR_MULTIPLE_WRITERS
class InvalidGraphError(VxError):    errno = ERROR_INVALID_GRAPH
class InvalidValueError(VxError):    errno = ERROR_INVALID_VALUE
class InvalidFormatError(VxError):   errno = ERROR_INVALID_FORMAT
class InvalidNodeError(VxError):     errno = ERROR_INVALID_NODE

class GraphAbandonedError(VxError): errno = ERROR_GRAPH_ABANDONED
class InvalidReferenceError(VxError): errno = ERROR_INVALID_REFERENCE
class InvalidParametersError(VxError): errno = ERROR_INVALID_PARAMETERS

TYPE_CHAR.ctype = 'vx_char'
TYPE_INT8.ctype = 'vx_int8'
TYPE_UINT8.ctype = 'vx_uint8'
TYPE_INT16.ctype = 'vx_int16'
TYPE_UINT16.ctype = 'vx_uint16'
TYPE_INT32.ctype = 'vx_int32'
TYPE_UINT32.ctype = 'vx_uint32'
TYPE_INT64.ctype = 'vx_int64'
TYPE_UINT64.ctype = 'vx_uint64'
TYPE_FLOAT32.ctype = 'vx_float32'
TYPE_FLOAT64.ctype = 'vx_float64'
TYPE_ENUM.ctype = 'vx_enum'
TYPE_SIZE.ctype = 'vx_size'
TYPE_DF_IMAGE.ctype = 'vx_df_image'
TYPE_BOOL.ctype = 'vx_bool'
TYPE_RECTANGLE.ctype = 'vx_rectangle'
TYPE_KEYPOINT.ctype = 'vx_keypoint'
TYPE_COORDINATES2D.ctype = 'vx_coordinates2d'
TYPE_COORDINATES3D.ctype = 'vx_coordinates3d'
TYPE_USER_STRUCT_START.ctype = 'vx_user_struct_start'
TYPE_REFERENCE.ctype = 'vx_reference'
TYPE_CONTEXT.ctype = 'vx_context'
TYPE_GRAPH.ctype = 'vx_graph'
TYPE_NODE.ctype = 'vx_node'
TYPE_KERNEL.ctype = 'vx_kernel'
TYPE_PARAMETER.ctype = 'vx_parameter'
TYPE_DELAY.ctype = 'vx_delay'
TYPE_LUT.ctype = 'vx_lut'
TYPE_DISTRIBUTION.ctype = 'vx_distribution'
TYPE_PYRAMID.ctype = 'vx_pyramid'
TYPE_THRESHOLD.ctype = 'vx_threshold'
TYPE_MATRIX.ctype = 'vx_matrix'
TYPE_CONVOLUTION.ctype = 'vx_convolution'
TYPE_SCALAR.ctype = 'vx_scalar'
TYPE_ARRAY.ctype = 'vx_array'
TYPE_IMAGE.ctype = 'vx_image'
TYPE_REMAP.ctype = 'vx_remap'
TYPE_ERROR.ctype = 'vx_error'
TYPE_META_FORMAT.ctype = 'vx_meta_format'

TYPE_STRING.ctype = 'char *'
