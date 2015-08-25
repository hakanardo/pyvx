from array import array
from pyvx.default import vx

class TestVX(object):
    def test_context(self):
        c = vx.CreateContext()
        assert vx.GetStatus(c) == vx.SUCCESS
        s, v = vx.QueryContext(c, vx.CONTEXT_ATTRIBUTE_VENDOR_ID, 'vx_uint16')
        assert s == vx.SUCCESS
        assert isinstance(v, int)
        s, v = vx.QueryContext(c, vx.CONTEXT_ATTRIBUTE_IMPLEMENTATION, 'vx_char[VX_MAX_IMPLEMENTATION_NAME]', str)
        assert s == vx.SUCCESS
        assert isinstance(v, str)

        s = vx.SetContextAttribute(c, vx.CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE,
                                      vx.border_mode_t(vx.BORDER_MODE_CONSTANT, 42))
        assert s == vx.SUCCESS
        s, v = vx.QueryContext(c, vx.CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE, 'vx_border_mode_t')
        assert s == vx.SUCCESS
        assert v.mode == vx.BORDER_MODE_CONSTANT
        assert v.constant_value == 42

        vx.Hint(c, vx.HINT_SERIALIZE)
        vx.Directive(c, vx.DIRECTIVE_DISABLE_LOGGING)
        assert vx.GetContext(c) == c
        vx.RegisterUserStruct(c, 42)

        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_image(self):
        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_RGB)
        assert vx.GetStatus(c) == vx.SUCCESS

        roi = vx.CreateImageFromROI(img, vx.rectangle_t(10, 10, 100, 100))
        assert vx.GetStatus(c) == vx.SUCCESS
        assert vx.ReleaseImage(roi) == vx.SUCCESS
        roi = None

        const = vx.CreateUniformImage(c, 640, 480, vx.DF_IMAGE_S16, 7, 'vx_int16')
        assert vx.GetStatus(c) == vx.SUCCESS

        const = vx.CreateUniformImage(c, 640, 480, vx.DF_IMAGE_RGB, (7, 8, 9), 'vx_uint8[]')
        assert vx.GetStatus(c) == vx.SUCCESS

        addr = vx.imagepatch_addressing_t(640, 480, 1, 640, vx.SCALE_UNITY, vx.SCALE_UNITY, 1, 1)
        data = array('B', [42]) * (640 * 480)
        hand = vx.CreateImageFromHandle(c, vx.DF_IMAGE_U8, (addr,), (data,), vx.IMPORT_TYPE_HOST)
        assert vx.GetStatus(c) == vx.SUCCESS
        hand = vx.CreateImageFromHandle(c, vx.DF_IMAGE_U8, addr, data, vx.IMPORT_TYPE_HOST)
        assert vx.GetStatus(c) == vx.SUCCESS
        hand = vx.CreateImageFromHandle(c, vx.DF_IMAGE_RGB, (addr, addr, addr), (data, data, data), vx.IMPORT_TYPE_HOST)
        assert vx.GetStatus(c) == vx.SUCCESS

        assert vx.QueryImage(img, vx.IMAGE_ATTRIBUTE_WIDTH, 'vx_uint32') == (vx.SUCCESS, 640)
        assert vx.SetImageAttribute(img, vx.IMAGE_ATTRIBUTE_SPACE, vx.COLOR_SPACE_BT601_525, 'vx_enum') == vx.SUCCESS
        assert vx.QueryImage(img, vx.IMAGE_ATTRIBUTE_SPACE, 'vx_enum') == (vx.SUCCESS, vx.COLOR_SPACE_BT601_525)

        assert vx.GetContext(img) == c

        r = vx.rectangle_t(10, 20, 30, 40)
        s = vx.ComputeImagePatchSize(img, r, 0)
        status, addr, ptr = vx.AccessImagePatch(img, r, 0, None, None, vx.READ_AND_WRITE)
        assert status == vx.SUCCESS
        assert addr.dim_x == addr.dim_y == 20
        ptr[0] = 'H'
        assert vx.CommitImagePatch(img, r, 0, addr, ptr) == vx.SUCCESS
        status, addr, ptr = vx.AccessImagePatch(img, r, 0, None, None, vx.READ_AND_WRITE)
        assert status == vx.SUCCESS
        assert ptr[0] == 'H'
        pixel = vx.FormatImagePatchAddress1d(ptr, 0, addr)
        assert pixel[0] == 'H'
        assert vx.CommitImagePatch(img, r, 0, addr, ptr) == vx.SUCCESS

        assert 7 not in data
        addr = vx.imagepatch_addressing_t(20, 20, 1, 20, vx.SCALE_UNITY, vx.SCALE_UNITY, 1, 1)
        rdata = array('B', [0]) * (20 * 20)
        status, addr, ptr = vx.AccessImagePatch(hand, r, 0, addr, rdata, vx.READ_AND_WRITE)
        assert rdata[1] == 42
        rdata[1] = 7
        pixel = vx.FormatImagePatchAddress1d(ptr, 1, addr)
        assert pixel[0] == chr(7)
        pixel = vx.FormatImagePatchAddress2d(ptr, 0, 0, addr)
        assert pixel[0] == chr(42)
        assert vx.CommitImagePatch(hand, r, 0, addr, ptr) == vx.SUCCESS
        assert data[11 + 20*640] == 7

        status, r = vx.GetValidRegionImage(const)
        assert status == vx.SUCCESS
        assert r.end_x == 640
        assert r.end_y == 480

        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_kernel(self):
        c = vx.CreateContext()
        assert vx.LoadKernels(c, "openvx-extras") == vx.SUCCESS
        kernel = vx.GetKernelByName(c, "org.khronos.openvx.sobel_3x3")
        assert vx.GetStatus(c) == vx.SUCCESS
        k = vx.GetKernelByEnum(c, vx.KERNEL_SOBEL_3x3)
        assert kernel == k
        s, i = vx.QueryKernel(kernel, vx.KERNEL_ATTRIBUTE_ENUM, 'vx_enum')
        assert i == vx.KERNEL_SOBEL_3x3
        vx.ReleaseKernel(k)
        param = vx.GetKernelParameterByIndex(kernel, 0)
        assert vx.GetStatus(c) == vx.SUCCESS

        # FIXME:  vxAddKernel, vxAddParameterToKernel, vxFinalizeKernel, vxRemoveKernel
        # FIXME: assert vx.SetKernelAttribute(kernel, vx.KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE, 7, 'vx_size') == vx.SUCCESS

        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_graph(self):
        c = vx.CreateContext()
        g = vx.CreateGraph(c)
        assert vx.IsGraphVerified(g) == vx.false_e
        assert vx.QueryGraph(g, vx.GRAPH_ATTRIBUTE_NUMNODES, 'vx_uint32') == (vx.SUCCESS, 0)

        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        node = vx.Sobel3x3Node(g, img, dx, dy)
        assert vx.VerifyGraph(g) == vx.SUCCESS
        assert vx.ProcessGraph(g) == vx.SUCCESS
        assert vx.ScheduleGraph(g) == vx.SUCCESS
        assert vx.WaitGraph(g) == vx.SUCCESS

        p = vx.GetParameterByIndex(node, 0)
        assert vx.AddParameterToGraph(g, p) == vx.SUCCESS
        p2 = vx.GetGraphParameterByIndex(g, 0)
        assert vx.SetGraphParameterByIndex(g, 0, dx) == vx.SUCCESS
        assert vx.VerifyGraph(g) != vx.SUCCESS
        assert vx.SetGraphParameterByIndex(g, 0, img) == vx.SUCCESS
        assert vx.VerifyGraph(g) == vx.SUCCESS
        assert vx.IsGraphVerified(g) == vx.true_e

        class flags:
            callback_called = False
        def callback(node):
            flags.callback_called = True
            return vx.SUCCESS

        assert vx.AssignNodeCallback(node, callback) == vx.SUCCESS
        assert vx.ProcessGraph(g) == vx.SUCCESS
        assert flags.callback_called

        assert vx.AssignNodeCallback(node, callback) != vx.SUCCESS
        assert vx.AssignNodeCallback(node, None) == vx.SUCCESS
        assert vx.AssignNodeCallback(node, callback) == vx.SUCCESS

        img = vx.CreateVirtualImage(g, 640, 480, vx.DF_IMAGE_RGB)
        assert vx.GetStatus(c) == vx.SUCCESS

        assert vx.ReleaseGraph(g) == vx.SUCCESS
        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_node(self):
        c = vx.CreateContext()
        g = vx.CreateGraph(c)

        k = vx.GetKernelByEnum(c, vx.KERNEL_SOBEL_3x3)
        assert vx.GetStatus(c) == vx.SUCCESS
        node = vx.CreateGenericNode(g, k)
        s = vx.SetNodeAttribute(node, vx.NODE_ATTRIBUTE_BORDER_MODE,
                                vx.border_mode_t(vx.BORDER_MODE_CONSTANT, 42))
        assert s == vx.SUCCESS
        s, v = vx.QueryNode(node, vx.NODE_ATTRIBUTE_BORDER_MODE, 'vx_border_mode_t')
        assert v.mode == vx.BORDER_MODE_CONSTANT
        assert v.constant_value == 42

        assert vx.ReleaseNode(node) == vx.SUCCESS

        node = vx.CreateGenericNode(g, k)
        assert vx.RemoveNode(node) == vx.SUCCESS

        assert vx.ReleaseGraph(g) == vx.SUCCESS
        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_parameter(self):
        c = vx.CreateContext()
        g = vx.CreateGraph(c)
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        node = vx.Sobel3x3Node(g, img, dx, dy)

        param = vx.GetParameterByIndex(node, 0)
        assert vx.GetStatus(c) == vx.SUCCESS
        s, v = vx.QueryParameter(param, vx.PARAMETER_ATTRIBUTE_REF, "vx_reference")
        assert s == vx.SUCCESS
        assert v == img

        assert vx.SetParameterByIndex(node, 0, dx) == vx.SUCCESS
        s, v = vx.QueryParameter(param, vx.PARAMETER_ATTRIBUTE_REF, "vx_reference")
        assert s == vx.SUCCESS
        assert v == dx

        assert vx.SetParameterByReference(param, dy) == vx.SUCCESS
        s, v = vx.QueryParameter(param, vx.PARAMETER_ATTRIBUTE_REF, "vx_reference")
        assert s == vx.SUCCESS
        assert v == dy

        assert vx.ReleaseParameter(param) == vx.SUCCESS
        assert vx.ReleaseContext(c) == vx.SUCCESS

    def test_scalar(self):
        c = vx.CreateContext()
        scalar = vx.CreateScalar(c, vx.TYPE_INT16, 7)
        assert vx.ReleaseContext(c) == vx.SUCCESS
