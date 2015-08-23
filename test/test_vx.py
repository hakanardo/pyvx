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

