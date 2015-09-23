from pyvx import __backend_version__
from pyvx._auto_vx import *
import sys

if ffi.string(lib._get_backend_version()) != __backend_version__:
    print(ffi.string(lib._get_backend_version()).__class__)
    print(ffi.string(lib._get_backend_name()).decode("utf8"))
    raise ImportError("Backend version missmatch. Please recompile it using:\n\n" +
                      "    %s -mpyvx.build_cbackend %s %s\n" % (sys.executable,
                                                                ffi.string(lib._get_backend_name()).decode("utf8"),
                                                                ffi.string(lib._get_backend_install_path()).decode("utf8")))

SCALE_PYRAMID_HALF = 0.5
SCALE_PYRAMID_ORB = 0.8408964
FMT_REF = ffi.string(lib._get_FMT_REF())
FMT_SIZE = ffi.string(lib._get_FMT_SIZE())

def KERNEL_BASE(vendor, libid):
    return lib._get_KERNEL_BASE(vendor, libid)

def imagepatch_addressing_t(dim_x=0, dim_y=0, stride_x=0, stride_y=0, scale_x=0, scale_y=0, step_x=0, step_y=0):
    """
    Allocates and returns a vx_imagepatch_addressing_t struct.
    """
    return ffi.new("vx_imagepatch_addressing_t *", (dim_x, dim_y, stride_x, stride_y, scale_x, scale_y, step_x, step_y))


def perf_t(tmp=0, beg=0, end=0, sum=0, avg=0, min=0, num=0, max=0):
    """
    Allocates and returns a vx_perf_t struct.
    """
    return ffi.new("vx_perf_t *", (tmp, beg, end, sum, avg, min, num, max))


def kernel_info_t(enumeration, name):
    """
    Allocates and returns a vx_kernel_info_t struct.
    """
    s = ffi.new("vx_kernel_info_t *")
    s.enumeration = enumeration
    assert len(name) < MAX_KERNEL_NAME
    s.name[0:len(name)] = name
    s.name[len(name)] = b'\0'
    return s


def border_mode_t(mode, constant_value=0):
    """
    Allocates and returns a vx_border_mode_t struct.
    """
    return ffi.new("vx_border_mode_t *", (mode, constant_value))


def keypoint_t(x, y, strength, scale, orientation, tracking_status, error):
    """
    Allocates and returns a vx_keypoint_t struct.
    """
    return ffi.new("vx_keypoint_t *", (x, y, strength, scale, orientation, tracking_status, error))


def rectangle_t(start_x, start_y, end_x, end_y):
    """
    Allocates and returns a vx_rectangle_t struct.
    """
    return ffi.new("vx_rectangle_t *", (start_x, start_y, end_x, end_y))


def delta_rectangle_t(delta_start_x, delta_start_y, delta_end_x, delta_end_y):
    """
    Allocates and returns a vx_delta_rectangle_t struct.
    """
    return ffi.new("vx_delta_rectangle_t *", (delta_start_x, delta_start_y, delta_end_x, delta_end_y))


def coordinates2d_t(x, y):
    """
    Allocates and returns a vx_coordinates2d_t struct.
    """
    return ffi.new("vx_coordinates2d_t *", (x, y))


def coordinates3d_t(x, y, z):
    """
    Allocates and returns a vx_coordinates3d_t struct.
    """
    return ffi.new("vx_coordinates3d_t *", (x, y, z))

