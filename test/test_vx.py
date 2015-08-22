from pyvx.default import vx

class TestVX(object):
    def test_context(self):
        c = vx.CreateContext()
        assert vx.ReleaseContext(c) == vx.SUCCESS

