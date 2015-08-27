from distutils.core import setup, Command
from pyvx import __version__
import sys

class PyTestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        errno = pytest.main()
        sys.exit(errno)


setup(
    name='PyVX',
    description='OpenVX python support',
    long_description='''
PyVX is a set of python bindings for `OpenVX`_. `OpenVX`_ is a standard for
expressing computer vision processing algorithms as a graph of function nodes.
This graph is verified once and can then be processed (executed) multiple
times. PyVX allows these graphs to be constructed and interacted with from
python. It also supports the use of multiple `OpenVX`_ backends, both C and
python backends. It also used to contain a code generating `OpenVX`_ backend
written it python, but it will be moved to a package of it's own (curently
it lives on the try1 branch of pyvx).

Further details are provided in the `Documentation`_

.. _`OpenVX`: https://www.khronos.org/openvx
.. _`Documentation`: https://pyvx.readthedocs.org
        ''',
    version=__version__,
    packages=['pyvx'],
    zip_safe=False,
    url='http://pyvx.readthedocs.org',
    author='Hakan Ardo',
    author_email='pyvx@googlegroups.com',
    license='MIT',
    install_requires=['cffi'],
    cmdclass={'test': PyTestCommand},
    tests_require=['pytest'],
)
