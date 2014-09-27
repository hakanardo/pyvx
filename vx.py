def CreateContext():
    return Context()

def CreateImage(context, width, height, color):
    return Image(context, width, height, color, False)

def CreateGraph(context):
    return Graph(context)

def CreateVirtualImage(graph, width, height, color):
    return Image(graph.context, width, height, color, True, graph)

def VerifyGraph(graph):
    return graph.verify()

def ProcessGraph(graph):
    return graph.process()

class FOURCC_VIRT: pass
class FOURCC_U8: pass
class FOURCC_RGB: pass
class FOURCC_UYVY: pass


class CHANNEL_0: pass
class CHANNEL_1: pass
class CHANNEL_2: pass
class CHANNEL_3: pass
class CHANNEL_Y: pass


class Context(object):   
    pass         

class Image(object):
    def __init__(self, context, width, height, color, virtual=False, graph=None):
        self.context = context
        self.width = width
        self.height = height
        self.color = color
        self.virtual = virtual
        self.graph = None

    def force(self):
        self.virtual = False


class Graph(object):
    def __init__(self, context):
        self.context = context
        self.nodes = []

    def _add_node(self, node):
        self.nodes.append(node)

    def verify(self):
        print self.nodes

    def process(self):
        pass

class Node(object):
    pass

class ChannelExtractNode(Node):
    def __init__(self, graph, input, channel, output):
        self.graph = graph
        self.channel = channel
        self.inputs = [input]
        self.outputs = [output]
        graph._add_node(self)

class Gaussian3x3Node(Node):
    def __init__(self, graph, input, output):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output]
        graph._add_node(self)

class Sobel3x3Node(Node):
    def __init__(self, graph, input, output_x, output_y):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output_x, output_y]
        graph._add_node(self)

class MagnitudeNode(Node):
    def __init__(self, graph, grad_x, grad_y, mag):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [mag]
        graph._add_node(self)

class PhaseNode(object):
    def __init__(self, graph, grad_x, grad_y, orientation):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [orientation]
        graph._add_node(self)
        
        
        
        