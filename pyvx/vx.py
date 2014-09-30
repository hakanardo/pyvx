from pyvx.pyvx import Image, Graph, Context

def CreateContext():
    return Context()


def CreateImage(context, width, height, color):
    return Image(context, width, height, color, None, False)


def CreateGraph(context):
    return Graph(context)


def CreateVirtualImage(graph, width, height, color):
    return Image(graph.context, width, height, color, None, True, graph)


def VerifyGraph(graph):
    return graph.verify()


def ProcessGraph(graph):
    return graph.process()

