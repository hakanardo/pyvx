from _types_auto import *

print lib.VX_MAX_KERNEL_NAME

SCALE_PYRAMID_HALF = 0.5
SCALE_PYRAMID_ORB = 0.8408964

def imagepatch_addressing_t(dim_x=0, dim_y=0, stride_x=0, stride_y=0, scale_x=0, scale_y=0, step_x=0, step_y=0):
    return ffi.new("vx_imagepatch_addressing_t *", (dim_x, dim_y, stride_x, stride_y, scale_x, scale_y, step_x, step_y))


def perf_t(tmp=0, beg=0, end=0, sum=0, avg=0, min=0, num=0, max=0):
    return ffi.new("vx_perf_t *", (tmp, beg, end, sum, avg, min, num, max))


def kernel_info_t(enumeration, name):
    s = ffi.new("vx_kernel_info_t *")
    s.enumeration = enumeration
    assert len(name) < MAX_KERNEL_NAME
    s.name[0:len(name)] = name
    s.name[len(name)] = '\0'
    return s


def border_mode_t(mode, constant_value=0):
    return ffi.new("vx_border_mode_t *", (mode, constant_value))


def keypoint_t(x, y, strength, scale, orientation, tracking_status, error):
    return ffi.new("vx_keypoint_t *", (x, y, strength, scale, orientation, tracking_status, error))


def rectangle_t(start_x, start_y, end_x, end_y):
    return ffi.new("vx_rectangle_t *", (start_x, start_y, end_x, end_y))


def delta_rectangle_t(delta_start_x, delta_start_y, delta_end_x, delta_end_y):
    return ffi.new("vx_delta_rectangle_t *", (delta_start_x, delta_start_y, delta_end_x, delta_end_y))


def coordinates2d_t(x, y):
    return ffi.new("vx_coordinates2d_t *", (x, y))


def coordinates3d_t(x, y, z):
    return ffi.new("vx_coordinates3d_t *", (x, y, z))
