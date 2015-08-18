cdef = '''

/*==============================================================================
 CONTEXT
 =============================================================================*/

 vx_context vxCreateContext(void);

 vx_status vxReleaseContext(vx_context *context);

 vx_context vxGetContext(vx_reference reference);

 vx_status vxQueryContext(vx_context context, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxSetContextAttribute(vx_context context, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxHint(vx_context context, vx_reference reference, vx_enum hint);

 vx_status vxDirective(vx_context context, vx_reference reference, vx_enum directive);

 vx_status vxGetStatus(vx_reference reference);

 vx_enum vxRegisterUserStruct(vx_context context, vx_size size);

/*==============================================================================
 IMAGE
 =============================================================================*/

 vx_image vxCreateImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color);

 vx_image vxCreateImageFromROI(vx_image img, vx_rectangle_t *rect);

 vx_image vxCreateUniformImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color, void *value);

 vx_image vxCreateVirtualImage(vx_graph graph, vx_uint32 width, vx_uint32 height, vx_df_image color);

 vx_image vxCreateImageFromHandle(vx_context context, vx_df_image color, vx_imagepatch_addressing_t addrs[], void *ptrs[], vx_enum import_type);

 vx_status vxQueryImage(vx_image image, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxSetImageAttribute(vx_image image, vx_enum attribute, void *out, vx_size size);

 vx_status vxReleaseImage(vx_image *image);

 vx_size vxComputeImagePatchSize(vx_image image,
                                       vx_rectangle_t *rect,
                                       vx_uint32 plane_index);

 vx_status vxAccessImagePatch(vx_image image,
                                    vx_rectangle_t *rect,
                                    vx_uint32 plane_index,
                                    vx_imagepatch_addressing_t *addr,
                                    void **ptr,
                                    vx_enum usage);

 vx_status vxCommitImagePatch(vx_image image,
                                    vx_rectangle_t *rect,
                                    vx_uint32 plane_index,
                                    vx_imagepatch_addressing_t *addr,
                                    void *ptr);

 void *vxFormatImagePatchAddress1d(void *ptr, vx_uint32 index, vx_imagepatch_addressing_t *addr);

 void *vxFormatImagePatchAddress2d(void *ptr, vx_uint32 x, vx_uint32 y, vx_imagepatch_addressing_t *addr);

 vx_status vxGetValidRegionImage(vx_image image, vx_rectangle_t *rect);

/*==============================================================================
 KERNEL
 =============================================================================*/

 vx_status vxLoadKernels(vx_context context, vx_char *module);

 vx_kernel vxGetKernelByName(vx_context context, vx_char *name);

 vx_kernel vxGetKernelByEnum(vx_context context, vx_enum kernel);

 vx_status vxQueryKernel(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxReleaseKernel(vx_kernel *kernel);

 vx_kernel vxAddKernel(vx_context context,
                             vx_char name[256],
                             vx_enum enumeration,
                             vx_kernel_f func_ptr,
                             vx_uint32 numParams,
                             vx_kernel_input_validate_f input,
                             vx_kernel_output_validate_f output,
                             vx_kernel_initialize_f init,
                             vx_kernel_deinitialize_f deinit);

 vx_status vxFinalizeKernel(vx_kernel kernel);

 vx_status vxAddParameterToKernel(vx_kernel kernel, vx_uint32 index, vx_enum dir, vx_enum data_type, vx_enum state);

 vx_status vxRemoveKernel(vx_kernel kernel);

 vx_status vxSetKernelAttribute(vx_kernel kernel, vx_enum attribute, void *ptr, vx_size size);

 vx_parameter vxGetKernelParameterByIndex(vx_kernel kernel, vx_uint32 index);

/*==============================================================================
 GRAPH
 =============================================================================*/

 vx_graph vxCreateGraph(vx_context context);

 vx_status vxReleaseGraph(vx_graph *graph);

 vx_status vxVerifyGraph(vx_graph graph);

 vx_status vxProcessGraph(vx_graph graph);

 vx_status vxScheduleGraph(vx_graph graph);

 vx_status vxWaitGraph(vx_graph graph);

 vx_status vxQueryGraph(vx_graph graph, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxSetGraphAttribute(vx_graph graph, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAddParameterToGraph(vx_graph graph, vx_parameter parameter);

 vx_status vxSetGraphParameterByIndex(vx_graph graph, vx_uint32 index, vx_reference value);

 vx_parameter vxGetGraphParameterByIndex(vx_graph graph, vx_uint32 index);

 vx_bool vxIsGraphVerified(vx_graph graph);

/*==============================================================================
 NODE
 =============================================================================*/

 vx_node vxCreateGenericNode(vx_graph graph, vx_kernel kernel);

 vx_status vxQueryNode(vx_node node, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxSetNodeAttribute(vx_node node, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxReleaseNode(vx_node *node);

 void vxRemoveNode(vx_node *node);

 vx_status vxAssignNodeCallback(vx_node node, vx_nodecomplete_f callback);

 vx_nodecomplete_f vxRetrieveNodeCallback(vx_node node);

/*==============================================================================
 PARAMETER
 =============================================================================*/

 vx_parameter vxGetParameterByIndex(vx_node node, vx_uint32 index);

 vx_status vxReleaseParameter(vx_parameter *param);

 vx_status vxSetParameterByIndex(vx_node node, vx_uint32 index, vx_reference value);

 vx_status vxSetParameterByReference(vx_parameter parameter, vx_reference value);

 vx_status vxQueryParameter(vx_parameter param, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 SCALAR
 =============================================================================*/

 vx_scalar vxCreateScalar(vx_context context, vx_enum data_type, void *ptr);

 vx_status vxReleaseScalar(vx_scalar *scalar);

 vx_status vxQueryScalar(vx_scalar scalar, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAccessScalarValue(vx_scalar ref, void *ptr);

 vx_status vxCommitScalarValue(vx_scalar ref, void *ptr);

/*==============================================================================
 REFERENCE
 =============================================================================*/

 vx_status vxQueryReference(vx_reference ref, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 DELAY
 =============================================================================*/

 vx_status vxQueryDelay(vx_delay delay, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxReleaseDelay(vx_delay *delay);

 vx_delay vxCreateDelay(vx_context context,
                              vx_reference exemplar,
                              vx_size count);

 vx_reference vxGetReferenceFromDelay(vx_delay delay, vx_int32 index);

 vx_status vxAgeDelay(vx_delay delay);


/*==============================================================================
 LOGGING
 =============================================================================*/

 void vxAddLogEntry(vx_reference ref, vx_status status, const char *message, ...);

 void vxRegisterLogCallback(vx_context context, vx_log_callback_f callback, vx_bool reentrant);

/*==============================================================================
 LUT
 =============================================================================*/

 vx_lut vxCreateLUT(vx_context context, vx_enum data_type, vx_size count);

 vx_status vxReleaseLUT(vx_lut *lut);

 vx_status vxQueryLUT(vx_lut lut, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAccessLUT(vx_lut lut, void **ptr, vx_enum usage);

 vx_status vxCommitLUT(vx_lut lut, void *ptr);

/*==============================================================================
 DISTRIBUTION
 =============================================================================*/

 vx_distribution vxCreateDistribution(vx_context context, vx_size numBins, vx_size offset, vx_size range);

 vx_status vxReleaseDistribution(vx_distribution *distribution);

 vx_status vxQueryDistribution(vx_distribution distribution, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAccessDistribution(vx_distribution distribution, void **ptr, vx_enum usage);

 vx_status vxCommitDistribution(vx_distribution distribution, void * ptr);

/*==============================================================================
 THRESHOLD
 =============================================================================*/

 vx_threshold vxCreateThreshold(vx_context c, vx_enum thresh_type, vx_enum data_type);

 vx_status vxReleaseThreshold(vx_threshold *thresh);

 vx_status vxSetThresholdAttribute(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxQueryThreshold(vx_threshold thresh, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 MATRIX
 =============================================================================*/

 vx_matrix vxCreateMatrix(vx_context c, vx_enum data_type, vx_size columns, vx_size rows);

 vx_status vxReleaseMatrix(vx_matrix *mat);

 vx_status vxQueryMatrix(vx_matrix mat, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAccessMatrix(vx_matrix mat, void *array);

 vx_status vxCommitMatrix(vx_matrix mat, void *array);

/*==============================================================================
 CONVOLUTION
 =============================================================================*/

 vx_convolution vxCreateConvolution(vx_context context, vx_size columns, vx_size rows);

 vx_status vxReleaseConvolution(vx_convolution *conv);

 vx_status vxQueryConvolution(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxSetConvolutionAttribute(vx_convolution conv, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAccessConvolutionCoefficients(vx_convolution conv, vx_int16 *array);

 vx_status vxCommitConvolutionCoefficients(vx_convolution conv, vx_int16 *array);

/*==============================================================================
 PYRAMID
 =============================================================================*/

 vx_pyramid vxCreatePyramid(vx_context context, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format);

 vx_pyramid vxCreateVirtualPyramid(vx_graph graph, vx_size levels, vx_float32 scale, vx_uint32 width, vx_uint32 height, vx_df_image format);


 vx_status vxReleasePyramid(vx_pyramid *pyr);

 vx_status vxQueryPyramid(vx_pyramid pyr, vx_enum attribute, void *ptr, vx_size size);

 vx_image vxGetPyramidLevel(vx_pyramid pyr, vx_uint32 index);

/*==============================================================================
 REMAP
 =============================================================================*/

 vx_remap vxCreateRemap(vx_context context,
                              vx_uint32 src_width,
                              vx_uint32 src_height,
                              vx_uint32 dst_width,
                              vx_uint32 dst_height);

 vx_status vxReleaseRemap(vx_remap *table);

 vx_status vxSetRemapPoint(vx_remap table,
                                 vx_uint32 dst_x, vx_uint32 dst_y,
                                 vx_float32 src_x, vx_float32 src_y);

 vx_status vxGetRemapPoint(vx_remap table,
                                 vx_uint32 dst_x, vx_uint32 dst_y,
                                 vx_float32 *src_x, vx_float32 *src_y);

 vx_status vxQueryRemap(vx_remap r, vx_enum attribute, void *ptr, vx_size size);

/*==============================================================================
 ARRAY
 =============================================================================*/

 vx_array vxCreateArray(vx_context context, vx_enum item_type, vx_size capacity);

 vx_array vxCreateVirtualArray(vx_graph graph, vx_enum item_type, vx_size capacity);

 vx_status vxReleaseArray(vx_array *arr);

 vx_status vxQueryArray(vx_array arr, vx_enum attribute, void *ptr, vx_size size);

 vx_status vxAddArrayItems(vx_array arr, vx_size count, void *ptr, vx_size stride);

 vx_status vxTruncateArray(vx_array arr, vx_size new_num_items);

 vx_status vxAccessArrayRange(vx_array arr, vx_size start, vx_size end, vx_size *stride, void **ptr, vx_enum usage);

 vx_status vxCommitArrayRange(vx_array arr, vx_size start, vx_size end, void *ptr);

/* TODO
#define vxFormatArrayPointer(ptr, index, stride) \
    (&(((vx_uint8*)(ptr))[(index) * (stride)]))

#define vxArrayItem(type, ptr, index, stride) \
    (*(type *)(vxFormatArrayPointer((ptr), (index), (stride))))
*/

/*==============================================================================
 META FORMAT
 =============================================================================*/

 vx_status vxSetMetaFormatAttribute(vx_meta_format meta, vx_enum attribute, void *ptr, vx_size size);

'''