from pyvx import vx

class TestDemo(object):
    def test_sobel(self):
        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        g = vx.CreateGraph(c)
        node = vx.Sobel3x3Node(g, img, dx, dy)
        assert vx.GetStatus(vx.reference(node)) == vx.SUCCESS
        assert vx.VerifyGraph(g) == vx.SUCCESS
        assert vx.ProcessGraph(g) == vx.SUCCESS
        # FIXME: assert something
        assert vx.ReleaseContext(c) == vx.SUCCESS
