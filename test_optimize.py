from pyvx import *
from array import array

class TestOptimize(object):
    def test_ded_code_removal(self):
        g = Graph()
        with g:
            img = Image(10, 10, FOURCC_U8, array('B', range(100)))
            dx, dy = Sobel3x3(img)
            gdx = Gaussian3x3(dx)
            gdy = Gaussian3x3(dy)
            gdx.force()
        g.verify()
        assert gdy.optimized_out
        assert dy.optimized_out
        assert gdy.producer.optimized_out
        assert not gdx.optimized_out
        assert not dx.optimized_out
        assert not gdx.producer.optimized_out
        assert not dx.producer.optimized_out
        assert not dy.producer.optimized_out
        g.process()
        assert gdx.data[55] == 8
        assert gdx.data[66] == 8

    def test_merge_elementwise(self):
        g = Graph()
        with g:
            img1 = Image(20, 20, FOURCC_U8, array('B', range(200) * 2))
            img2 = Image(20, 20, FOURCC_U8, array('B', range(200) * 2))
            dx, dy = Sobel3x3(img1)
            t1 = dx + img2
            t2 = 2 * dy
            t3 = Gaussian3x3(Gaussian3x3(t2)) - t1
            t3.force()
        g.verify()
        assert t1.producer is t2.producer
        assert t3.producer is not t1.producer
        g.process()
        assert t3.data[9*20 + 9] == 147
        assert t3.data[10*20 + 10] == 70
        assert t3.data[11*20 + 11] == 37

