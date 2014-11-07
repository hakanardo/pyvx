
/*******************************************************************************
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
******************************************************************************/

#ifndef _OPENVX_NODES_H_
#define _OPENVX_NODES_H_

#ifdef __cplusplus
extern "C" {
#endif

VX_API vx_node vxColorConvertNode(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxChannelExtractNode(vx_graph graph,
                             vx_image input,
                             vx_enum channel,
                             vx_image output);

VX_API vx_node vxChannelCombineNode(vx_graph graph,
                             vx_image plane0,
                             vx_image plane1,
                             vx_image plane2,
                             vx_image plane3,
                             vx_image output);

VX_API vx_node vxPhaseNode(vx_graph graph, vx_image grad_x, vx_image grad_y, vx_image orientation);

VX_API vx_node vxSobel3x3Node(vx_graph graph, vx_image input, vx_image output_x, vx_image output_y);


VX_API vx_node vxMagnitudeNode(vx_graph graph, vx_image grad_x, vx_image grad_y, vx_image mag);

VX_API vx_node vxScaleImageNode(vx_graph graph, vx_image src, vx_image dst, vx_enum type);

VX_API vx_node vxTableLookupNode(vx_graph graph, vx_image input, vx_lut lut, vx_image output);

VX_API vx_node vxHistogramNode(vx_graph graph, vx_image input, vx_distribution distribution);

VX_API vx_node vxEqualizeHistNode(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxAbsDiffNode(vx_graph graph, vx_image in1, vx_image in2, vx_image out);

VX_API vx_node vxMeanStdDevNode(vx_graph graph, vx_image input, vx_scalar mean, vx_scalar stddev);

VX_API vx_node vxThresholdNode(vx_graph graph, vx_image input, vx_threshold thresh, vx_image output);

VX_API vx_node vxIntegralImageNode(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxErode3x3Node(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxDilate3x3Node(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxMedian3x3Node(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxBox3x3Node(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxGaussian3x3Node(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxConvolveNode(vx_graph graph, vx_image input, vx_convolution conv, vx_image output);

VX_API vx_node vxGaussianPyramidNode(vx_graph graph, vx_image input, vx_pyramid gaussian);

VX_API vx_node vxAccumulateImageNode(vx_graph graph, vx_image input, vx_image accum);

VX_API vx_node vxAccumulateWeightedImageNode(vx_graph graph, vx_image input, vx_scalar alpha, vx_image accum);

VX_API vx_node vxAccumulateSquareImageNode(vx_graph graph, vx_image input, vx_scalar shift, vx_image accum);

VX_API vx_node vxMinMaxLocNode(vx_graph graph,
                        vx_image input,
                        vx_scalar minVal, vx_scalar maxVal,
                        vx_array minLoc, vx_array maxLoc,
                        vx_scalar minCount, vx_scalar maxCount);

VX_API vx_node vxAndNode(vx_graph graph, vx_image in1, vx_image in2, vx_image out);

VX_API vx_node vxOrNode(vx_graph graph, vx_image in1, vx_image in2, vx_image out);

VX_API vx_node vxXorNode(vx_graph graph, vx_image in1, vx_image in2, vx_image out);

VX_API vx_node vxNotNode(vx_graph graph, vx_image input, vx_image output);

VX_API vx_node vxMultiplyNode(vx_graph graph,
                       vx_image in1, vx_image in2,
                       vx_scalar scale,
                       vx_enum overflow_policy,
                       vx_enum rounding_policy,
                       vx_image out);

VX_API vx_node vxAddNode(vx_graph graph,
                  vx_image in1, vx_image in2,
                  vx_enum policy,
                  vx_image out);

VX_API vx_node vxSubtractNode(vx_graph graph,
                       vx_image in1, vx_image in2,
                       vx_enum policy,
                       vx_image out);

VX_API vx_node vxConvertDepthNode(vx_graph graph, vx_image input, vx_image output, vx_enum policy, vx_scalar shift);

VX_API vx_node vxCannyEdgeDetectorNode(vx_graph graph, vx_image input, vx_threshold hyst,
                                vx_int32 gradient_size, vx_enum norm_type,
                                vx_image output);

VX_API vx_node vxWarpAffineNode(vx_graph graph, vx_image input, vx_matrix matrix, vx_enum type, vx_image output);

VX_API vx_node vxWarpPerspectiveNode(vx_graph graph, vx_image input, vx_matrix matrix, vx_enum type, vx_image output);

VX_API vx_node vxHarrisCornersNode(vx_graph graph,
                            vx_image input,
                            vx_scalar strength_thresh,
                            vx_scalar min_distance,
                            vx_scalar sensitivity,
                            vx_int32 gradient_size,
                            vx_int32 block_size,
                            vx_array corners,
                            vx_scalar num_corners);

VX_API vx_node vxFastCornersNode(vx_graph graph, vx_image input, vx_scalar strength_thresh, vx_bool nonmax_suppression, vx_array corners, vx_scalar num_corners);

VX_API vx_node vxOpticalFlowPyrLKNode(vx_graph graph,
                               vx_pyramid old_images,
                               vx_pyramid new_images,
                               vx_array old_points,
                               vx_array new_points_estimates,
                               vx_array new_points,
                               vx_enum termination,
                               vx_scalar epsilon,
                               vx_scalar num_iterations,
                               vx_scalar use_initial_estimate,
                               vx_size window_dimension);

VX_API vx_node vxRemapNode(vx_graph graph,
                    vx_image input,
                    vx_remap table,
                    vx_enum policy,
                    vx_image output);

VX_API vx_node vxHalfScaleGaussianNode(vx_graph graph, vx_image input, vx_image output, vx_int32 kernel_size);

#ifdef __cplusplus
}
#endif

#endif
