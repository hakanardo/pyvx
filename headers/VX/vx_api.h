
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

#ifndef _OPENVX_API_H_
#define _OPENVX_API_H_

#if defined(_WIN32) || defined(_WIN64) || defined(__CYGWIN__)
#if defined(VX_BUILDING)
#if defined(__GNUC__)
#define VX_API __attribute__((dllexport))
#else
#define VX_API __declspec(dllexport)
#endif
#else
#if defined(__GNUC__)
#define VX_API __attribute__((dllimport))
#else
#define VX_API __declspec(dllimport)
#endif
#endif
#else
#if (__GNUC__ >= 4)
#define VX_API __attribute__((visibility("default")))
#else
#define VX_API
#endif
#endif

#ifdef  __cplusplus
extern "C" {
#endif

/*==============================================================================
 CONTEXT
 =============================================================================*/

VX_API vx_context vxCreateContext(void);

VX_API vx_status vxReleaseContext(vx_context *context);

VX_API vx_context vxGetContext(vx_reference reference);

VX_API vx_status vxQueryContext(vx_context context, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxSetContextAttribute(vx_context context, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxHint(vx_context context, vx_reference reference, vx_enum hint);

VX_API vx_status vxDirective(vx_context context, vx_reference reference, vx_enum directive);

VX_API vx_status vxGetStatus(vx_reference reference);

VX_API vx_enum vxRegisterUserStruct(vx_context context, vx_size size);

/*==============================================================================
 IMAGE
 =============================================================================*/

VX_API vx_image vxCreateImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color);

VX_API vx_image vxCreateImageFromROI(vx_image img, vx_rectangle_t *rect);

VX_API vx_image vxCreateUniformImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color, void *value);

VX_API vx_image vxCreateVirtualImage(vx_graph graph, vx_uint32 width, vx_uint32 height, vx_df_image color);

VX_API vx_image vxCreateImageFromHandle(vx_context context, vx_df_image color, vx_imagepatch_addressing_t addrs[], void *ptrs[], vx_enum import_type);

VX_API vx_status vxQueryImage(vx_image image, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxSetImageAttribute(vx_image image, vx_enum attribute, void *out, vx_size size);

VX_API vx_status vxReleaseImage(vx_image *image);

VX_API vx_size vxComputeImagePatchSize(vx_image image,
                                       vx_rectangle_t *rect,
                                       vx_uint32 plane_index);

VX_API vx_status vxAccessImagePatch(vx_image image,
                                    vx_rectangle_t *rect,
                                    vx_uint32 plane_index,
                                    vx_imagepatch_addressing_t *addr,
                                    void **ptr,
                                    vx_enum usage);

VX_API vx_status vxCommitImagePatch(vx_image image,
                                    vx_rectangle_t *rect,
                                    vx_uint32 plane_index,
                                    vx_imagepatch_addressing_t *addr,
                                    void *ptr);

VX_API void *vxFormatImagePatchAddress1d(void *ptr, vx_uint32 index, vx_imagepatch_addressing_t *addr);

VX_API void *vxFormatImagePatchAddress2d(void *ptr, vx_uint32 x, vx_uint32 y, vx_imagepatch_addressing_t *addr);

VX_API vx_status vxGetValidRegionImage(vx_image image, vx_rectangle_t *rect);

/*==============================================================================
 KERNEL
 =============================================================================*/

VX_API vx_status vxLoadKernels(vx_context context, vx_char *module);

VX_API vx_kernel vxGetKernelByName(vx_context context, vx_char *name);

VX_API vx_kernel vxGetKernelByEnum(vx_context context, vx_enum kernel);

VX_API vx_status vxQueryKernel(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxReleaseKernel(vx_kernel *kernel);

VX_API vx_kernel vxAddKernel(vx_context context,
                             vx_char name[VX_MAX_KERNEL_NAME],
                             vx_enum enumeration,
                             vx_kernel_f func_ptr,
                             vx_uint32 numParams,
                             vx_kernel_input_validate_f input,
                             vx_kernel_output_validate_f output,
                             vx_kernel_initialize_f init,
                             vx_kernel_deinitialize_f deinit);

VX_API vx_status vxFinalizeKernel(vx_kernel kernel);

VX_API vx_status vxAddParameterToKernel(vx_kernel kernel, vx_uint32 index, vx_enum dir, vx_enum data_type, vx_enum state);

VX_API vx_status vxRemoveKernel(vx_kernel kernel);

VX_API vx_status vxSetKernelAttribute(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_parameter vxGetKernelParameterByIndex(vx_kernel kernel, vx_uint32 index);

/*==============================================================================
 GRAPH
 =============================================================================*/

VX_API vx_graph vxCreateGraph(vx_context context);

VX_API vx_status vxReleaseGraph(vx_graph *graph);

VX_API vx_status vxVerifyGraph(vx_graph graph);

VX_API vx_status vxProcessGraph(vx_graph graph);

VX_API vx_status vxScheduleGraph(vx_graph graph);

VX_API vx_status vxWaitGraph(vx_graph graph);

VX_API vx_status vxQueryGraph(vx_graph graph, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxSetGraphAttribute(vx_graph graph, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAddParameterToGraph(vx_graph graph, vx_parameter parameter);

VX_API vx_status vxSetGraphParameterByIndex(vx_graph graph, vx_uint32 index, vx_reference value);

VX_API vx_parameter vxGetGraphParameterByIndex(vx_graph graph, vx_uint32 index);

VX_API vx_bool vxIsGraphVerified(vx_graph graph);

/*==============================================================================
 NODE
 =============================================================================*/

VX_API vx_node vxCreateGenericNode(vx_graph graph, vx_kernel kernel);

VX_API vx_status vxQueryNode(vx_node node, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxSetNodeAttribute(vx_node node, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxReleaseNode(vx_node *node);

VX_API void vxRemoveNode(vx_node *node);

VX_API vx_status vxAssignNodeCallback(vx_node node, vx_nodecomplete_f callback);

VX_API vx_nodecomplete_f vxRetrieveNodeCallback(vx_node node);

/*==============================================================================
 PARAMETER
 =============================================================================*/

VX_API vx_parameter vxGetParameterByIndex(vx_node node, vx_uint32 index);

VX_API vx_status vxReleaseParameter(vx_parameter *param);

VX_API vx_status vxSetParameterByIndex(vx_node node, vx_uint32 index, vx_reference value);

VX_API vx_status vxSetParameterByReference(vx_parameter parameter, vx_reference value);

VX_API vx_status vxQueryParameter(vx_parameter param, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 SCALAR
 =============================================================================*/

VX_API vx_scalar vxCreateScalar(vx_context context, vx_enum data_type, void *ptr);

VX_API vx_status vxReleaseScalar(vx_scalar *scalar);

VX_API vx_status vxQueryScalar(vx_scalar scalar, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAccessScalarValue(vx_scalar ref, void *ptr);

VX_API vx_status vxCommitScalarValue(vx_scalar ref, void *ptr);

/*==============================================================================
 REFERENCE
 =============================================================================*/

VX_API vx_status vxQueryReference(vx_reference ref, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 DELAY
 =============================================================================*/

VX_API vx_status vxQueryDelay(vx_delay delay, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxReleaseDelay(vx_delay *delay);

VX_API vx_delay vxCreateDelay(vx_context context,
                              vx_reference exemplar,
                              vx_size count);

VX_API vx_reference vxGetReferenceFromDelay(vx_delay delay, vx_int32 index);

VX_API vx_status vxAgeDelay(vx_delay delay);


/*==============================================================================
 LOGGING
 =============================================================================*/

VX_API void vxAddLogEntry(vx_reference ref, vx_status status, const char *message, ...);

VX_API void vxRegisterLogCallback(vx_context context, vx_log_callback_f callback, vx_bool reentrant);

/*==============================================================================
 LUT
 =============================================================================*/

VX_API vx_lut vxCreateLUT(vx_context context, vx_enum data_type, vx_size count);

VX_API vx_status vxReleaseLUT(vx_lut *lut);

VX_API vx_status vxQueryLUT(vx_lut lut, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAccessLUT(vx_lut lut, void **ptr, vx_enum usage);

VX_API vx_status vxCommitLUT(vx_lut lut, void *ptr);

/*==============================================================================
 DISTRIBUTION
 =============================================================================*/

VX_API vx_distribution vxCreateDistribution(vx_context context, vx_size numBins, vx_size offset, vx_size range);

VX_API vx_status vxReleaseDistribution(vx_distribution *distribution);

VX_API vx_status vxQueryDistribution(vx_distribution distribution, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAccessDistribution(vx_distribution distribution, void **ptr, vx_enum usage);

VX_API vx_status vxCommitDistribution(vx_distribution distribution, void * ptr);

/*==============================================================================
 THRESHOLD
 =============================================================================*/

VX_API vx_threshold vxCreateThreshold(vx_context c, vx_enum thresh_type, vx_enum data_type);

VX_API vx_status vxReleaseThreshold(vx_threshold *thresh);

VX_API vx_status vxSetThresholdAttribute(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxQueryThreshold(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 MATRIX
 =============================================================================*/

VX_API vx_matrix vxCreateMatrix(vx_context c, vx_enum data_type, vx_size columns, vx_size rows);

VX_API vx_status vxReleaseMatrix(vx_matrix *mat);

VX_API vx_status vxQueryMatrix(vx_matrix mat, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAccessMatrix(vx_matrix mat, void *array);

VX_API vx_status vxCommitMatrix(vx_matrix mat, void *array);

/*==============================================================================
 CONVOLUTION
 =============================================================================*/

VX_API vx_convolution vxCreateConvolution(vx_context context, vx_size columns, vx_size rows);

VX_API vx_status vxReleaseConvolution(vx_convolution *conv);

VX_API vx_status vxQueryConvolution(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxSetConvolutionAttribute(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAccessConvolutionCoefficients(vx_convolution conv, vx_int16 *array);

VX_API vx_status vxCommitConvolutionCoefficients(vx_convolution conv, vx_int16 *array);

/*==============================================================================
 PYRAMID
 =============================================================================*/

VX_API vx_pyramid vxCreatePyramid(vx_context context, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format);

VX_API vx_pyramid vxCreateVirtualPyramid(vx_graph graph, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format);


VX_API vx_status vxReleasePyramid(vx_pyramid *pyr);

VX_API vx_status vxQueryPyramid(vx_pyramid pyr, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_image vxGetPyramidLevel(vx_pyramid pyr, vx_uint32 index);

/*==============================================================================
 REMAP
 =============================================================================*/

VX_API vx_remap vxCreateRemap(vx_context context,
                              vx_uint32 src_width,
                              vx_uint32 src_height,
                              vx_uint32 dst_width,
                              vx_uint32 dst_height);

VX_API vx_status vxReleaseRemap(vx_remap *table);

VX_API vx_status vxSetRemapPoint(vx_remap table,
                                 vx_uint32 dst_x, vx_uint32 dst_y,
                                 vx_float32 src_x, vx_float32 src_y);

VX_API vx_status vxGetRemapPoint(vx_remap table,
                                 vx_uint32 dst_x, vx_uint32 dst_y,
                                 vx_float32 *src_x, vx_float32 *src_y);

VX_API vx_status vxQueryRemap(vx_remap r, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 ARRAY
 =============================================================================*/

VX_API vx_array vxCreateArray(vx_context context, vx_enum item_type, vx_size capacity);

VX_API vx_array vxCreateVirtualArray(vx_graph graph, vx_enum item_type, vx_size capacity);

VX_API vx_status vxReleaseArray(vx_array *arr);

VX_API vx_status vxQueryArray(vx_array arr, vx_enum attribute, void *ptr, vx_size size);

VX_API vx_status vxAddArrayItems(vx_array arr, vx_size count, void *ptr, vx_size stride);

VX_API vx_status vxTruncateArray(vx_array arr, vx_size new_num_items);

VX_API vx_status vxAccessArrayRange(vx_array arr, vx_size start, vx_size end, vx_size *stride, void **ptr, vx_enum usage);

VX_API vx_status vxCommitArrayRange(vx_array arr, vx_size start, vx_size end, void *ptr);

#define vxFormatArrayPointer(ptr, index, stride) \
    (&(((vx_uint8*)(ptr))[(index) * (stride)]))

#define vxArrayItem(type, ptr, index, stride) \
    (*(type *)(vxFormatArrayPointer((ptr), (index), (stride))))

/*==============================================================================
 META FORMAT
 =============================================================================*/

VX_API vx_status vxSetMetaFormatAttribute(vx_meta_format meta, vx_enum attribute, void *ptr, vx_size size);

#ifdef  __cplusplus
}
#endif

#endif

