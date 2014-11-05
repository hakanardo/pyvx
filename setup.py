from distutils.core import setup, Command
from distutils.command.build import build as BuildCommand
from distutils.command.install import install as InstallCommand
from distutils.dir_util import copy_tree, remove_tree, mkpath
import sys
import os
import pyvx.nodes
import pyvx.capi
from pyvx import __version__

mydir = os.path.dirname(os.path.abspath(__file__))
libdir = os.path.join('build', 'lib')
libs = []

class MyBuild(BuildCommand):
    def run(self):
        BuildCommand.run(self)
        if os.path.exists(libdir):
            remove_tree(libdir)
        mkpath(libdir)
        libs.extend(pyvx.capi.build(libdir))

class MyInstall(InstallCommand):
    def run(self):
        InstallCommand.run(self)
        for l in libs:
            l = os.path.basename(l)
            l = os.path.join('/usr/local/lib/', l)
            if os.path.exists(l) or os.path.islink(l):
                print 'Removing', l
                os.unlink(l)
        copy_tree(libdir, '/usr/local/lib/', preserve_symlinks=True)
        os.system('ldconfig')

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
        long_description='''
PyVX is an implementation of `OpenVX`_ in python. `OpenVX`_ is a standard for
expressing computer vision processing algorithms as a graph of function nodes.
This graph is verified once and can then be processed (executed) multiple
times. This implementation gains its performance by generating C-code during the
verification phase. This code is compiled and loaded dynamically and then
called during the process phase.

To use this python implementation as an `OpenVX`_ backend from a C program, a
shared library is provided. This library embeds python and provides an C API
following the `OpenVX`_ specification. That way the C program does not need to
be aware of the fact that python is used. Also, any C program following the
`OpenVX`_ specification will be compilable with this backend.

Further details are provided in the `Documentation`_

.. _`OpenVX`: https://www.khronos.org/openvx
.. _`Documentation`: https://pyvx.readthedocs.org        
        ''',
        version=__version__,
        packages=['pyvx', 'pyvx.inc'],
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
                                                 'headers/VX/vx_vendors.h'])],
        cmdclass={'build': MyBuild, 'test': PyTest, 'install': MyInstall},
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
