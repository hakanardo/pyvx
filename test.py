from imgpy.io import Mplayer, view
from pyvx import *

def main():
    video = Mplayer("/usr/share/cognimatics/data/facit/events/passanger/bustst1-M3014-180.mjpg", True)
    frame = video.next()
    w, h = frame.width, frame.height
    res = frame.new()    

    g = Graph()
    with g:
        img = Image(w, h, FOURCC_U8, data=frame)
        gimg = Gaussian3x3(img)
        gimg.producer.border_mode = BORDER_MODE_REPLICATE
        gimg.force(res)
        # dx, dy = Sobel3x3(gimg)
        # mag = Magnitude(dx, dy)
        # phi = Phase(dx, dy)
    g.verify()

    for new_frame in video:
        frame.data[:] = new_frame.data
        g.process()
        view(res)

if __name__ == '__main__':
    main()