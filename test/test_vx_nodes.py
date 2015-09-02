from pyvx.default import vx

class TestDemo(object):
    def test_sobel(self):
        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        g = vx.CreateGraph(c)
        node = vx.Sobel3x3Node(g, img, dx, dy)
        assert vx.GetStatus(vx.reference(node)) == vx.SUCCESS
        vx.VerifyGraph(g)
        vx.ProcessGraph(g)
        _, r = vx.GetValidRegionImage(img)
        assert r.start_x == 0
        assert r.start_y == 0
        _, r = vx.GetValidRegionImage(dx)
        assert r.start_x == 1
        assert r.start_y == 1
        assert vx.ReleaseContext(c) == vx.SUCCESS
