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

The C-like Python API :ref:`pyvx.api` wraps the entire `OpenVX`_ standard version 1.0.1.

This is currently only a prof of
concept. Most of the OpenVX functionality is still missing. Some small examples are working. See the `demo`_ directory.
A handful of nodes are implemented as well as graph optimizations to do dead code elimination and to merge strictly
element-wise nodes. Contributions are welcome.

.. _`demo`: https://github.com/hakanardo/pyvx/tree/master/demo

Installation
============

Before installing, make sure all dependencies are installed (the package
will install anyway, but some functionality will be missing):

.. code-block:: bash

  apt-get install vlc libvlc-dev freeglut3-dev

Then there are a few different ways to install PyVX:

* Use pip:

.. code-block:: bash

    pip install pyvx

* or get the source code via the `Python Package Index`__.

.. __: http://pypi.python.org/pypi/pyvx

* or get it from `Github`_:

.. code-block:: bash

  git clone https://github.com/hakanardo/pyvx.git
  cd pyvx
  python setup.py install

This will install the backend and the python API. If you also want the C API
which allows you to compile `OpenVX`_ programs written in C and have them use 
PyVx as their backend you also need to:

.. code-block:: bash

  sudo python -mpyvx.capi build /usr/local/

This will install `libopenvx.so*` into `/usr/local/lib` and place the
`OpenVX`_ headers in `/usr/local/include/VX`.

.. _`Github`: https://github.com/hakanardo/pyvx

Modules
=======

The main modules of PyVX are:

:mod:`pyvx.vx`
    C-like Python API following the `OpenVX`_ API as strictly as possible.

:mod:`pyvx.pythonic`
    A more python friendly version of the `OpenVX`_ API.

:mod:`pyvx.capi`
    A specification of a C API that is used generate a shared
    library and a header file  that embeds python and calls the ``pyvx.vx``
    functions. This aims to provide the C API as it is specified by the `OpenVX`_ standard.

:mod:`pyvx.nodes`
    The implementation of the different processing nodes.

:mod:`pyvx.optimize`
    Graph optimizations that are executed on the graphs during the verification step.

:mod:`pyvx.codegen`
    Code generation tools.

.. automodule:: pyvx.vx
   :members:
.. automodule:: pyvx.pythonic
   :members:
.. automodule:: pyvx.capi
   :members:
.. automodule:: pyvx.nodes
   :members:
.. automodule:: pyvx.codegen
   :members:

Comments and bugs
=================

There is a `mailing list`_ for general discussions and an `issue tracker`_ for reporting bugs and a `continuous integration service`_ that's running tests.

.. _`issue tracker`: https://github.com/hakanardo/pyvx/issues
.. _`mailing list`: https://groups.google.com/forum/#!forum/pyvx
.. _`continuous integration service`: https://travis-ci.org/hakanardo/pyvx



