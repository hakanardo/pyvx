""" 
:mod:`pyvx.capi` --- C API
==========================================

This module allows the use of this python implementation as an `OpenVX`_ backend 
from a C program. A shared library is provided that embeds python and exports a C API
following the `OpenVX`_ specification. That way the C program does not need to
be aware of the fact that python is used. Also, any C program following the
`OpenVX`_ specification should be compilable with this backend.

.. code-block:: bash

  sudo python -mpyvx.capi build /usr/local/

This will install `libopenvx.so*` into `/usr/local/lib` and place the
`OpenVX`_ headers in `/usr/local/include/VX`.

.. _`OpenVX`: https://www.khronos.org/openvx

"""

from codegen import PythonApi, Enum, Reference
import codegen
from pyvx import vx
from pyvx.types import enum2ctype

from pyvx import __version_info__, __version__
major, minor, _ = __version_info__
soversion = '%d.%d' % (major, minor)

def export(signature, add_ret_to_arg=0, exception_return=vx.FAILURE, **kwargs):
    return codegen.export(signature, add_ret_to_arg, exception_return=exception_return, **kwargs)



class OpenVxApi(object):
    wrapped_reference_types = ['vx_context', 'vx_image', 'vx_graph', 
                               'vx_node', 'vx_parameter', 'vx_reference',
                               'vx_scalar']
    setup = ["import sys",
             "sys.path = ['.'] + sys.path",
             "import pyvx",
             "if pyvx.__version__ != %r:" % __version__,
             "    print 'Version mismatch. Please reinstall pyvx and/or recompile your binary. Exiting...'",
             "    exit()",
             "from pyvx.capi import OpenVxApi",
             "from pyvx.codegen import PythonApi",
             "from pyvx.inc.vx import ffi",
             "api = PythonApi(OpenVxApi, ffi).load()"]

    @export("vx_context()", add_ret_to_arg=None)
    def vxCreateContext():
        return vx.CreateContext()

    @export("vx_image(vx_context, uint32_t, uint32_t, vx_df_image)")
    def vxCreateImage(context, width, height, color):
        return vx.CreateImage(context, width, height, color)

    @export("vx_graph(vx_context)")
    def vxCreateGraph(context):
        return vx.CreateGraph(context, early_verify=False)

    @export("vx_image(vx_graph, uint32_t, uint32_t, vx_df_image)")
    def vxCreateVirtualImage(graph, width, height, color):
        return vx.CreateVirtualImage(graph, width, height, color)

    @export("vx_status(vx_graph)")
    def vxVerifyGraph(graph):
        return vx.VerifyGraph(graph)

    @export("vx_status(vx_graph)")
    def vxProcessGraph(graph):
        return vx.ProcessGraph(graph)
    
    @export("vx_status(vx_context *)")
    def vxReleaseContext(context):
        context_obj = OpenVxApi.pyapi.retrive(context[0])
        for r in context_obj.references:
            OpenVxApi.pyapi.discard(r)
        context_obj.clear_references()
        OpenVxApi.pyapi.discard(context[0])
        context[0] = OpenVxApi.pyapi.ffi.NULL
        return vx.SUCCESS

    @export("vx_node(vx_graph, vx_image, vx_enum, vx_image)")
    def vxChannelExtractNode(graph, input, channel, output):
        return vx.ChannelExtractNode(graph, input, channel, output)

    @export("vx_node(vx_graph, vx_image, vx_image)")
    def vxGaussian3x3Node(graph, input, output):
        return vx.Gaussian3x3Node(graph, input, output)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxSobel3x3Node(graph, input, output_x, output_y):
        return vx.Sobel3x3Node(graph, input, output_x, output_y)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxMagnitudeNode(graph, grad_x, grad_y, mag):
        return vx.MagnitudeNode(graph, grad_x, grad_y, mag)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxPhaseNode(graph, grad_x, grad_y, orientation):
        return vx.PhaseNode(graph, grad_x, grad_y, orientation)

    @export("vx_node(vx_graph, char *, vx_image)")
    def vxPlayNode(graph, fn, output):
        return vx.PlayNode(graph, OpenVxApi.pyapi.ffi.string(fn), output)

    @export("vx_node(vx_graph, vx_image, char *)")
    def vxShowNode(graph, input, name):
        return vx.ShowNode(graph, input, name)

    @export("vx_status(vx_graph, vx_parameter)")
    def vxAddParameterToGraph(graph, parameter):
        return vx.AddParameterToGraph(graph, parameter)

    @export("vx_status(vx_graph, vx_uint32, vx_reference)")
    def vxSetGraphParameterByIndex(graph, index, value):
        return vx.SetGraphParameterByIndex(graph, index, value)

    @export("vx_parameter(vx_graph, vx_uint32)")
    def vxGetGraphParameterByIndex(graph, index):
        return vx.GetGraphParameterByIndex(graph, index)


    # ========================================================================
    # PARAMETER
    # ========================================================================
    @export("vx_parameter(vx_node, vx_uint32 index)")
    def vxGetParameterByIndex(node, index):
        return vx.GetParameterByIndex(node, index)
    
    @export("vx_status(vx_parameter *)")
    def vxReleaseParameter(param):
        param_obj = OpenVxApi.pyapi.retrive(param[0])
        OpenVxApi.pyapi.discard(param[0])
        param[0] = OpenVxApi.pyapi.ffi.NULL
        return vx.ReleaseParameter(param_obj)
    
    @export('vx_status(vx_node, vx_uint32, vx_reference)')    
    def vxSetParameterByIndex(node, index, value):
        return vx.SetParameterByIndex(node, index, value)

    @export('vx_status(vx_parameter, vx_reference)')
    def vxSetParameterByReference(parameter, value):
        return vx.SetParameterByReference(parameter, value)

    @export("vx_status(vx_parameter, vx_enum, void *, vx_size)")
    def vxQueryParameter(param, attribute, ptr, size):
        attr_type = {vx.PARAMETER_ATTRIBUTE_INDEX: 'vx_uint32',
                     vx.PARAMETER_ATTRIBUTE_DIRECTION: 'vx_enum',
                     vx.PARAMETER_ATTRIBUTE_TYPE: 'vx_enum',
                     vx.PARAMETER_ATTRIBUTE_STATE: 'vx_enum',
                     vx.PARAMETER_ATTRIBUTE_REF: 'vx_reference'}

        if attribute not in attr_type:
            return vx.FAILURE
        if size != OpenVxApi.pyapi.ffi.sizeof(attr_type[attribute]):
            return vx.FAILURE
        status, value = vx.QueryParameter(param, attribute)
        ptr = OpenVxApi.pyapi.ffi.cast(attr_type[attribute] + "*", ptr)
        if attr_type[attribute] == 'vx_reference':
            ptr[0] = OpenVxApi.pyapi.store(value)
        else:
            ptr[0] = value
        return status

    # ==============================================================================
    # SCALAR
    # =============================================================================

    @export("vx_scalar(vx_context, vx_enum, void *)")
    def vxCreateScalar(context, data_type, ptr):
        ctype = enum2ctype[data_type]
        ptr = OpenVxApi.pyapi.ffi.cast(ctype + '*', ptr)
        return vx.CreateScalar(context, data_type, ptr[0])

    @export("vx_status(vx_scalar *)")
    def vxReleaseScalar(scalar):
        scalar_obj = OpenVxApi.pyapi.retrive(scalar[0])
        scalar[0] = OpenVxApi.pyapi.ffi.NULL
        return vx.ReleaseScalar(scalar_obj)

    @export("vx_status(vx_scalar, vx_enum , void *, vx_size)")
    def vxQueryScalar(scalar, attribute, ptr, size):
        if size != OpenVxApi.pyapi.ffi.sizeof('vx_enum'):
            return FAILURE
        ptr = OpenVxApi.pyapi.ffi.cast("vx_enum *", ptr)
        status, value = vx.QueryScalar(scalar, attribute)
        ptr[0] = value
        return status


    @export("vx_status(vx_scalar, void *)")
    def vxAccessScalarValue(ref, ptr):
        status, value = vx.AccessScalarValue(ref)
        ctype = enum2ctype[ref.vxtype]
        ptr = OpenVxApi.pyapi.ffi.cast(ctype + "*", ptr)
        ptr[0] = value
        return status

    @export("vx_status(vx_scalar, void *)")
    def vxCommitScalarValue(ref, ptr):
        ctype = enum2ctype[ref.vxtype]
        ptr = OpenVxApi.pyapi.ffi.cast(ctype + "*", ptr)
        return vx.CommitScalarValue(ref, ptr[0])

    # ========================================================================
    # FOR TESTS
    # ========================================================================
    @export("int(vx_reference, vx_reference)")
    def same_pyobj(ref1, ref2):
        return ref1 is ref2



def build(prefix='/usr/local'):
    from pyvx.inc.vx import ffi
    import os
    from distutils.dir_util import copy_tree

    libdir = os.path.join(prefix, 'lib')
    incdir = os.path.join(prefix, 'include', 'VX')
    if not os.path.exists(libdir):
        os.makedirs(libdir)
    if not os.path.exists(incdir):
        os.makedirs(incdir)

    api = PythonApi(OpenVxApi, ffi)
    api.build('openvx', __version__, soversion, libdir)
    srcdir = os.path.join(os.path.dirname(__file__), 'inc', 'headers', 'VX')
    copy_tree(srcdir, incdir)
    os.system('ldconfig')

    return api.library_names

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'build' and len(sys.argv) in (2,3):
        build(*sys.argv[2:])
    else:
        print 'Usage: %s build [<prefix>]' % sys.argv[0]
