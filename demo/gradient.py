from pyvx import *


def main(fn="v4l2:///dev/video0"):
    with Graph() as g:
        cimg = Play(fn)
        yuv = ColorConvert(cimg)
        yuv.color = DF_IMAGE_YUYV
        img = ChannelExtract(yuv, CHANNEL_Y)
        gimg = Gaussian3x3(img)
        dx, dy = Sobel3x3(gimg)
        mag = Magnitude(dx, dy)
        phi = Phase(dx, dy)
        mag.color = DF_IMAGE_U8
        if True:
            vis = ChannelCombine(mag, mag, mag)
        else:
            vis = ChannelCombine(phi, phi, phi)
        vis.color = DF_IMAGE_RGB
        Show(vis)
    g.verify()
    while g.process() == SUCCESS:
        pass

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
