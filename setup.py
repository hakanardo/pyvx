from setuptools import setup, Extension
import os
import pyvx.nodes

mydir = os.path.dirname(os.path.abspath(__file__))

setup(
        name='pyvx',
        description='OpenVx implementation',
        long_description=open(os.path.join(mydir, 'README.rst')).read(),
        version='0.1.0',
        packages=['pyvx'],
        package_data={'pyvx': ['glview.h', 'vlcplay.h']},
        zip_safe=False,
        url='FIXME',
        author='Hakan Ardo',
        author_email='hakan@debian.org',
        license='MIT',
        install_requires=['cffi'],
        ext_modules=[pyvx.nodes.ffi.verifier.get_extension()],
    )