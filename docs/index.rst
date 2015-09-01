.. PyVX documentation master file, created by
   sphinx-quickstart on Wed Oct 15 08:26:42 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyVX
====

PyVX is a set of python bindings for `OpenVX`_. `OpenVX`_ is a standard for
expressing computer vision processing algorithms as a graph of function nodes.
This graph is verified once and can then be processed (executed) multiple
times. PyVX allows these graphs to be constructed and interacted with from
python. It also supports the use of multiple `OpenVX`_ backends, both C and
python backends. It also used to contain a code generating `OpenVX`_ backend
written it python, but it will be moved to a package of it's own (curently
it lives on the try1 branch of pyvx).

.. _`OpenVX`: https://www.khronos.org/openvx

Status
======

The C-like Python API :mod:`pyvx.api` wraps the entire `OpenVX`_ standard
version 1.0.1. The pythonic interface :mod:`pyvx.pythonic` is still work in
progress. Some small examples are working. See the `demo`_ directory.

.. _`demo`: https://github.com/hakanardo/pyvx/tree/master/demo

Installation
============

Then there are a few different ways to install PyVX:

* Use pip:

    .. code-block:: bash

        sudo pip install pyvx

* or get the source code via the `Python Package Index`__.

.. __: http://pypi.python.org/pypi/pyvx

* or get it from `Github`_:

    .. code-block:: bash

      git clone https://github.com/hakanardo/pyvx.git
      cd pyvx
      sudo python setup.py install

This will install the frontend and the python API. You will also need one or
several openvx backend implementations. For each backend you need to build
some backend specific wrappers:

.. code-block:: bash

  sudo python -mpyvx.build_cbackend [--default] name /path/to/openvx/install/

This will make the openvx backend installed in /path/to/openvx/install/
availible as :mod:`pyvx.backend.name` in python. One of the backends should
be marked as the default backend using the --default switch.

There is a `sample bakcend implementation`_ from Khronos. To use it as the
default backend on a 64 bit linux system:

.. code-block:: bash

    cd /usr/local/src
    wget https://www.khronos.org/registry/vx/sample/openvx_sample_1.0.1.tar.bz2
    tar xf openvx_sample_1.0.1.tar.bz2
    cd openvx_sample
    python Build.py --os Linux
    python -mpyvx.build_cbackend --default sample /usr/local/src/openvx_sample/install/Linux/x64/Release/


.. _`Github`: https://github.com/hakanardo/pyvx
.. _`sample bakcend implementation`:  https://www.khronos.org/registry/vx/

Modules
=======

The main modules of PyVX are:

:mod:`pyvx.default`
    Exportes an instance of :class:`pyvx.api.VX` with the default backend as
    *vx*.

:mod:`pyvx.api`
    C-like Python API following the `OpenVX`_ API as strictly as possible.

:mod:`pyvx.pythonic`
    A more python friendly version of the `OpenVX`_ API.

.. automodule:: pyvx.api
   :members:

Comments and bugs
=================

There is a `mailing list`_ for general discussions and an `issue tracker`_ for reporting bugs and a `continuous integration service`_ that's running tests.

.. _`issue tracker`: https://github.com/hakanardo/pyvx/issues
.. _`mailing list`: https://groups.google.com/forum/#!forum/pyvx
.. _`continuous integration service`: https://travis-ci.org/hakanardo/pyvx



