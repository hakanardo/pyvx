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
