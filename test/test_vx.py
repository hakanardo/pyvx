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

        addr = vx.imagepatch_addressing_t(640, 480, 1, 640, 1, 1, 1, 640)
        data = array('B', [0]) * (640 * 480)
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

        s = vx.ComputeImagePatchSize(img, vx.rectangle_t(10, 20, 30, 40), 0)

        assert vx.ReleaseContext(c) == vx.SUCCESS
