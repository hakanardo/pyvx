import vx

context = vx.Context()
context.current_graph = None


class Graph(vx.Graph):

    def __init__(self):
        vx.Graph.__init__(self, context)

    def __enter__(self):
        assert context.current_graph is None
        context.current_graph = self

    def __exit__(self, *args):
        assert context.current_graph is self
        context.current_graph = None


class Image(vx.Image):

    def __init__(self, width, height, color, virtual=False, graph=None):
        vx.Image.__init__(self, context, width, height, color,
                          virtual, graph)

    @property
    def channel_y(self):
        return ChannelExtract(self, vx.CHANNEL_Y)


def VirtualImage(w=0, h=0):
    return Image(w, h, vx.FOURCC_VIRT, True, context.current_graph)


def ChannelExtract(input, channel):
    output = VirtualImage()
    vx.ChannelExtractNode(context.current_graph,
                          input, channel, output)
    return output


def Gaussian3x3(input):
    output = VirtualImage()
    vx.Gaussian3x3Node(context.current_graph, input, output)
    return output


def Sobel3x3(input):
    dx, dy = VirtualImage(), VirtualImage()
    vx.Sobel3x3Node(context.current_graph, input, dx, dy)
    return dx, dy


def Magnitude(grad_x, grad_y):
    mag = VirtualImage()
    vx.MagnitudeNode(context.current_graph, grad_x, grad_y, mag)
    return mag


def Phase(grad_x, grad_y):
    ph = VirtualImage()
    vx.PhaseNode(context.current_graph, grad_x, grad_y, ph)
    return ph


def AccumulateImage(input):
    accum = VirtualImage()
    vx.VirtualImageNode(context.current_graph, input, accum)
    return accum

if __name__ == '__main__':
    from imgpy.io import Mplayer, view
    from array import array
    video = Mplayer("/usr/share/cognimatics/data/facit/events/passanger/bustst1-M3014-180.mjpg", True)
    frame = video.next()
    w, h = frame.width, frame.height    

    g = Graph()
    with g:
        img = Image(w, h, vx.FOURCC_U8)
        gimg = Gaussian3x3(img)
        gimg.force()
        # dx, dy = Sobel3x3(gimg)
        # mag = Magnitude(dx, dy)
        # phi = Phase(dx, dy)
    g.verify()

    for frame in video:
        img.cdata[0:len(frame.data)] = frame.data[:]
        g.process()
        frame.data[:] = array('B', gimg.cdata[0:len(frame.data)])
        view(frame)
