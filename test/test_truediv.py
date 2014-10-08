from __future__ import division
from pyvx import *
from array import array

class TestDiv(object):
    def test_div(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(12)))
            sa1 = img / 2
            sa2 = img // 2
            sa1.force()
            sa2.force()
        g.verify()
        g.process()
        assert [sa1.data[i] for i in range(6)] == [0, 0.5, 1.0, 1.5, 2.0, 2.5]
        assert [sa2.data[i] for i in range(6)] == [0, 0, 1, 1, 2, 2]
