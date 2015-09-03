from pyvx import vx, vxu

class TestDemo(object):
    def test_sobel(self):
        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        assert vxu.Sobel3x3(c, img, dx, dy) == vx.SUCCESS
        # FIXME: assert something
        assert vx.ReleaseContext(c) == vx.SUCCESS
