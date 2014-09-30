from pyvx.backend import Image, Graph, Context

def CreateContext():
    return Context()


def CreateImage(context, width, height, color):
    return Image(width, height, color, virtual=False, context=context)


def CreateGraph(context):
    return Graph(context)


def CreateVirtualImage(graph, width, height, color):
    return Image(width, height, color, virtual=True, graph=graph)


def VerifyGraph(graph):
    return graph.verify()


def ProcessGraph(graph):
    return graph.process()

