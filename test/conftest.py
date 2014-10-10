import sys, os
sys.path = [os.path.dirname(os.path.dirname(__file__))] + sys.path

def pytest_addoption(parser):
    group = parser.getgroup("pyvx")
    group._addoption('--src',
                     action="store_true", dest="show_src", default=False,
                     help="print the produced C-code")

def pytest_configure(config):
    if config.getvalue("show_src"):
        import pyvx.backend
        config.option.capture = 'no'
        pyvx.backend.CoreGraph.show_source = True
