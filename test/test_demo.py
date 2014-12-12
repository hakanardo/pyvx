import os, pytest

class TestDemo(object):
    def test_simple(self):
        import demo.simple

    def test_simple_pythonic(self):
        import demo.simple_pythonic

    @pytest.mark.skipif(not os.getenv('DISPLAY'), reason="No DISPLAY")
    def test_gradient(self):
        from demo.gradient import main
        main('test/test.avi')

    @pytest.mark.skipif(not os.getenv('DISPLAY'), reason="No DISPLAY")
    def test_view(self):
        from demo.view import main
        main('test/test.avi')
