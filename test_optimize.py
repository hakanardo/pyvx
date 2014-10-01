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
