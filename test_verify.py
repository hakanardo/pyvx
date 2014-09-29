import py.test
from pyvx import *


class TestVerify(object):

    def test_single_writer(self):
        g = Graph()
        img = Image(640, 480, vx.FOURCC_U8)
        out = VirtualImage()
        vx.Gaussian3x3Node(g, img, out)
        with py.test.raises(vx.MultipleWritersError):
            vx.Gaussian3x3Node(g, img, out)
        with py.test.raises(vx.MultipleWritersError):
            g.verify()

    def test_single_writer_inout(self):
        g = Graph()
        img = Image(640, 480, vx.FOURCC_U8)
        out = Image(640, 480, vx.FOURCC_U8)
        vx.AccumulateImageNode(g, img, out)
        with py.test.raises(vx.MultipleWritersError):
            vx.Gaussian3x3Node(g, img, out)
        with py.test.raises(vx.MultipleWritersError):
            g.verify()

    def test_no_producer(self):
        g = Graph()
        img = VirtualImage(640, 480, vx.FOURCC_U8)
        out2 = VirtualImage()
        vx.Gaussian3x3Node(g, img, out2)
        with py.test.raises(vx.InvalidGraphError):
            g.verify()

    def test_loop(self):
        g = Graph()
        out1 = VirtualImage(640, 480, vx.FOURCC_U8)
        out2 = VirtualImage()
        vx.Gaussian3x3Node(g, out1, out2)
        vx.Gaussian3x3Node(g, out2, out1)
        with py.test.raises(vx.InvalidGraphError):
            g.verify()

    def test_virtual_inout(self):
        g = Graph()
        a, b = Image(640, 480, vx.FOURCC_U8), VirtualImage()
        with py.test.raises(vx.InvalidGraphError):
            vx.AccumulateImageNode(g, a, b)
        with py.test.raises(vx.InvalidGraphError):
            g.verify()

    def test_verification_order(self):
        g = vx.Graph(context, False)
        img = Image(640, 480, vx.FOURCC_U8)
        out = VirtualImage()
        out2 = VirtualImage()
        vx.Gaussian3x3Node(g, out, out2)
        vx.Gaussian3x3Node(g, img, out)
        g.verify()
