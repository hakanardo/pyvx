from codegen import PythonApi, Enum, Reference
import codegen
from pyvx import vx

def export(signature, add_ret_to_arg=0, **kwargs):
    return codegen.export(signature, add_ret_to_arg, **kwargs)



class OpenVxApi(object):
    wrapped_reference_types = ['vx_context', 'vx_image', 'vx_graph', 'vx_node']

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
    
    @export("vx_status(vx_context *)", retrive_args=False, add_ret_to_arg=None)
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
        return vx.PlayNode(graph, fn, output)

    @export("vx_node(vx_graph, vx_image, char *)")
    def vxShowNode(graph, input, name):
        return vx.ShowNode(graph, input, name)


def build(out_path='.'):
    from pyvx import __version_info__, __version__
    from pyvx.inc.vx import ffi
    major, minor, _ = __version_info__
    soversion = '%d.%d' % (major, minor)
    api = PythonApi(OpenVxApi, ffi)
    api.build('openvx', __version__, soversion, out_path)
    return api.library_names

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'build' and len(sys.argv) == 2:
        build()
    else:
        print 'Usage: %s build' % sys.argv[0]
