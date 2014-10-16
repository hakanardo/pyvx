from pyvx import *
from array import array

class TestPyVx(object):
    def test_gaussian(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(12)))
            gimg = Gaussian3x3(img)
            gimg.force()
        g.verify()
        g.process()
        assert gimg.data[4] == 4
        assert gimg.data[7] == 7

    def test_replicate_border(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(12)))
            gimg = Gaussian3x3(img)
            gimg.producer.border_mode = BORDER_MODE_REPLICATE
            gimg.force()
        g.verify()
        g.process()
        assert gimg.data[0] == 1
        assert gimg.data[1] == 1
        assert gimg.data[11] == 10

    def test_add_truncate(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(12)))
            sa = img + img
            sa.force()
        g.verify()
        g.process()
        for i in range(12):
            assert sa.data[i] == 2*i

    def test_add_saturate8(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', [1, 2, 100, 200] * 3))
            sa = img + img
            sa_sat = img + img
            sa_sat.producer.convert_policy = CONVERT_POLICY_SATURATE
            sa.force()
            sa_sat.force()
        g.verify()
        g.process()
        assert sa.data[0] == 2
        assert sa.data[1] == 4
        assert sa.data[2] == 200
        assert sa.data[3] == 400 - 256
        assert sa_sat.data[0] == 2
        assert sa_sat.data[1] == 4
        assert sa_sat.data[2] == 200
        assert sa_sat.data[3] == 255

    def test_add_saturate16(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_S16, array('h', [1, 2, 10000, 20000] * 3))
            sa = img + img
            sa_sat = img + img
            sa_sat.producer.convert_policy = CONVERT_POLICY_SATURATE
            sa.force()
            sa_sat.force()
        g.verify()
        g.process()
        assert sa.data[0] == 2
        assert sa.data[1] == 4
        assert sa.data[2] == 20000
        assert sa.data[3] == 40000 - 2**16
        assert sa_sat.data[0] == 2
        assert sa_sat.data[1] == 4
        assert sa_sat.data[2] == 20000
        assert sa_sat.data[3] == 2**15 - 1

    def test_channel_extract_rgb(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_RGB, array('B', range(12*3)))
            rimg = img.channel_r
            rimg.force()
            gimg = img.channel_g
            gimg.force()
            bimg = img.channel_b
            bimg.force()
        g.verify()
        g.process()
        for i in range(12):
            assert rimg.data[i] == 3*i
            assert gimg.data[i] == 3*i + 1
            assert bimg.data[i] == 3*i + 2

    def test_channel_extract_uyvu(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_UYVY, array('B', range(12*2)))
            yimg = img.channel_y
            yimg.force()
            uimg = img.channel_u
            uimg.force()
            vimg = img.channel_v
            vimg.force()
        g.verify()
        g.process()
        assert [yimg.data[i] for i in range(7)] == [1,3,5,7,9,11,13]
        assert [uimg.data[i] for i in range(7)] == [0,0,4,4,8,8,12]
        assert [vimg.data[i] for i in range(7)] == [2,2,6,6,10,10,14]

    def test_mul_truncate(self):
        g = Graph()
        with g:
            img1 = Image(3, 4, FOURCC_U8, array('B', range(12)))
            img2 = Image(3, 4, FOURCC_U8, array('B', [2]*12))
            sa = img1 * img2
            sa.producer.scale = 0.25
            sa.force()
        g.verify()
        g.process()
        for i, expected in enumerate([0,0,1,1,2,2,3,3,4,4,5,5]):
            assert sa.data[i] == expected

    def test_mul_round_even(self):
        g = Graph()
        with g:
            img1 = Image(3, 4, FOURCC_U8, array('B', range(12)))
            img2 = Image(3, 4, FOURCC_U8, array('B', [2]*12))
            sa = img1 * img2
            sa.producer.scale = 0.25
            sa.producer.round_policy = ROUND_POLICY_TO_NEAREST_EVEN
            sa.force()
        g.verify()
        g.process()
        for i, expected in enumerate([0,0,1,2,2,2,3,4,4,4,5,6]):
            assert sa.data[i] == expected

    def test_arithmetic1(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(1,13)))
            sa1 = img + img - 2 * img + 1
            sa2 = (img * img + 5) / img - img
            sa1.force()
            sa2.force()
        g.verify()
        g.process()
        for i in range(12):
            assert sa1.data[i] == 1
            assert sa2.data[i] == 5 / (i + 1)

    def test_arithmetic2(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(1,13)))
            sa1 = img | (img + 2) << 3 + 0xF
            sa2 = ((img & sa1**2 ) >> 1) ^ img 
            sa3 = sa1 % img
            sa1.force()
            sa2.force()
            sa3.force()
        g.verify()
        g.process()
        for i in range(12):
            img = i + 1
            assert sa1.data[i] == img | (img + 2) << 3 + 0xF
            assert sa2.data[i] == ((img & sa1.data[i]**2 ) >> 1) ^ img
            assert sa3.data[i] == sa1.data[i] % img

    def test_compare(self):
        g = Graph()
        with g:
            img = Image(3, 4, FOURCC_U8, array('B', range(12)))
            sa1 = (1 < img) & (img <= 2)
            sa2 = img == 3
            sa3 = img != 4
            sa1.force()
            sa2.force()
            sa3.force()
        g.verify()
        g.process()
        for i in range(12):
            img = i
            assert sa1.data[i] == (1 < img <= 2)
            assert sa2.data[i] == (img == 3)
            assert sa3.data[i] == (img != 4)

    def test_play(self):
        g = Graph()
        with g:
            img = Play("test/test.avi")
        g.verify()
        g.process()
        assert img.width == 320
        assert img.height == 240
        fcnt = 1
        while g.process() == SUCCESS:
            fcnt += 1
        assert fcnt > 100
