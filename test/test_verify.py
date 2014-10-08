import py.test
from pyvx import *

class TestVerify(object):

    def test_single_writer(self):
        g = Graph()
        img = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        out = Image(graph=g)
        Gaussian3x3Node(g, img, out)
        with py.test.raises(MultipleWritersError):
            Gaussian3x3Node(g, img, out)
        with py.test.raises(MultipleWritersError):
            g.verify()

    def test_single_writer_inout(self):
        g = Graph()
        img = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        out = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        AccumulateImageNode(g, img, out)
        with py.test.raises(MultipleWritersError):
            Gaussian3x3Node(g, img, out)
        with py.test.raises(MultipleWritersError):
            g.verify()

    def test_no_producer(self):
        g = Graph()
        img = Image(640, 480, FOURCC_U8, graph=g, virtual=True)
        out2 = Image(graph=g)
        Gaussian3x3Node(g, img, out2)
        with py.test.raises(InvalidGraphError):
            g.verify()

    def test_loop(self):
        g = Graph()
        out1 = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        out2 = Image(graph=g)
        Gaussian3x3Node(g, out1, out2)
        Gaussian3x3Node(g, out2, out1)
        with py.test.raises(InvalidGraphError):
            g.verify()

    def test_virtual_inout(self):
        g = Graph()
        a = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        b = Image(graph=g)
        with py.test.raises(InvalidGraphError):
            AccumulateImageNode(g, a, b)
        with py.test.raises(InvalidGraphError):
            g.verify()

    def test_verification_order(self):
        g = Graph(early_verify=False)
        img = Image(640, 480, FOURCC_U8, context=Graph.default_context)
        out = Image(graph=g)
        out2 = Image(graph=g)
        Gaussian3x3Node(g, out, out2)
        Gaussian3x3Node(g, img, out)
        g.verify()

    def test_channel_extract(self):
        g = Graph()
        with g:
            img = Image(640, 480, FOURCC_U8)
            with py.test.raises(InvalidFormatError):
                ChannelExtract(img, CHANNEL_R)
            img = Image(640, 480, FOURCC_RGB)
            with py.test.raises(InvalidFormatError):
                ChannelExtract(img, CHANNEL_U)
            ChannelExtract(img, CHANNEL_R)

