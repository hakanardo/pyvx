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
