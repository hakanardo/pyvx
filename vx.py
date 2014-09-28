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
        self.graph = graph
        self.producer = None

    def force(self):
        self.virtual = False


class Graph(object):
    def __init__(self, context):
        self.context = context
        self.nodes = []
        self.data_objects = set()

    def _add_node(self, node):
        self.nodes.append(node)
        for d in node.inputs + node.outputs + node.inouts:
            self.data_objects.add(d)

    def verify(self):
        for node in self.nodes:
            # Signle writer
            for d in node.outputs + node.inouts:
                if d.producer is not node:
                    raise MultipleWritersError

            # Bidirection data bot virtual
            for d in node.inouts:
                if d.virtual:
                    raise InvalidGraphError("Bidirection data cant be virtual.")

        # Virtual data produced
        for d in self.data_objects:
            if d.virtual and d.producer is None:
                raise InvalidGraphError("Virtual data never produced.")

        self.schedule()

    def schedule(self):
        for d in self.data_objects:
            d.present = not d.virtual
        for n in self.nodes:
            for d in n.outputs + n.inouts:
                d.present = False
        worklist = self.nodes[:]
        order = []
        while worklist:
            remaining = []
            for n in worklist:
                if all(d.present for d in n.inputs):
                    order.append(n)
                    for d in n.outputs:
                        d.present = True
                else:
                    remaining.append(n)
            if len(worklist) == len(remaining):
                raise InvalidGraphError("Loops not allowed in the graph.")
            worklist = remaining







    def process(self):
        pass

class MultipleWritersError(Exception):
    pass

class InvalidGraphError(Exception):
    pass

class InvalidValueError(Exception):
    pass

class InvalidFormat(Exception):
    pass

class Node(object):
    def _setup(self):
        self.graph._add_node(self)
        for img in self.outputs + self.inouts:
            if img.producer is not None:
                raise MultipleWritersError
            img.producer = self

class ChannelExtractNode(Node):
    def __init__(self, graph, input, channel, output):
        self.graph = graph
        self.channel = channel
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self._setup()

class Gaussian3x3Node(Node):
    def __init__(self, graph, input, output):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self._setup()

class Sobel3x3Node(Node):
    def __init__(self, graph, input, output_x, output_y):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output_x, output_y]
        self.inouts = []
        self._setup()

class MagnitudeNode(Node):
    def __init__(self, graph, grad_x, grad_y, mag):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [mag]
        self.inouts = []
        self._setup()

class PhaseNode(Node):
    def __init__(self, graph, grad_x, grad_y, orientation):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [orientation]
        self.inouts = []
        self._setup()

class AccumulateImageNode(Node):
    def __init__(self, graph, input, accum):
        self.graph = graph
        self.inputs = [input]
        self.outputs = []
        self.inouts = [accum]
        self._setup()
        
        