import os
from cffi import FFI
import pyvx.inc.vx_vendors as vendors
import pyvx.inc.vx_types as types
import pyvx.inc.vx_kernels as kernels

ffi = FFI()

ffi.cdef('''
#define VX_MAX_IMPLEMENTATION_NAME ...
#define VX_MAX_KERNEL_NAME ...
#define VX_MAX_LOG_MESSAGE_LEN ...
/* TODO
#define VX_VERSION_MAJOR(x) ((x & 0xFF) << 8)
#define VX_VERSION_MINOR(x) ((x & 0xFF) << 0)
*/
#define VX_VERSION_1_0 ...
#define VX_VERSION ...
''')

ffi.cdef(vendors.cdef)
ffi.cdef(types.cdef + kernels.cdef)
#ffi.cdef(kernels.cdef)

mydir = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(mydir, 'headers')
lib = ffi.verify('#include "VX/vx.h"\n' + types.verify,
                 extra_compile_args=["-I" + d],
                 modulename='__pyvx_inc_vx')
for n in dir(lib):
    if n.lower().startswith('vx_'):
        locals()[n[3:]] = getattr(lib, n)

def imagepatch_addressing(dim_x=0, dim_y=0, stride_x=0, stride_y=0, 
                          scale_x=0, scale_y=0, step_x=0, step_y=0):
    return  ffi.new('vx_imagepatch_addressing_t *', 
                    [dim_x, dim_y, stride_x, stride_y, 
                     scale_x, scale_y, step_x, step_y])

def perf(tmp=0, beg=0, end=0, sum=0, avg=0, min=0, num=0):
    return ffi.new('vx_perf_t *', [tmp, beg, end, sum, avg, min, num])

def kernel_info(enumeration, name):
    return ffi.new('vx_kernel_info_t *', [enumeration, name])

def border_mode(mode, constant_value=0):
    return ffi.new('vx_border_mode_t *', [mode, constant_value])

def keypoint(x, y, strength, scale, orientation, tracking_status, error):
    return ffi.new('vx_keypoint_t *', 
                   [x, y, strength, scale, orientation, tracking_status, error])

def rectangle(start_x, start_y, end_x, end_y):
    return ffi.new('vx_rectangle_t *', [start_x, start_y, end_x, end_y])

def delta_rectangle(delta_start_x, delta_start_y, delta_end_x, delta_end_y):
    return ffi.new('vx_delta_rectangle_t *',
                   [delta_start_x, delta_start_y, delta_end_x, delta_end_y])

def coordinates2d(x, y):
    return ffi.new('vx_coordinates2d_t *', [x, y])

def coordinates3d(x, y, z):
    return ffi.new('vx_coordinates3d_t *', [x, y, z])

def coordinates(x, y, z=None):
    if z is None:
        return coordinates2d(x, y)
    else:
        return coordinates3d(x, y, z)
