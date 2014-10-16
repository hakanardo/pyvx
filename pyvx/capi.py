from codegen import PythonApi, Enum, Reference
import codegen
from pyvx import *

def export(signature, add_ret_to_arg=0, **kwargs):
    return codegen.export(signature, add_ret_to_arg, **kwargs)



class OpenVxApi(object):
    cdef = ''

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
    vx_status = Enum(*status_codes, prefix="VX_")

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

    @export("vx_status(vx_graph)")
    def vxVerifyGraph(graph):
        try:
            graph.verify()
        except VerificationError as e:
            return e.__class__
        return SUCCESS

    @export("vx_status(vx_graph)")
    def vxProcessGraph(graph):
        return graph.process()
    
    @export("void(vx_context *)", retrive_args=False)
    def vxReleaseContext(context):
        context_obj = OpenVxApi.pyapi.retrive(context[0])
        for r in context_obj.references:
            OpenVxApi.pyapi.discard(r)
        context_obj.clear_references()
        OpenVxApi.pyapi.discard(context[0])
        context[0] = OpenVxApi.pyapi.ffi.NULL

    @export("vx_node(vx_graph, vx_image, vx_channel, vx_image)")
    def vxChannelExtractNode(graph, input, channel, output):
        return ChannelExtractNode(graph, input, channel, output)

    @export("vx_node(vx_graph, vx_image, vx_image)")
    def vxGaussian3x3Node(graph, input, output):
        return Gaussian3x3Node(graph, input, output)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxSobel3x3Node(graph, input, output_x, output_y):
        return Sobel3x3Node(graph, input, output_x, output_y)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxMagnitudeNode(graph, grad_x, grad_y, mag):
        return MagnitudeNode(graph, grad_x, grad_y, mag)

    @export("vx_node(vx_graph, vx_image, vx_image, vx_image)")
    def vxPhaseNode(graph, grad_x, grad_y, orientation):
        return PhaseNode(graph, grad_x, grad_y, orientation)

    @export("vx_node(vx_graph, char *, vx_image)")
    def vxPlayNode(graph, fn, output):
        return PlayNode(graph, fn, output)

    @export("vx_node(vx_graph, vx_image, char *)")
    def vxShowNode(graph, input, name):
        return ShowNode(graph, input, name)


def build(out_path='.'):
    from pyvx import __version_info__, __version__
    major, minor, _ = __version_info__
    soversion = '%d.%d' % (major, minor)
    api = PythonApi(OpenVxApi, build=('openvx', __version__, soversion, out_path))
    return api.library_names

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'build' and len(sys.argv) == 2:
        build()
    else:
        print 'Usage: %s build' % sys.argv[0]
