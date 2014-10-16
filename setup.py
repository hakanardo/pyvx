from distutils.core import setup
from distutils.command.build import build
import os
import pyvx.nodes
import pyvx.capi
from pyvx import __version__

mydir = os.path.dirname(os.path.abspath(__file__))
libs = []

class my_build(build):
    def run(self):
        if not os.path.exists('build'):
            os.mkdir('build')
        libs.extend(pyvx.capi.build('build'))
        build.run(self)



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
        data_files = [('/usr/local/include', [os.path.join('build', 'openvx.h')]),
                      ('/usr/local/lib', libs)],
        cmdclass={'build': my_build},
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
