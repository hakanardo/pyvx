
/*
 * Copyright (c) 2012-2014 The Khronos Group Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and/or associated documentation files (the
 * "Materials"), to deal in the Materials without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Materials, and to
 * permit persons to whom the Materials are furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Materials.
 *
 * THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY,\todo FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
 */

#ifndef _OPENVX_VENDORS_H_
#define _OPENVX_VENDORS_H_

enum vx_vendor_id_e {
    VX_ID_KHRONOS   = 0x000, 
    VX_ID_TI        = 0x001, 
    VX_ID_QUALCOMM  = 0x002, 
    VX_ID_NVIDIA    = 0x003, 
    VX_ID_ARM       = 0x004, 
    VX_ID_BDTI      = 0x005, 
    VX_ID_RENESAS   = 0x006, 
    VX_ID_VIVANTE   = 0x007, 
    VX_ID_XILINX    = 0x008, 
    VX_ID_AXIS      = 0x009, 
    VX_ID_MOVIDIUS  = 0x00A, 
    VX_ID_SAMSUNG   = 0x00B, 
    VX_ID_FREESCALE = 0x00C, 
    VX_ID_AMD       = 0x00D, 
    VX_ID_BROADCOM  = 0x00E, 
    VX_ID_INTEL     = 0x00F, 
    VX_ID_MARVELL   = 0x010, 
    VX_ID_MEDIATEK  = 0x011, 
    VX_ID_ST        = 0x012, 
    VX_ID_CEVA      = 0x013, 
    VX_ID_ITSEEZ    = 0x014, 
    VX_ID_IMAGINATION=0x015, 
    VX_ID_COGNIVUE  = 0x016, 
    VX_ID_VIDEANTIS = 0x017, 
    /* Add new vendor code above this line */

    VX_ID_MAX       = 0xFFF,
    VX_ID_DEFAULT = VX_ID_MAX,
};

#endif

