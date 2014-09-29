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


class FOURCC_VIRT:
    pass


class FOURCC_RGB:
    pass


class FOURCC_UYVY:
    pass


class FOURCC_U8:
    pass


class CHANNEL_0:
    pass


class CHANNEL_1:
    pass


class CHANNEL_2:
    pass


class CHANNEL_3:
    pass


class CHANNEL_Y:
    pass


class Context(object):
    pass


class Image(object):

    def __init__(self, context, width, height, color, 
                 virtual=False, graph=None):
        self.context = context
        self.width = width
        self.height = height
        self.color = color
        self.virtual = virtual
        self.graph = graph
        self.producer = None

    def force(self):
        self.virtual = False

    def ensure(self, width, height, color):
        if self.width == 0:
            self.width = width
        if self.height == 0:
            self.height = height
        if self.color == FOURCC_VIRT:
            self.color = color
        if self.width != width or self.height != height or self.color != color:
            raise InvalidFormatError


class Graph(object):

    def __init__(self, context, early_verify=True):
        self.context = context
        self.nodes = []
        self.data_objects = set()
        self.early_verify = early_verify

    def _add_node(self, node):
        self.nodes.append(node)
        for d in node.inputs + node.outputs + node.inouts:
            self.data_objects.add(d)

    def verify(self):
        self.nodes = self.schedule()

        for node in self.nodes:
            node.do_verify()

        # Virtual data produced
        for d in self.data_objects:
            if d.virtual and d.producer is None:
                raise InvalidGraphError("Virtual data never produced.")

    def schedule(self):
        for d in self.data_objects:
            d.present = not d.virtual
        for n in self.nodes:
            for d in n.outputs + n.inouts:
                d.present = False
        worklist = self.nodes[:]
        inorder = []
        while worklist:
            remaining = []
            for n in worklist:
                if all(d.present for d in n.inputs):
                    inorder.append(n)
                    for d in n.outputs:
                        d.present = True
                else:
                    remaining.append(n)
            if len(worklist) == len(remaining):
                raise InvalidGraphError("Loops not allowed in the graph.")
            worklist = remaining
        return inorder

    def process(self):
        pass


class MultipleWritersError(Exception):
    pass


class InvalidGraphError(Exception):
    pass


class InvalidValueError(Exception):
    pass


class InvalidFormatError(Exception):
    pass


class Node(object):

    def setup(self):
        self.graph._add_node(self)
        for d in self.outputs + self.inouts:
            if d.producer is None:
                d.producer = self
        if self.graph.early_verify:
            self.do_verify()

    def do_verify(self):
        # Signle writer
        for d in self.outputs + self.inouts:
            if d.producer is not self:
                raise MultipleWritersError

        # Bidirection data not virtual
        for d in self.inouts:
            if d.virtual:
                raise InvalidGraphError("Bidirection data cant be virtual.")

        for d in self.inputs:
            if not d.width or not d.height:
                raise InvalidFormatError
        self.verify()


class ChannelExtractNode(Node):

    def __init__(self, graph, input, channel, output):
        self.graph = graph
        self.channel = channel
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        if i.color == FOURCC_UYVY and self.channel == CHANNEL_Y:
            pass
        else:
            raise InvalidFormatError(
                'Cant extract channel %s from %s image.' % (self.channel,
                                                            i.color))
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class Gaussian3x3Node(Node):

    def __init__(self, graph, input, output):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class Sobel3x3Node(Node):

    def __init__(self, graph, input, output_x, output_y):
        self.graph = graph
        self.inputs = [input]
        self.outputs = [output_x, output_y]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class MagnitudeNode(Node):

    def __init__(self, graph, grad_x, grad_y, mag):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [mag]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)


class PhaseNode(Node):

    def __init__(self, graph, grad_x, grad_y, orientation):
        self.graph = graph
        self.inputs = [grad_x, grad_y]
        self.outputs = [orientation]
        self.inouts = []
        self.setup()

    def verify(self):
        i = self.inputs[0]
        self.outputs[0].ensure(i.width, i.height, FOURCC_U8)
        self.outputs[1].ensure(i.width, i.height, FOURCC_U8)


class AccumulateImageNode(Node):

    def __init__(self, graph, input, accum):
        self.graph = graph
        self.inputs = [input]
        self.outputs = []
        self.inouts = [accum]
        self.setup()

    def verify(self):
        pass
