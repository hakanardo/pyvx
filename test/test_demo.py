class TestDemo(object):
    def test_simple(self):
        import demo.simple

    def test_simple_pythonic(self):
        import demo.simple_pythonic

    def test_gradient(self):
        from demo.gradient import main
        main('test/test.avi')

    def test_view(self):
        from demo.view import main
        main('test/test.avi')
