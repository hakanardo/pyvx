""" 
:mod:`pyvx.vx` --- Standards compliant Python API
=================================================

This module provides the functions as specified by the `OpenVX`_ standard.
Please refer to the `OpenVX speficication`_ for a description of the API. The
module name vx is used instead of a vx prefix on all symbols. The initial
example on page 12 of that specification would in python look like this:

.. code-block:: python 

    from pyvx import vx

    context = vx.CreateContext()
    images = [
        vx.CreateImage(context, 640, 480, vx.FOURCC_UYVY),
        vx.CreateImage(context, 640, 480, vx.FOURCC_U8),
        vx.CreateImage(context, 640, 480, vx.FOURCC_U8),
    ]
    graph = vx.CreateGraph(context)
    virts = [
        vx.CreateVirtualImage(graph, 0, 0, vx.FOURCC_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.FOURCC_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.FOURCC_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.FOURCC_VIRT),
    ]
    vx.ChannelExtractNode(graph, images[0], vx.CHANNEL_Y, virts[0])
    vx.Gaussian3x3Node(graph, virts[0], virts[1])
    vx.Sobel3x3Node(graph, virts[1], virts[2], virts[3])
    vx.MagnitudeNode(graph, virts[2], virts[3], images[1])
    vx.PhaseNode(graph, virts[2], virts[3], images[2])
    status = vx.VerifyGraph(graph)
    if status == vx.SUCCESS:
        status = vx.ProcessGraph(graph)
    else:
        print("Verification failed.")
    vx.ReleaseContext(context)


.. _`OpenVX`: https://www.khronos.org/openvx
.. _`OpenVX speficication`: https://www.khronos.org/registry/vx/specs/OpenVX_1.0_Provisional_Specifications.zip
"""

from pyvx.backend import CoreImage, Context
from pyvx.optimize import OptimizedGraph
from pyvx.types import *
from pyvx.nodes import *


def CreateContext():
    return Context()

def ReleaseContext(context):
    pass


def CreateImage(context, width, height, color):
    return CoreImage(width, height, color, virtual=False, context=context)


def CreateGraph(context):
    return OptimizedGraph(context)


def CreateVirtualImage(graph, width, height, color):
    return CoreImage(width, height, color, virtual=True, graph=graph)


def VerifyGraph(graph):
    try:
        graph.verify()
    except VerificationError as e:
        return e.__class__
    return SUCCESS

def ProcessGraph(graph):
    return graph.process()

