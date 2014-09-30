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

def make_fourcc(n_items, t, chs=[], ctype=None, n=None):
    if ctype is None:
        ctype = t + '_t'
    if n is None:
        n = t
    chs = chs + [[CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3][i]
                 for i in xrange(len(chs))]
    class T:
        base_type = ctype
        channels = set(chs)
        items = n_items
        dtype = numpy.dtype(t)
        name = n
    if T.items == 1:
        dtype2fourcc[T.dtype] = T
    assert FFI().sizeof(ctype) == T.dtype.itemsize
    return T

class FOURCC_VIRT: pass
FOURCC_RGB  = make_fourcc(3, 'uint8', [CHANNEL_R, CHANNEL_G, CHANNEL_B], n='RGB')
FOURCC_RGBX = make_fourcc(4, 'uint8', [CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_3], n='RGBX')
FOURCC_UYVY = make_fourcc(2, 'uint8', [CHANNEL_Y, CHANNEL_U, CHANNEL_V], n='UYVY')
FOURCC_YUYV = make_fourcc(2, 'uint8', [CHANNEL_Y, CHANNEL_U, CHANNEL_V], n='YUYV')
FOURCC_U8   = make_fourcc(1, 'uint8')
FOURCC_S8   = make_fourcc(1, 'int8')
FOURCC_U16  = make_fourcc(1, 'uint16')
FOURCC_S16  = make_fourcc(1, 'int16')
FOURCC_U32  = make_fourcc(1, 'uint32')
FOURCC_S32  = make_fourcc(1, 'int32')
FOURCC_U64  = make_fourcc(1, 'uint64')
FOURCC_S64  = make_fourcc(1, 'int64')
FOURCC_F32  = make_fourcc(1, 'float32', [CHANNEL_0], 'float')
FOURCC_F64  = make_fourcc(1, 'float64', [CHANNEL_0], 'double')
FOURCC_F128 = make_fourcc(1, 'float128', [CHANNEL_0], 'long double')

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
