import os
from pyvx.vx.types import *

class TestVxTypes(object):
    def test_imagepatch_addressing_t(self):
        a = imagepatch_addressing_t()
        assert a.dim_x == 0
        a = imagepatch_addressing_t(dim_x=1, dim_y=2, scale_x=3, scale_y=4, stride_x=5,
                                    stride_y=6, step_x=7, step_y=8)
        assert a.dim_x == 1
        assert a.dim_y == 2
        assert a.scale_x == 3
        assert a.scale_y == 4
        assert a.stride_x == 5
        assert a.stride_y == 6
        assert a.step_x == 7
        assert a.step_y == 8

    def test_float_consts(self):
        assert SCALE_PYRAMID_HALF == 0.5

    def test_perf_t(self):
        p = perf_t()
        assert p.tmp == 0
        p = perf_t(tmp=1, beg=2, end=3, sum=4, avg=5, min=6, num=7, max=8)
        assert p.tmp == 1
        assert p.beg == 2
        assert p.end == 3
        assert p.sum == 4
        assert p.avg == 5
        assert p.min == 6
        assert p.num == 7
        assert p.max == 8

    def test_kernel_info_t(self):
        i = kernel_info_t(7, "hello")
        assert i.enumeration == 7
        assert ffi.string(i.name) == "hello"

    def test_border_mode_t(self):
        b = border_mode_t(BORDER_MODE_CONSTANT, 42)
        assert b.mode == BORDER_MODE_CONSTANT
        assert b.constant_value == 42

    def test_keypoint_t(self):
        k = keypoint_t(x=1, y=2, strength=3.5, scale=4.5, orientation=5.5, tracking_status=6, error=7.5)
        assert  k.x == 1
        assert  k.y == 2
        assert  k.strength == 3.5
        assert  k.scale == 4.5
        assert  k.orientation == 5.5
        assert  k.tracking_status == 6
        assert  k.error == 7.5

    def test_coordinates2d_t(self):
        c = coordinates2d_t(1, 2)
        assert c.x == 1
        assert c.y == 2

    def test_coordinates3d_t(self):
        c = coordinates3d_t(1, 2, 3)
        assert c.x == 1
        assert c.y == 2
        assert c.z == 3

    def test_fmt_ref_size(self):
        if os.name != 'nt':
            assert FMT_REF == "%p"
            assert FMT_SIZE == "%zu"

