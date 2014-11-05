from cffi import FFI
import numpy
from pyvx.inc.vx import *

class ImageFormatMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        if cls.dtype is not None:
            cls.dtype = numpy.dtype(cls.dtype)
            if not cls.ctype:
                cls.ctype = cls.dtype.name + '_t'
            assert FFI().sizeof(cls.ctype) == cls.dtype.itemsize
            if cls.items == 1:
                assert cls.dtype not in ImageFormat.dtype2ImageFormat
                ImageFormat.dtype2ImageFormat[cls.dtype] = cls
            try:
                cls.maxval = numpy.iinfo(cls.dtype).max
                cls.minval = numpy.iinfo(cls.dtype).min
                cls.inttype = True
            except ValueError:
                cls.maxval = numpy.finfo(cls.dtype).max
                cls.minval = numpy.finfo(cls.dtype).min
                cls.inttype = False
        return cls

    def __eq__(self, other):
        return self is other or self.enum == other

class ImageFormat(object):
    __metaclass__ = ImageFormatMeta
    dtype2ImageFormat = {}

    items = 1
    channels = [CHANNEL_0]
    channel_offsets = [0]
    channel_subsamp = [0]
    dtype = None
    ctype = None
    enum = None

    @classmethod
    def subsamp(cls, channel):
        if cls.channel_subsamp[cls.channels.index(channel)]:
            return 'subsample'
        return ''

    @classmethod
    def offset(cls, channel):
        return cls.channel_offsets[cls.channels.index(channel)]

class ImageFormatVIRT(ImageFormat): pass

class ImageFormatRGB(ImageFormat):
    items = 3
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 2] * 2
    channel_subsamp = [0, 0, 0] * 2

class ImageFormatRGBX(ImageFormat):
    items = 4
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3]
    channel_offsets = [0, 1, 2, 0, 1, 2, 3]
    channel_subsamp = [0, 0, 0, 0, 0, 0, 0] 

class ImageFormatUYVY(ImageFormat):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [1, 0, 2] * 2
    channel_subsamp = [0, 1, 1] * 2

class ImageFormatYUYV(ImageFormat):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 3] * 2
    channel_subsamp = [0, 1, 1] * 2

class ImageFormatU8(ImageFormat): dtype = 'uint8'
class ImageFormatS8(ImageFormat): dtype = 'int8'
class ImageFormatU16(ImageFormat): dtype = 'uint16'
class ImageFormatS16(ImageFormat): dtype = 'int16'
class ImageFormatU32(ImageFormat): dtype = 'uint32'
class ImageFormatS32(ImageFormat): dtype = 'int32'
class ImageFormatU64(ImageFormat): dtype = 'uint64'
class ImageFormatS64(ImageFormat): dtype = 'int64'

class ImageFormatF32(ImageFormat): 
    dtype = 'float32'
    ctype = 'float'

class ImageFormatF64(ImageFormat): 
    dtype = 'float64'
    ctype = 'double'

try:
    class ImageFormatF128(ImageFormat):
        dtype = 'float128'
        ctype = 'long double'
except TypeError:
    pass

def result_color(t0, *color):
    if numpy.result_type is None:
        return t0 # FIXME
    dt = numpy.result_type(*[c.dtype for c in color])
    return ImageFormat.dtype2ImageFormat[dt]

def value_color_type(val):
    dt = numpy.array([val]).dtype
    return ImageFormat.dtype2ImageFormat[dt]

def signed_color(col):
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
    if isinstance(color, type):
        assert issubclass(color, ImageFormat)
        return color
    return _image_format[color]

_image_format = {
    DF_IMAGE_VIRT: ImageFormatVIRT,
    DF_IMAGE_RGB : ImageFormatRGB,
    DF_IMAGE_RGBX: ImageFormatRGBX,
    #DF_IMAGE_NV12: ImageFormatNV12, TODO
    #DF_IMAGE_NV21: ImageFormatNV21, TODO
    DF_IMAGE_UYVY: ImageFormatUYVY,
    DF_IMAGE_YUYV: ImageFormatYUYV,
    #DF_IMAGE_IYUV: ImageFormatIYUV, TODO
    #DF_IMAGE_YUV4: ImageFormatYUV4, TODO
    DF_IMAGE_U8: ImageFormatU8,
    DF_IMAGE_U16 : ImageFormatU16,
    DF_IMAGE_S16 : ImageFormatS16,
    DF_IMAGE_U32 : ImageFormatU32,
    DF_IMAGE_S32 : ImageFormatS32,
}
for k, v in _image_format.items():
    v.enum = k

class VerificationError(Exception): pass
class MultipleWritersError(VerificationError): errno = ERROR_MULTIPLE_WRITERS
class InvalidGraphError(VerificationError):    errno = ERROR_INVALID_GRAPH
class InvalidValueError(VerificationError):    errno = ERROR_INVALID_VALUE
class InvalidFormatError(VerificationError):   errno = ERROR_INVALID_FORMAT
class InvalidNodeError(VerificationError):     errno = ERROR_INVALID_NODE

class GraphAbandonedError(Exception): errno = ERROR_GRAPH_ABANDONED

channel_number = {
    CHANNEL_0: 0,
    CHANNEL_1: 1,
    CHANNEL_2: 2,
    CHANNEL_3: 3,
}