from distutils.core import setup
import os
import pyvx.nodes
import pyvx.capi
from pyvx.version import version

mydir = os.path.dirname(os.path.abspath(__file__))

libs = pyvx.capi.build()
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
        install_requires=['cffi'],
        ext_modules=[pyvx.nodes.ffi.verifier.get_extension()],
        data_files = [('/usr/local/include', ['openvx.h']),
                      ('/usr/local/lib', libs)],
    )