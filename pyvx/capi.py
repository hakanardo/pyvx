from codegen import PythonApi, Enum, Reference
import codegen
from pyvx import *


def export(signature, add_ret_to_arg=0, **kwargs):
    return codegen.export(signature, add_ret_to_arg, **kwargs)



class OpenVxApi(object):
    cdef = """
        typedef enum {
            VX_ERROR_MULTIPLE_WRITERS, VX_ERROR_INVALID_GRAPH, 
            VX_ERROR_INVALID_VALUE, VX_ERROR_INVALID_FORMAT,
            VX_SUCCESS
        } vx_status;
    """
    
    vx_context = Reference()
    vx_image = Reference()
    vx_graph = Reference()
    vx_node = Reference()

    vx_fourcc = Enum(FOURCC_VIRT, FOURCC_RGB, FOURCC_RGBX, FOURCC_UYVY,
                     FOURCC_YUYV, FOURCC_U8, FOURCC_S8, FOURCC_U16, 
                     FOURCC_S16, FOURCC_U32, FOURCC_S32)
    vx_channel = Enum(CHANNEL_0, CHANNEL_1, CHANNEL_2, CHANNEL_3,
                      CHANNEL_R, CHANNEL_G, CHANNEL_B, CHANNEL_A,
                      CHANNEL_Y, CHANNEL_U, CHANNEL_V, prefix="VX_")

    @export("vx_context()", add_ret_to_arg=None)
    def vxCreateContext():
        return Context()

    @export("vx_image(vx_context, uint32_t, uint32_t, vx_fourcc)")
    def vxCreateImage(context, width, height, color):
        return Image(width, height, color, context=context)

    @export("vx_graph(vx_context)")
    def vxCreateGraph(context):
        return Graph(context, early_verify=False)

    @export("vx_image(vx_graph, uint32_t, uint32_t, vx_fourcc)")
    def vxCreateVirtualImage(graph, width, height, color):
        return Image(width, height, color, graph=graph, virtual=True)

    @export("vx_node(vx_graph, vx_image, vx_channel, vx_image)")
    def vxChannelExtractNode(graph, input, channel, output):
        return ChannelExtractNode(graph, input, channel, output)

    @export("vx_node(vx_graph, vx_image, vx_image)")
    def vxGaussian3x3Node(graph, input, output):
        return Gaussian3x3Node(graph, input, output)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxSobel3x3Node(graph, input, output_x, output_y):
        Sobel3x3Node(graph, input, output_x, output_y)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxMagnitudeNode(graph, grad_x, grad_y, mag):
        MagnitudeNode(graph, grad_x, grad_y, mag)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxPhaseNode(graph, grad_x, grad_y, orientation):
        PhaseNode(graph, grad_x, grad_y, orientation)

    @export("vx_status(vx_graph)")
    def vxVerifyGraph(graph):
        try:
            graph.verify()
        except InvalidGraphError:
            return OpenVxApi.pyapi.lib.VX_ERROR_INVALID_GRAPH
        except InvalidValueError:
            return OpenVxApi.pyapi.lib.VX_ERROR_INVALID_VALUE
        except InvalidFormatError:
            return OpenVxApi.pyapi.lib.VX_ERROR_INVALID_FORMAT
        except MultipleWritersError: 
            return OpenVxApi.pyapi.lib.VX_ERROR_MULTIPLE_WRITERS
        return OpenVxApi.pyapi.lib.VX_SUCCESS

    @export("vx_status(vx_graph)")
    def vxProcessGraph(graph):
        graph.process()
        return OpenVxApi.pyapi.lib.VX_SUCCESS
    
    @export("void(vx_context *)", retrive_args=False)
    def vxReleaseContext(context):
        context_obj = OpenVxApi.pyapi.retrive(context[0])
        for r in context_obj.references:
            OpenVxApi.pyapi.discard(r)
        context_obj.clear_references()
        OpenVxApi.pyapi.discard(context[0])
        context[0] = OpenVxApi.pyapi.ffi.NULL

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'build' and len(sys.argv) == 3:
        api = PythonApi(OpenVxApi, build=sys.argv[2])
    else:
        print 'Usage: %s build <lib>' % sys.argv[0]
