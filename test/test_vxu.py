from pyvx.default import vx, vxu

class TestDemo(object):
    def test_sobel(self):
        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        assert vxu.Sobel3x3(c, img, dx, dy) == vx.SUCCESS
        _, r = vx.GetValidRegionImage(img)
        assert r.start_x == 0
        assert r.start_y == 0
        _, r = vx.GetValidRegionImage(dx)
        assert r.start_x == 1
        assert r.start_y == 1
        assert vx.ReleaseContext(c) == vx.SUCCESS
