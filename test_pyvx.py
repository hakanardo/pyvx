from pyvx import *
from array import array

class TestPyVx(object):
    def test_gaussian(self):
        g = Graph()
        img = Image(3, 4, vx.FOURCC_U8, array('B', range(12)))
        with g:
            gimg = Gaussian3x3(img)
            gimg.force()
        g.verify()
        g.process()
        assert gimg.cdata[4] == 4
        assert gimg.cdata[7] == 7

    def test_replicate_border(self):
        g = Graph()
        img = Image(3, 4, vx.FOURCC_U8, array('B', range(12)))
        with g:
            gimg = Gaussian3x3(img)
            gimg.producer.border_mode = vx.BORDER_MODE_REPLICATE
            gimg.force()
        g.verify()
        g.process()
        assert gimg.cdata[0] == 1
        assert gimg.cdata[1] == 1
        assert gimg.cdata[11] == 10
