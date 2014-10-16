from pyvx import *
from imgpy.io import Mplayer, view
import time

def main(fn):
    video = Mplayer(fn, True)
    frame = video.next()
    w, h = frame.width, frame.height
    mag_res = frame.new()    
    phi_res = frame.new()    

    with Graph() as g:
        img = Image(w, h, FOURCC_U8, data=frame)
        gimg = Gaussian3x3(img)
        dx, dy = Sobel3x3(gimg)
        mag = Magnitude(dx, dy)
        phi = Phase(dx, dy)
        mag.color = FOURCC_U8
        mag.force(mag_res)
        phi.force(phi_res)
    g.verify()

    for new_frame in video:
        frame.data[:] = new_frame.data
        g.process()
        if False:
            view(mag_res)
        else:
            view(phi_res)
        time.sleep(0.01)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])