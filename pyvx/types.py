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

dtype2fourcc = {}

def make_fourcc(n_items, t, ctype=None):
    if ctype is None:
        ctype = t + '_t'
    class T(object):
        base_type = ctype
        channels = [CHANNEL_0]
        channel_offsets = [0]
        channel_subsamp = [0]
        items = n_items
        dtype = numpy.dtype(t)

        @classmethod
        def subsamp(cls, channel):
            if cls.channel_subsamp[cls.channels.index(channel)]:
                return 'subsample'
            return ''

        @classmethod
        def offset(cls, channel):
            return cls.channel_offsets[cls.channels.index(channel)]

    if T.items == 1:
        dtype2fourcc[T.dtype] = T
    assert FFI().sizeof(ctype) == T.dtype.itemsize
    return T

class FOURCC_VIRT(object): pass

class FOURCC_RGB (make_fourcc(3, 'uint8')):
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 2] * 2
    channel_subsamp = [0, 0, 0] * 2

class FOURCC_RGBX(make_fourcc(4, 'uint8')):
    channels = [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3]
    channel_offsets = [0, 1, 2, 0, 1, 2, 3]
    channel_subsamp = [0, 0, 0, 0, 0, 0, 0] 

class FOURCC_UYVY(make_fourcc(2, 'uint8')):
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [1, 0, 2] * 2
    channel_subsamp = [0, 1, 1] * 2

class FOURCC_YUYV(make_fourcc(2, 'uint8')):
    channels = [CHANNEL_Y, CHANNEL_U, CHANNEL_V, CHANNEL_0, CHANNEL_1, CHANNEL_2]
    channel_offsets = [0, 1, 3] * 2
    channel_subsamp = [0, 1, 1] * 2

class FOURCC_U8  (make_fourcc(1, 'uint8')): pass
class FOURCC_S8  (make_fourcc(1, 'int8')): pass
class FOURCC_U16 (make_fourcc(1, 'uint16')): pass
class FOURCC_S16 (make_fourcc(1, 'int16')): pass
class FOURCC_U32 (make_fourcc(1, 'uint32')): pass
class FOURCC_S32 (make_fourcc(1, 'int32')): pass
class FOURCC_U64 (make_fourcc(1, 'uint64')): pass
class FOURCC_S64 (make_fourcc(1, 'int64')): pass
class FOURCC_F32 (make_fourcc(1, 'float32', 'float')): pass
class FOURCC_F64 (make_fourcc(1, 'float64', 'double')): pass
class FOURCC_F128(make_fourcc(1, 'float128', 'long double')): pass

def binop_type(a, b):
    dt = (numpy.array([], a) + numpy.array([], b)).dtype
    return dtype2fourcc[dt]

class BORDER_MODE_UNDEFINED: pass
class BORDER_MODE_CONSTANT: pass
class BORDER_MODE_REPLICATE: pass

class CONVERT_POLICY_TRUNCATE: pass
class CONVERT_POLICY_SATURATE: pass

class MultipleWritersError(Exception): pass
class InvalidGraphError(Exception): pass
class InvalidValueError(Exception): pass
class InvalidFormatError(Exception): pass
