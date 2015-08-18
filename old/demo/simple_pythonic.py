from pyvx import *

with Graph() as g:
    img = Image(640, 480, DF_IMAGE_UYVY)
    smooth = Gaussian3x3(img.channel_y)
    dx, dy = Sobel3x3(smooth)
    mag = Magnitude(dx, dy)
    phi = Phase(dx, dy)
    mag.force()
    phi.force()
g.verify()
g.process()


with Graph() as g:
    img = Image(640, 480, DF_IMAGE_UYVY)
    dx, dy = Sobel3x3(img.channel_y)
    mag = dx*dx + dy*dy
    mag.color = DF_IMAGE_U32
    mag.force()
g.verify()
g.process()
