
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
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
 */

#ifndef _OPENVX_TYPES_H_
#define _OPENVX_TYPES_H_

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#if defined(WIN32) || defined(UNDER_CE)
#include <windows.h>
#endif

typedef char     vx_char;

typedef uint8_t  vx_uint8;

typedef uint16_t vx_uint16;

typedef uint32_t vx_uint32;

typedef uint64_t vx_uint64;

typedef int8_t   vx_int8;

typedef int16_t  vx_int16;

typedef int32_t  vx_int32;

typedef int64_t  vx_int64;

#if defined(OVX_PLATFORM_SUPPORTS_16_FLOAT)

typedef hfloat   vx_float16;
#endif

typedef float    vx_float32;

typedef double   vx_float64;

typedef struct _vx_reference *vx_reference;

typedef int32_t vx_enum;

typedef size_t vx_size;

typedef uint32_t vx_df_image;

typedef struct _vx_scalar *vx_scalar;

typedef struct _vx_image *vx_image;

typedef struct _vx_kernel *vx_kernel;

typedef struct _vx_parameter *vx_parameter;

typedef struct _vx_node *vx_node;

typedef struct _vx_graph *vx_graph;

typedef struct _vx_context *vx_context;

typedef struct _vx_delay *vx_delay;

typedef struct _vx_lut *vx_lut;

typedef struct _vx_distribution *vx_distribution;

typedef struct _vx_matrix *vx_matrix;

typedef struct _vx_pyramid *vx_pyramid;

typedef struct _vx_threshold *vx_threshold;

typedef struct _vx_convolution *vx_convolution;

typedef struct _vx_remap *vx_remap;

typedef struct _vx_array *vx_array;

typedef enum _vx_bool_e {
    vx_false_e = 0,
    vx_true_e,
} vx_bool;

typedef struct _vx_meta_format* vx_meta_format;

enum vx_type_e {
    VX_TYPE_INVALID         = 0x000,
    VX_TYPE_CHAR            = 0x001,
    VX_TYPE_INT8            = 0x002,
    VX_TYPE_UINT8           = 0x003,
    VX_TYPE_INT16           = 0x004,
    VX_TYPE_UINT16          = 0x005,
    VX_TYPE_INT32           = 0x006,
    VX_TYPE_UINT32          = 0x007,
    VX_TYPE_INT64           = 0x008,
    VX_TYPE_UINT64          = 0x009,
    VX_TYPE_FLOAT32         = 0x00A,
    VX_TYPE_FLOAT64         = 0x00B,
    VX_TYPE_ENUM            = 0x00C,
    VX_TYPE_SIZE            = 0x00D,
    VX_TYPE_DF_IMAGE        = 0x00E,
#if defined(OVX_PLATFORM_SUPPORTS_16_FLOAT)
    VX_TYPE_FLOAT16         = 0x00F,
#endif
    VX_TYPE_BOOL            = 0x010,
    /* add new scalar types here */

    VX_TYPE_SCALAR_MAX,     
    VX_TYPE_RECTANGLE       = 0x020,
    VX_TYPE_KEYPOINT        = 0x021,
    VX_TYPE_COORDINATES2D   = 0x022,
    VX_TYPE_COORDINATES3D   = 0x023,
    VX_TYPE_STRUCT_MAX,     
    VX_TYPE_USER_STRUCT_START = 0x100, 
    VX_TYPE_REFERENCE       = 0x800,
    VX_TYPE_CONTEXT         = 0x801,
    VX_TYPE_GRAPH           = 0x802,
    VX_TYPE_NODE            = 0x803,
    VX_TYPE_KERNEL          = 0x804,
    VX_TYPE_PARAMETER       = 0x805,
    VX_TYPE_DELAY           = 0x806,
    VX_TYPE_LUT             = 0x807,
    VX_TYPE_DISTRIBUTION    = 0x808,
    VX_TYPE_PYRAMID         = 0x809,
    VX_TYPE_THRESHOLD       = 0x80A,
    VX_TYPE_MATRIX          = 0x80B,
    VX_TYPE_CONVOLUTION     = 0x80C,
    VX_TYPE_SCALAR          = 0x80D,
    VX_TYPE_ARRAY           = 0x80E,
    VX_TYPE_IMAGE           = 0x80F,
    VX_TYPE_REMAP           = 0x810,
    VX_TYPE_ERROR           = 0x811,
    VX_TYPE_META_FORMAT     = 0x812,
    /* \todo add new object types here */

    VX_TYPE_OBJECT_MAX,     
};

enum vx_status_e {
    VX_STATUS_MIN                       = -25,
    /* add new codes here */
    VX_ERROR_REFERENCE_NONZERO          = -24,
    VX_ERROR_MULTIPLE_WRITERS           = -23,
    VX_ERROR_GRAPH_ABANDONED            = -22,
    VX_ERROR_GRAPH_SCHEDULED            = -21,
    VX_ERROR_INVALID_SCOPE              = -20,
    VX_ERROR_INVALID_NODE               = -19,
    VX_ERROR_INVALID_GRAPH              = -18,
    VX_ERROR_INVALID_TYPE               = -17,
    VX_ERROR_INVALID_VALUE              = -16,
    VX_ERROR_INVALID_DIMENSION          = -15,
    VX_ERROR_INVALID_FORMAT             = -14,
    VX_ERROR_INVALID_LINK               = -13,
    VX_ERROR_INVALID_REFERENCE          = -12,
    VX_ERROR_INVALID_MODULE             = -11,
    VX_ERROR_INVALID_PARAMETERS         = -10,
    VX_ERROR_OPTIMIZED_AWAY             = -9,
    VX_ERROR_NO_MEMORY                  = -8,
    VX_ERROR_NO_RESOURCES               = -7,
    VX_ERROR_NOT_COMPATIBLE             = -6,
    VX_ERROR_NOT_ALLOCATED              = -5,
    VX_ERROR_NOT_SUFFICIENT             = -4,
    VX_ERROR_NOT_SUPPORTED              = -3,
    VX_ERROR_NOT_IMPLEMENTED            = -2,
    VX_FAILURE                          = -1,
    VX_SUCCESS                          =  0,
};

typedef vx_enum vx_status;

typedef vx_enum vx_action;

typedef vx_action (*vx_nodecomplete_f)(vx_node node);

#define VX_VENDOR_MASK                      (0xFFF00000)

#define VX_TYPE_MASK                        (0x000FFF00)

#define VX_LIBRARY_MASK                     (0x000FF000)

#define VX_KERNEL_MASK                      (0x00000FFF)

#define VX_ATTRIBUTE_ID_MASK                (0x000000FF)

#define VX_ENUM_TYPE_MASK                   (0x000FF000)

#define VX_ENUM_MASK                        (0x00000FFF)

#define VX_VENDOR(e)                        (((vx_uint32)e & VX_VENDOR_MASK) >> 20)

#define VX_TYPE(e)                          (((vx_uint32)e & VX_TYPE_MASK) >> 8)

#define VX_ENUM_TYPE(e)                     (((vx_uint32)e & VX_ENUM_TYPE_MASK) >> 12)

#define VX_LIBRARY(e)                       (((vx_uint32)e & VX_LIBRARY_MASK) >> 12)

#if defined(_LITTLE_ENDIAN_) || (__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__) || defined(_WIN32) || defined(WIN32)
#define VX_DF_IMAGE(a,b,c,d)                  ((a) | (b << 8) | (c << 16) | (d << 24))
#define VX_ATTRIBUTE_BASE(vendor, object)   (((vendor) << 20) | (object << 8))
#define VX_KERNEL_BASE(vendor, lib)         (((vendor) << 20) | (lib << 12))
#define VX_ENUM_BASE(vendor, id)            (((vendor) << 20) | (id << 12))
#elif defined(_BIG_ENDIAN_) || (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#define VX_DF_IMAGE(a,b,c,d)                  ((d) | (c << 8) | (b << 16) | (a << 24))
#define VX_ATTRIBUTE_BASE(vendor, object)   ((vendor) | (object << 12))
#define VX_KERNEL_BASE(vendor, lib)         ((vendor) | (lib << 12))
#define VX_ENUM_BASE(vendor, id)            ((vendor) | (id << 12))
#else
#error "Endian-ness must be defined!"
#endif

enum vx_enum_e {
    VX_ENUM_DIRECTION       = 0x00, 
    VX_ENUM_ACTION          = 0x01, 
    VX_ENUM_HINT            = 0x02, 
    VX_ENUM_DIRECTIVE       = 0x03, 
    VX_ENUM_INTERPOLATION   = 0x04, 
    VX_ENUM_OVERFLOW        = 0x05, 
    VX_ENUM_COLOR_SPACE     = 0x06, 
    VX_ENUM_COLOR_RANGE     = 0x07, 
    VX_ENUM_PARAMETER_STATE = 0x08, 
    VX_ENUM_CHANNEL         = 0x09, 
    VX_ENUM_CONVERT_POLICY  = 0x0A, 
    VX_ENUM_THRESHOLD_TYPE  = 0x0B, 
    VX_ENUM_BORDER_MODE     = 0x0C, 
    VX_ENUM_COMPARISON      = 0x0D, 
    VX_ENUM_IMPORT_MEM      = 0x0E, 
    VX_ENUM_TERM_CRITERIA   = 0x0F, 
    VX_ENUM_NORM_TYPE       = 0x10, 
    VX_ENUM_ACCESSOR        = 0x11, 
    VX_ENUM_ROUND_POLICY    = 0x12, 
};

enum vx_action_e {
    VX_ACTION_CONTINUE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACTION) + 0x0,
    VX_ACTION_RESTART  = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACTION) + 0x1,
    VX_ACTION_ABANDON  = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACTION) + 0x2,
};

enum vx_direction_e {
    VX_INPUT = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_DIRECTION) + 0x0,
    VX_OUTPUT = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_DIRECTION) + 0x1,
    VX_BIDIRECTIONAL = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_DIRECTION) + 0x2,
};

enum vx_hint_e {
    VX_HINT_SERIALIZE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_HINT) + 0x0,
};

enum vx_directive_e {
    VX_DIRECTIVE_DISABLE_LOGGING = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_DIRECTIVE) + 0x0,
    VX_DIRECTIVE_ENABLE_LOGGING = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_DIRECTIVE) + 0x1,
};

enum vx_convert_policy_e {
    VX_CONVERT_POLICY_WRAP = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CONVERT_POLICY) + 0x0,
    VX_CONVERT_POLICY_SATURATE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CONVERT_POLICY) + 0x1,
};

enum vx_df_image_e {
    VX_DF_IMAGE_VIRT = VX_DF_IMAGE('V','I','R','T'),
    VX_DF_IMAGE_RGB  = VX_DF_IMAGE('R','G','B','2'),
    VX_DF_IMAGE_RGBX = VX_DF_IMAGE('R','G','B','A'),
    VX_DF_IMAGE_NV12 = VX_DF_IMAGE('N','V','1','2'),
    VX_DF_IMAGE_NV21 = VX_DF_IMAGE('N','V','2','1'),
    VX_DF_IMAGE_UYVY = VX_DF_IMAGE('U','Y','V','Y'),
    VX_DF_IMAGE_YUYV = VX_DF_IMAGE('Y','U','Y','V'),
    VX_DF_IMAGE_IYUV = VX_DF_IMAGE('I','Y','U','V'),
    VX_DF_IMAGE_YUV4 = VX_DF_IMAGE('Y','U','V','4'),
    VX_DF_IMAGE_U8 = VX_DF_IMAGE('U','0','0','8'),
    VX_DF_IMAGE_U16  = VX_DF_IMAGE('U','0','1','6'),
    VX_DF_IMAGE_S16  = VX_DF_IMAGE('S','0','1','6'),
    VX_DF_IMAGE_U32  = VX_DF_IMAGE('U','0','3','2'),
    VX_DF_IMAGE_S32  = VX_DF_IMAGE('S','0','3','2'),
};

enum vx_reference_attribute_e {
    VX_REF_ATTRIBUTE_COUNT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REFERENCE) + 0x0,
    VX_REF_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REFERENCE) + 0x1,
};

enum vx_context_attribute_e {
    VX_CONTEXT_ATTRIBUTE_VENDOR_ID = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x0,
    VX_CONTEXT_ATTRIBUTE_VERSION = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x1,
    VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x2,
    VX_CONTEXT_ATTRIBUTE_MODULES = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x3,
    VX_CONTEXT_ATTRIBUTE_REFERENCES = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x4,
    VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x5,
    VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x6,
    VX_CONTEXT_ATTRIBUTE_EXTENSIONS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x7,
    VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x8,
    VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0x9,
    VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0xA,
    VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONTEXT) + 0xB,
};

enum vx_kernel_attribute_e {
    VX_KERNEL_ATTRIBUTE_PARAMETERS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_KERNEL) + 0x0,
    VX_KERNEL_ATTRIBUTE_NAME = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_KERNEL) + 0x1,
    VX_KERNEL_ATTRIBUTE_ENUM = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_KERNEL) + 0x2,
    VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_KERNEL) + 0x3,
    VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_KERNEL) + 0x4,
};

enum vx_node_attribute_e {
    VX_NODE_ATTRIBUTE_STATUS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_NODE) + 0x0,
    VX_NODE_ATTRIBUTE_PERFORMANCE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_NODE) + 0x1,
    VX_NODE_ATTRIBUTE_BORDER_MODE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_NODE) + 0x2,
    VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_NODE) + 0x3,
    VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_NODE) + 0x4,
};

enum vx_parameter_attribute_e {
    VX_PARAMETER_ATTRIBUTE_INDEX = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PARAMETER) + 0x0,
    VX_PARAMETER_ATTRIBUTE_DIRECTION = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PARAMETER) + 0x1,
    VX_PARAMETER_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PARAMETER) + 0x2,
    VX_PARAMETER_ATTRIBUTE_STATE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PARAMETER) + 0x3,
    VX_PARAMETER_ATTRIBUTE_REF = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PARAMETER) + 0x4,
};

enum vx_image_attribute_e {
    VX_IMAGE_ATTRIBUTE_WIDTH = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x0,
    VX_IMAGE_ATTRIBUTE_HEIGHT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x1,
    VX_IMAGE_ATTRIBUTE_FORMAT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x2,
    VX_IMAGE_ATTRIBUTE_PLANES = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x3,
    VX_IMAGE_ATTRIBUTE_SPACE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x4,
    VX_IMAGE_ATTRIBUTE_RANGE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x5,
    VX_IMAGE_ATTRIBUTE_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_IMAGE) + 0x6,
};

enum vx_scalar_attribute_e {
    VX_SCALAR_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_SCALAR) + 0x0,
};

enum vx_graph_attribute_e {
    VX_GRAPH_ATTRIBUTE_NUMNODES = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_GRAPH) + 0x0,
    VX_GRAPH_ATTRIBUTE_STATUS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_GRAPH) + 0x1,
    VX_GRAPH_ATTRIBUTE_PERFORMANCE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_GRAPH) + 0x2,
    VX_GRAPH_ATTRIBUTE_NUMPARAMETERS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_GRAPH) + 0x3,
};

enum vx_lut_attribute_e {
    VX_LUT_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS,VX_TYPE_LUT) + 0x0,
    VX_LUT_ATTRIBUTE_COUNT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS,VX_TYPE_LUT) + 0x1,
    VX_LUT_ATTRIBUTE_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS,VX_TYPE_LUT) + 0x2,
};

enum vx_distribution_attribute_e {
    VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x0,
    VX_DISTRIBUTION_ATTRIBUTE_OFFSET = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x1,
    VX_DISTRIBUTION_ATTRIBUTE_RANGE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x2,
    VX_DISTRIBUTION_ATTRIBUTE_BINS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x3,
    VX_DISTRIBUTION_ATTRIBUTE_WINDOW = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x4,
    VX_DISTRIBUTION_ATTRIBUTE_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DISTRIBUTION) + 0x5,
};

enum vx_threshold_type_e {
    VX_THRESHOLD_TYPE_BINARY = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_THRESHOLD_TYPE) + 0x0,
    VX_THRESHOLD_TYPE_RANGE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_THRESHOLD_TYPE) + 0x1,
};

enum vx_threshold_attribute_e {
    VX_THRESHOLD_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x0,
    VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x1,
    VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x2,
    VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x3,
    VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x4,
    VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_THRESHOLD) + 0x5,
};

enum vx_matrix_attribute_e {
    VX_MATRIX_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_MATRIX) + 0x0,
    VX_MATRIX_ATTRIBUTE_ROWS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_MATRIX) + 0x1,
    VX_MATRIX_ATTRIBUTE_COLUMNS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_MATRIX) + 0x2,
    VX_MATRIX_ATTRIBUTE_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_MATRIX) + 0x3,
};

enum vx_convolution_attribute_e {
    VX_CONVOLUTION_ATTRIBUTE_ROWS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONVOLUTION) + 0x0,
    VX_CONVOLUTION_ATTRIBUTE_COLUMNS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONVOLUTION) + 0x1,
    VX_CONVOLUTION_ATTRIBUTE_SCALE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONVOLUTION) + 0x2,
    VX_CONVOLUTION_ATTRIBUTE_SIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_CONVOLUTION) + 0x3,
};

enum vx_pyramid_attribute_e {
    VX_PYRAMID_ATTRIBUTE_LEVELS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PYRAMID) + 0x0,
    VX_PYRAMID_ATTRIBUTE_SCALE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PYRAMID) + 0x1,
    VX_PYRAMID_ATTRIBUTE_WIDTH = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PYRAMID) + 0x2,
    VX_PYRAMID_ATTRIBUTE_HEIGHT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PYRAMID) + 0x3,
    VX_PYRAMID_ATTRIBUTE_FORMAT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_PYRAMID) + 0x4,
};

enum vx_remap_attribute_e {
    VX_REMAP_ATTRIBUTE_SOURCE_WIDTH = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REMAP) + 0x0,
    VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REMAP) + 0x1,
    VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REMAP) + 0x2,
    VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_REMAP) + 0x3,
};

enum vx_array_attribute_e {
    VX_ARRAY_ATTRIBUTE_ITEMTYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_ARRAY) + 0x0,
    VX_ARRAY_ATTRIBUTE_NUMITEMS = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_ARRAY) + 0x1,
    VX_ARRAY_ATTRIBUTE_CAPACITY = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_ARRAY) + 0x2,
    VX_ARRAY_ATTRIBUTE_ITEMSIZE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_ARRAY) + 0x3,
};

enum vx_meta_format_attribute_e {
    VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_META_FORMAT) + 0x0,
};

enum vx_channel_e {
    VX_CHANNEL_0 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CHANNEL) + 0x0,
    VX_CHANNEL_1 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CHANNEL) + 0x1,
    VX_CHANNEL_2 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CHANNEL) + 0x2,
    VX_CHANNEL_3 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_CHANNEL) + 0x3,

    VX_CHANNEL_R = VX_CHANNEL_0,
    VX_CHANNEL_G = VX_CHANNEL_1,
    VX_CHANNEL_B = VX_CHANNEL_2,
    VX_CHANNEL_A = VX_CHANNEL_3,
    VX_CHANNEL_Y = VX_CHANNEL_0,
    VX_CHANNEL_U = VX_CHANNEL_1,
    VX_CHANNEL_V = VX_CHANNEL_2,
};

enum vx_import_type_e {
    VX_IMPORT_TYPE_NONE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_IMPORT_MEM) + 0x0,

    VX_IMPORT_TYPE_HOST = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_IMPORT_MEM) + 0x1,
};

enum vx_interpolation_type_e {
    VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_INTERPOLATION) + 0x0,
    VX_INTERPOLATION_TYPE_BILINEAR = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_INTERPOLATION) + 0x1,
    VX_INTERPOLATION_TYPE_AREA = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_INTERPOLATION) + 0x2,
};

enum vx_color_space_e {
    VX_COLOR_SPACE_NONE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_SPACE) + 0x0,
    VX_COLOR_SPACE_BT601_525 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_SPACE) + 0x1,
    VX_COLOR_SPACE_BT601_625 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_SPACE) + 0x2,
    VX_COLOR_SPACE_BT709 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_SPACE) + 0x3,

    VX_COLOR_SPACE_DEFAULT = VX_COLOR_SPACE_BT709,
};

enum vx_channel_range_e {
    VX_CHANNEL_RANGE_FULL = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_RANGE) + 0x0,
    VX_CHANNEL_RANGE_RESTRICTED = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_COLOR_RANGE) + 0x1,
};

enum vx_parameter_state_e {
    VX_PARAMETER_STATE_REQUIRED = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_PARAMETER_STATE) + 0x0,
    VX_PARAMETER_STATE_OPTIONAL = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_PARAMETER_STATE) + 0x1,
};

enum vx_border_mode_e {
    VX_BORDER_MODE_UNDEFINED = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_BORDER_MODE) + 0x0,
    VX_BORDER_MODE_CONSTANT = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_BORDER_MODE) + 0x1,
    VX_BORDER_MODE_REPLICATE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_BORDER_MODE) + 0x2,
};

enum vx_termination_criteria_e {
    VX_TERM_CRITERIA_ITERATIONS = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_TERM_CRITERIA) + 0x0,
    VX_TERM_CRITERIA_EPSILON = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_TERM_CRITERIA) + 0x1,
    VX_TERM_CRITERIA_BOTH = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_TERM_CRITERIA) + 0x2,
};

enum vx_norm_type_e {
    VX_NORM_L1 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_NORM_TYPE) + 0x0,
    VX_NORM_L2 = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_NORM_TYPE) + 0x1,
};

enum vx_delay_attribute_e {
    VX_DELAY_ATTRIBUTE_TYPE = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DELAY) + 0x0,
    VX_DELAY_ATTRIBUTE_COUNT = VX_ATTRIBUTE_BASE(VX_ID_KHRONOS, VX_TYPE_DELAY) + 0x1,
};

enum vx_accessor_e {
    VX_READ_ONLY = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACCESSOR) + 0x1,
    VX_WRITE_ONLY = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACCESSOR) + 0x2,
    VX_READ_AND_WRITE = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ACCESSOR) + 0x3,
};

enum vx_round_policy_e {
    VX_ROUND_POLICY_TO_ZERO = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ROUND_POLICY) + 0x1,
    VX_ROUND_POLICY_TO_NEAREST_EVEN = VX_ENUM_BASE(VX_ID_KHRONOS, VX_ENUM_ROUND_POLICY) + 0x2,
};

typedef vx_status (*vx_publish_kernels_f)(vx_context context);

typedef vx_status (*vx_kernel_f)(vx_node node, vx_reference *parameters, vx_uint32 num);

typedef vx_status (*vx_kernel_initialize_f)(vx_node node, vx_reference *parameters, vx_uint32 num);

typedef vx_status (*vx_kernel_deinitialize_f)(vx_node node, vx_reference *parameters, vx_uint32 num);

typedef vx_status (*vx_kernel_input_validate_f)(vx_node node, vx_uint32 index);

typedef vx_status (*vx_kernel_output_validate_f)(vx_node node, vx_uint32 index, vx_meta_format meta);

#if defined(WIN32) || defined(UNDER_CE)

#if defined(ARCH_32)
#define VX_FMT_REF  "%lu"

#define VX_FMT_SIZE "%lu"
#elif defined(ARCH_64)

#define VX_FMT_REF  "%I64u"

#define VX_FMT_SIZE "%I64u"
#endif
#else

#define VX_FMT_REF  "%p"

#define VX_FMT_SIZE "%zu"
#endif

#define VX_SCALE_UNITY (1024u)

typedef struct _vx_imagepatch_addressing_t {
    vx_uint32 dim_x;        
    vx_uint32 dim_y;        
    vx_int32  stride_x;     
    vx_int32  stride_y;     
    vx_uint32 scale_x;      
    vx_uint32 scale_y;      
    vx_uint32 step_x;       
    vx_uint32 step_y;       
} vx_imagepatch_addressing_t;

#define VX_IMAGEPATCH_ADDR_INIT {0u, 0u, 0, 0, 0u, 0u, 0u, 0u}

typedef struct _vx_perf_t {
    vx_uint64 tmp;          
    vx_uint64 beg;          
    vx_uint64 end;          
    vx_uint64 sum;          
    vx_uint64 avg;          
    vx_uint64 min;          
    vx_uint64 num;          
} vx_perf_t;

#define VX_PERF_INIT    {0ul, 0ul, 0ul, 0ul, 0ul, 0ul}

typedef struct _vx_kernel_info_t {
    vx_enum enumeration;

    vx_char name[VX_MAX_KERNEL_NAME];
} vx_kernel_info_t;

#define VX_SCALE_PYRAMID_HALF       (0.5f)

#define VX_SCALE_PYRAMID_ORB        ((vx_float32)0.8408964f)

typedef struct _vx_border_mode_t {
    vx_enum mode;
    vx_uint32 constant_value;
} vx_border_mode_t;

typedef struct _vx_keypoint_t {
    vx_int32 x;                 
    vx_int32 y;                 
    vx_float32 strength;        
    vx_float32 scale;           
    vx_float32 orientation;     
    vx_int32 tracking_status;   
    vx_float32 error;           
} vx_keypoint_t;

typedef struct _vx_rectangle_t {
    vx_uint32 start_x;          
    vx_uint32 start_y;          
    vx_uint32 end_x;            
    vx_uint32 end_y;            
} vx_rectangle_t;

typedef struct _vx_delta_rectangle_t {
    vx_int32 delta_start_x; 
    vx_int32 delta_start_y; 
    vx_int32 delta_end_x;   
    vx_int32 delta_end_y;   
} vx_delta_rectangle_t;

typedef struct _vx_coordinates2d_t {
    vx_uint32 x;    
    vx_uint32 y;    
} vx_coordinates2d_t;

typedef struct _vx_coordinates3d_t {
    vx_uint32 x;    
    vx_uint32 y;    
    vx_uint32 z;    
} vx_coordinates3d_t;

typedef void (*vx_log_callback_f)(vx_context context,
                                  vx_reference ref,
                                  vx_status status,
                                  vx_char string[]);

#endif
