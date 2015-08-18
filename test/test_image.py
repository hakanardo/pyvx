import py.test
from pyvx import *

class TestImage(object):
    def test_imagepatch_addressing(self):
        with Graph() as g:
            img = Image(640, 480, DF_IMAGE_U8)
        assert(img.imagepatch_addressing[0].dim_x == 640)
        assert(img.imagepatch_addressing[0].dim_y == 480)
        assert(img.imagepatch_addressing[0].step_x == 1)
        assert(img.imagepatch_addressing[0].step_y == 1)
        assert(img.imagepatch_addressing[0].scale_x == SCALE_UNITY)
        assert(img.imagepatch_addressing[0].scale_y == SCALE_UNITY)
        assert(img.imagepatch_addressing[0].stride_x == 1)
        assert(img.imagepatch_addressing[0].stride_y == 640)
