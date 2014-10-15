from distutils.core import setup
from distutils.command.build import build
import os
import pyvx.nodes
import pyvx.capi
from pyvx.version import version

mydir = os.path.dirname(os.path.abspath(__file__))
libs = []

class my_build(build):
    def run(self):
        if not os.path.exists('build'):
            os.mkdir('build')
        libs.extend(pyvx.capi.build('build'))
        build.run(self)



setup(
        name='PyVX',
        description='OpenVX implementation',
        long_description=open(os.path.join(mydir, 'README.rst')).read(),
        version=version,
        packages=['pyvx'],
        package_data={'pyvx': ['glview.h', 'vlcplay.h']},
        zip_safe=False,
        url='http://pyvx.readthedocs.org',
        author='Hakan Ardo',
        author_email='pyvx@googlegroups.com',
        license='MIT',
        install_requires=['pycparser','cffi'],
        ext_modules=[pyvx.nodes.ffi.verifier.get_extension()],
        data_files = [('/usr/local/include', [os.path.join('build', 'openvx.h')]),
                      ('/usr/local/lib', libs)],
        cmdclass={'build': my_build},
    )