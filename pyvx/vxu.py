"""
:mod:`pyvx.vxu` --- C-like Python API
==========================================

All the *vxuXxx* functions of the `OpenVX`_ standard are availible as
*vxu.Xxx*. For example,

.. code-block:: python

        c = vx.CreateContext()
        img = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_U8)
        dx = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        dy = vx.CreateImage(c, 640, 480, vx.DF_IMAGE_S16)
        assert vxu.Sobel3x3(c, img, dx, dy) == vx.SUCCESS
        vx.ReleaseContext(c)

"""
from pyvx._auto_vxu import *
