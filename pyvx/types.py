from cffi import FFI
import numpy

class CHANNEL_0: pass
class CHANNEL_1: pass
class CHANNEL_2: pass
class CHANNEL_3: pass
class CHANNEL_R: pass
class CHANNEL_G: pass
class CHANNEL_B: pass
class CHANNEL_A: pass
class CHANNEL_Y: pass
class CHANNEL_U: pass
class CHANNEL_V: pass

class FourccMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        if cls.dtype is not None:
            cls.dtype = numpy.dtype(cls.dtype)
            if not cls.ctype:
                cls.ctype = cls.dtype.name + '_t'
            assert FFI().sizeof(cls.ctype) == cls.dtype.itemsize
            if cls.items == 1:
                assert cls.dtype not in FOURCC.dtype2fourcc
                FOURCC.dtype2fourcc[cls.dtype] = cls
            try:
                cls.maxval = numpy.iinfo(cls.dtype).max
                cls.minval = numpy.iinfo(cls.dtype).min
                cls.inttype = True
            except ValueError:
                cls.maxval = numpy.finfo(cls.dtype).max
                cls.minval = numpy.finfo(cls.dtype).min
                cls.inttype = False
        return cls

class FOURCC(object):
    __metaclass__ = FourccMeta
    dtype2fourcc = {}

    items = 1
    channels = [CHANNEL_0]
    channel_offsets = [0]
    channel_subsamp = [0]
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

class FOURCC_VIRT(FOURCC): pass

class FOURCC_RGB(FOURCC):
    items = 3
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 2] * 2
    channel_subsamp = [0, 0, 0] * 2

class FOURCC_RGBX(FOURCC):
    items = 4
    dtype = 'uint8'
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3]
    channel_offsets = [0, 1, 2, 0, 1, 2, 3]
    channel_subsamp = [0, 0, 0, 0, 0, 0, 0] 

class FOURCC_UYVY(FOURCC):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [1, 0, 2] * 2
    channel_subsamp = [0, 1, 1] * 2

class FOURCC_YUYV(FOURCC):
    items = 2
    dtype = 'uint8'
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 3] * 2
    channel_subsamp = [0, 1, 1] * 2

class FOURCC_U8(FOURCC): dtype = 'uint8'
class FOURCC_S8(FOURCC): dtype = 'int8'
class FOURCC_U16(FOURCC): dtype = 'uint16'
class FOURCC_S16(FOURCC): dtype = 'int16'
class FOURCC_U32(FOURCC): dtype = 'uint32'
class FOURCC_S32(FOURCC): dtype = 'int32'
class FOURCC_U64(FOURCC): dtype = 'uint64'
class FOURCC_S64(FOURCC): dtype = 'int64'

class FOURCC_F32(FOURCC): 
    dtype = 'float32'
    ctype = 'float'

class FOURCC_F64(FOURCC): 
    dtype = 'float64'
    ctype = 'double'

try:
    class FOURCC_F128(FOURCC):
        dtype = 'float128'
        ctype = 'long double'
except TypeError:
    pass

def result_color(t0, *color):
    if numpy.result_type is None:
        return t0 # FIXME
    dt = numpy.result_type(*[c.dtype for c in color])
    return FOURCC.dtype2fourcc[dt]

def value_color_type(val):
    dt = numpy.array([val]).dtype
    return FOURCC.dtype2fourcc[dt]

def signed_color(col):
    return {FOURCC_U8: FOURCC_S8,
            FOURCC_S8: FOURCC_S8,
            FOURCC_U16: FOURCC_S16,
            FOURCC_S16: FOURCC_S16,
            FOURCC_U32: FOURCC_S32,
            FOURCC_S32: FOURCC_S32,
            FOURCC_U64: FOURCC_S64,
            FOURCC_S64: FOURCC_S64,
            FOURCC_F32: FOURCC_F32,
            FOURCC_F64: FOURCC_F64,
            FOURCC_F128: FOURCC_F128,
           }[col]

class BORDER_MODE_UNDEFINED: pass
class BORDER_MODE_CONSTANT: pass
class BORDER_MODE_REPLICATE: pass

class CONVERT_POLICY_TRUNCATE: pass
class CONVERT_POLICY_SATURATE: pass

class ROUND_POLICY_TO_ZERO: pass
class ROUND_POLICY_TO_NEAREST_EVEN: pass

class VerificationError(Exception): pass
class VX_ERROR_MULTIPLE_WRITERS(VerificationError): pass
class VX_ERROR_INVALID_GRAPH(VerificationError): pass
class VX_ERROR_INVALID_VALUE(VerificationError): pass
class VX_ERROR_INVALID_FORMAT(VerificationError): pass
class VX_ERROR_GRAPH_ABANDONED(Exception): pass
class VX_SUCCESS(object): pass
vx_status_codes = [VX_SUCCESS, VX_ERROR_MULTIPLE_WRITERS, VX_ERROR_INVALID_GRAPH, 
                   VX_ERROR_INVALID_VALUE, VX_ERROR_INVALID_FORMAT,
                   VX_ERROR_GRAPH_ABANDONED]
