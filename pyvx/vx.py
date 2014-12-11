""" 
:mod:`pyvx.vx` --- C-like Python API
==========================================

This module provides the functions specified by the `OpenVX`_ standard.
Please refer to the `OpenVX speficication`_ for a description of the API. The
module name vx is used instead of a vx prefix on all symbols. The initial
example on page 12 of the specification would in python look like this:

.. code-block:: python 

    from pyvx import vx

    context = vx.CreateContext()
    images = [
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_UYVY),
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_U8),
        vx.CreateImage(context, 640, 480, vx.DF_IMAGE_U8),
    ]
    graph = vx.CreateGraph(context)
    virts = [
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
        vx.CreateVirtualImage(graph, 0, 0, vx.DF_IMAGE_VIRT),
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

In cases listed below, the C-API returns data by passing in pointers to the 
functions. In those cases the python functions return multiple values instead.
"""

from pyvx.backend import CoreImage, Context
from pyvx.optimize import OptimizedGraph
from pyvx.nodes import *
from pyvx.inc.vx import *


def CreateContext():
    return Context()


def ReleaseContext(context):
    pass


def CreateImage(context, width, height, color):
    return CoreImage(width, height, color, virtual=False, context=context)


def CreateGraph(context, early_verify=True):
    return OptimizedGraph(context, early_verify)


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

# ========================================================================
# PARAMETER
# ========================================================================


def GetParameterByIndex(node, index):
    return node.parameters[index]


def ReleaseParameter(param):
    return SUCCESS


def SetParameterByIndex(node, index, value):
    setattr(node, node.parameters[index].name, value)
    return SUCCESS


def SetParameterByReference(parameter, value):
    setattr(parameter.node, parameter.name, value)
    return SUCCESS


def QueryParameter(param, attribute):
    """
        status, value = QueryParameter(param, attribute)
    """
    if attribute == PARAMETER_ATTRIBUTE_REF:
        val = getattr(param.node, param.name)
    else:
        val = getattr(param, {PARAMETER_ATTRIBUTE_INDEX: 'index',
                              PARAMETER_ATTRIBUTE_DIRECTION: 'direction',
                              PARAMETER_ATTRIBUTE_TYPE: 'data_type',
                              PARAMETER_ATTRIBUTE_STATE: 'state',
                              }[attribute])
    return SUCCESS, val
