from distutils.core import setup, Command
from distutils.command.build import build as BuildCommand
import sys
import os
import pyvx.nodes
import pyvx.capi
from pyvx import __version__

mydir = os.path.dirname(os.path.abspath(__file__))
libs = []

class MyBuild(BuildCommand):
    def run(self):
        if not os.path.exists('build'):
            os.mkdir('build')
        libs.extend(pyvx.capi.build('build'))
        BuildCommand.run(self)


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        errno = pytest.main()
        sys.exit(errno)

ext_modules = [n.ffi.verifier.get_extension() 
               for n in [pyvx.nodes.PlayNode, pyvx.nodes.ShowNode]
               if n.lib]

setup(
        name='PyVX',
        description='OpenVX implementation',
        long_description=open(os.path.join(mydir, 'README.rst')).read(),
        version=__version__,
        packages=['pyvx'],
        package_data={'pyvx': ['glview.h', 'vlcplay.h', 'glview.c', 'vlcplay.c']},
        zip_safe=False,
        url='http://pyvx.readthedocs.org',
        author='Hakan Ardo',
        author_email='pyvx@googlegroups.com',
        license='MIT',
        install_requires=['pycparser','cffi'],
        ext_modules=ext_modules,
        data_files = [('/usr/local/include/VX', ['headers/VX/vx_api.h',
                                                 'headers/VX/vx.h',
                                                 'headers/VX/vx_kernels.h',
                                                 'headers/VX/vx_nodes.h',
                                                 'headers/VX/vx_types.h',
                                                 'headers/VX/vxu.h',
                                                 'headers/VX/vx_vendors.h']),
                      ('/usr/local/lib', libs)],
        cmdclass={'build': MyBuild, 'test': PyTest},
        tests_require=['pytest'],
    )

if pyvx.nodes.PlayNode.lib is None:
    print
    print "Warning: PlayNode not availible due to mssing dependencies. Try:"
    print
    print "    apt-get install vlc libvlc-dev"
    print

if pyvx.nodes.ShowNode.lib is None:
    print
    print "Warning: ShowNode not availible due to mssing dependencies. Try:"
    print
    print "    apt-get install freeglut3-dev"
    print
