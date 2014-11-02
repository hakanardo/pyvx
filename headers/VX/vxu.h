
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

#ifndef _OPENVX_UTILITY_H_
#define _OPENVX_UTILITY_H_

#ifdef __cplusplus
extern "C" {
#endif

VX_API vx_status vxuColorConvert(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuChannelExtract(vx_context context, vx_image input, vx_enum channel, vx_image output);

VX_API vx_status vxuChannelCombine(vx_context context, vx_image plane0, vx_image plane1, vx_image plane2, vx_image plane3, vx_image output);

VX_API vx_status vxuSobel3x3(vx_context context, vx_image input, vx_image output_x, vx_image output_y);

VX_API vx_status vxuMagnitude(vx_context context, vx_image grad_x, vx_image grad_y, vx_image output);

VX_API vx_status vxuPhase(vx_context context, vx_image grad_x, vx_image grad_y, vx_image output);

VX_API vx_status vxuScaleImage(vx_context context, vx_image src, vx_image dst, vx_enum type);

VX_API vx_status vxuTableLookup(vx_context context, vx_image input, vx_lut lut, vx_image output);

VX_API vx_status vxuHistogram(vx_context context, vx_image input, vx_distribution distribution);

VX_API vx_status vxuEqualizeHist(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuAbsDiff(vx_context context, vx_image in1, vx_image in2, vx_image out);

VX_API vx_status vxuMeanStdDev(vx_context context, vx_image input, vx_float32 *mean, vx_float32 *stddev);

VX_API vx_status vxuThreshold(vx_context context, vx_image input, vx_threshold thresh, vx_image output);

VX_API vx_status vxuIntegralImage(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuErode3x3(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuDilate3x3(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuMedian3x3(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuBox3x3(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuGaussian3x3(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuConvolve(vx_context context, vx_image input, vx_convolution matrix, vx_image output);

VX_API vx_status vxuGaussianPyramid(vx_context context, vx_image input, vx_pyramid gaussian);

VX_API vx_status vxuAccumulateImage(vx_context context, vx_image input, vx_image accum);

VX_API vx_status vxuAccumulateWeightedImage(vx_context context, vx_image input, vx_scalar scale, vx_image accum);

VX_API vx_status vxuAccumulateSquareImage(vx_context context, vx_image input, vx_scalar shift, vx_image accum);

VX_API vx_status vxuMinMaxLoc(vx_context context, vx_image input,
                        vx_scalar minVal, vx_scalar maxVal,
                        vx_array minLoc, vx_array maxLoc,
                        vx_scalar minCount, vx_scalar maxCount);

VX_API vx_status vxuConvertDepth(vx_context context, vx_image input, vx_image output, vx_enum policy, vx_int32 shift);

VX_API vx_status vxuCannyEdgeDetector(vx_context context, vx_image input, vx_threshold hyst,
                               vx_int32 gradient_size, vx_enum norm_type,
                               vx_image output);

VX_API vx_status vxuHalfScaleGaussian(vx_context context, vx_image input, vx_image output, vx_int32 kernel_size);

VX_API vx_status vxuAnd(vx_context context, vx_image in1, vx_image in2, vx_image out);

VX_API vx_status vxuOr(vx_context context, vx_image in1, vx_image in2, vx_image out);

VX_API vx_status vxuXor(vx_context context, vx_image in1, vx_image in2, vx_image out);

VX_API vx_status vxuNot(vx_context context, vx_image input, vx_image output);

VX_API vx_status vxuMultiply(vx_context context, vx_image in1, vx_image in2, vx_float32 scale, vx_enum overflow_policy, vx_enum rounding_policy, vx_image out);

VX_API vx_status vxuAdd(vx_context context, vx_image in1, vx_image in2, vx_enum policy, vx_image out);

VX_API vx_status vxuSubtract(vx_context context, vx_image in1, vx_image in2, vx_enum policy, vx_image out);

VX_API vx_status vxuWarpAffine(vx_context context, vx_image input, vx_matrix matrix, vx_enum type, vx_image output);

VX_API vx_status vxuWarpPerspective(vx_context context, vx_image input, vx_matrix matrix, vx_enum type, vx_image output);

VX_API vx_status vxuHarrisCorners(vx_context context,
                           vx_image input,
                           vx_scalar strength_thresh,
                           vx_scalar min_distance,
                           vx_scalar sensitivity,
                           vx_int32 gradient_size,
                           vx_int32 block_size,
                           vx_array corners,
                           vx_scalar num_corners);


VX_API vx_status vxuFastCorners(vx_context context, vx_image input, vx_scalar strength_thresh, vx_bool nonmax_suppression, vx_array corners, vx_scalar num_corners);

VX_API vx_status vxuOpticalFlowPyrLK(vx_context context,
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

VX_API vx_status vxuRemap(vx_context context,
                  vx_image input,
                  vx_remap table,
                  vx_enum policy,
                  vx_image output);

#ifdef __cplusplus
}
#endif

#endif
