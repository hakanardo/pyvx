import vx

context = vx.Context()
context.current_graph = None

class Graph(vx.Graph):
    def __init__(self):
        vx.Graph.__init__(self, context)

    def __enter__(self):
        assert context.current_graph is None
        context.current_graph = self._graph

    def __exit__(self, *args):
        assert context.current_graph is self._graph
        context.current_graph = None


class Image(vx.Image):
    def __init__(self, width, height, color, virtual=False, graph=None):
        vx.Image.__init__(self, context, width, height, color, 
                          virtual, graph)

    @property
    def channel_y(self):
        return ChannelExtract(self, vx.CHANNEL_Y)

def VirtualImage():
    return Image(0, 0, vx.FOURCC_VIRT, True, context.current_graph)

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
    g = Graph()
    with g:
        img = Image(640, 480, vx.FOURCC_UYVY)
        dx, dy = Sobel3x3(Gaussian3x3(img))
        mag = Magnitude(dx, dy)
        phi = Phase(dx, dy)
    g.verify()
    g.process()
