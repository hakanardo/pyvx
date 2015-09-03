from pyvx.backend import lib, ffi

def ColorConvert(context, input, output):
    '''
:brief: [Immediate] Invokes an immediate Color Conversion.
:param: [in] context The reference to the overall context.
:param: [in] input The input image.
:param: [out] output The output image.
:ingroup: group_vision_function_colorconvert
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuColorConvert(context, input, output)
    
def ChannelExtract(context, input, channel, output):
    '''
:brief: [Immediate] Invokes an immediate Channel Extract.
:param: [in] context The reference to the overall context.
:param: [in] input The input image. Must be one of the defined *vx_df_image_e* multiplanar formats.
:param: [in] channel The *vx_channel_e* enumeration to extract.
:param: [out] output The output image. Must be *VX_DF_IMAGE_U8*.
:ingroup: group_vision_function_channelextract
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuChannelExtract(context, input, channel, output)
    
def ChannelCombine(context, plane0, plane1, plane2, plane3, output):
    '''
:brief: [Immediate] Invokes an immediate Channel Combine.
:param: [in] context The reference to the overall context.
:param: [in] plane0 The plane that forms channel 0. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane1 The plane that forms channel 1. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane2 [optional] The plane that forms channel 2. Must be *VX_DF_IMAGE_U8*.
:param: [in] plane3 [optional] The plane that forms channel 3. Must be *VX_DF_IMAGE_U8*.
:param: [out] output The output image.
:ingroup: group_vision_function_channelcombine
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuChannelCombine(context, plane0, plane1, plane2, plane3, output)
    
def Sobel3x3(context, input, output_x, output_y):
    '''
:brief: [Immediate] Invokes an immediate Sobel 3x3.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output_x [optional] The output gradient in the x direction in *VX_DF_IMAGE_S16*.
:param: [out] output_y [optional] The output gradient in the y direction in *VX_DF_IMAGE_S16*.
:ingroup: group_vision_function_sobel3x3
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuSobel3x3(context, input, output_x, output_y)
    
def Magnitude(context, grad_x, grad_y, output):
    '''
:brief: [Immediate] Invokes an immediate Magnitude.
:param: [in] context The reference to the overall context.
:param: [in] grad_x The input x image. This must be in *VX_DF_IMAGE_S16* format.
:param: [in] grad_y The input y image. This must be in *VX_DF_IMAGE_S16* format.
:param: [out] output The magnitude image. This will be in *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_magnitude
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuMagnitude(context, grad_x, grad_y, output)
    
def Phase(context, grad_x, grad_y, output):
    '''
:brief: [Immediate] Invokes an immediate Phase.
:param: [in] context The reference to the overall context.
:param: [in] grad_x The input x image. This must be in *VX_DF_IMAGE_S16* format.
:param: [in] grad_y The input y image. This must be in *VX_DF_IMAGE_S16* format.
:param: [out] output The phase image. This will be in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_phase
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuPhase(context, grad_x, grad_y, output)
    
def ScaleImage(context, src, dst, type):
    '''
:brief: [Immediate] Scales an input image to an output image.
:param: [in] context The reference to the overall context.
:param: [in] src The source image of type *VX_DF_IMAGE_U8*.
:param: [out] dst The destintation image of type *VX_DF_IMAGE_U8*.
:param: [in] type The interpolation type. :see: vx_interpolation_type_e.
:ingroup: group_vision_function_scale_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuScaleImage(context, src, dst, type)
    
def TableLookup(context, input, lut, output):
    '''
:brief: [Immediate] Processes the image through the LUT.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8*
:param: [in] lut The LUT which is of type VX_TYPE_UINT8
:param: [out] output The output image of type *VX_DF_IMAGE_U8*
:ingroup: group_vision_function_lut
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuTableLookup(context, input, lut, output)
    
def Histogram(context, input, distribution):
    '''
:brief: [Immediate] Generates a distribution from an image.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8*
:param: [out] distribution The output distribution.
:ingroup: group_vision_function_histogram
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuHistogram(context, input, distribution)
    
def EqualizeHist(context, input, output):
    '''
:brief: [Immediate] Equalizes the Histogram of a grayscale image.
:param: [in] context The reference to the overall context.
:param: [in] input The grayscale input image in *VX_DF_IMAGE_U8*
:param: [out] output The grayscale output image of type *VX_DF_IMAGE_U8* with equalized brightness and contrast.
:ingroup: group_vision_function_equalize_hist
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuEqualizeHist(context, input, output)
    
def AbsDiff(context, in1, in2, out):
    '''
:brief: [Immediate] Computes the absolute difference between two images.
:param: [in] context The reference to the overall context.
:param: [in] in1 An input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [in] in2 An input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [out] out The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_absdiff
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAbsDiff(context, in1, in2, out)
    
def MeanStdDev(context, input, mean, stddev):
    '''
:brief: [Immediate] Computes the mean value and standard deviation.
:param: [in] context The reference to the overall context.
:param: [in] input The input image. *VX_DF_IMAGE_U8* is supported.
:param: [out] mean The average pixel value.
:param: [out] stddev The standard deviation of the pixel values.
:ingroup: group_vision_function_meanstddev
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuMeanStdDev(context, input, mean, stddev)
    
def Threshold(context, input, thresh, output):
    '''
:brief: [Immediate] Threshold's an input image and produces a *VX_DF_IMAGE_U8* boolean image.
:param: [in] context The reference to the overall context.
:param: [in] input The input image. *VX_DF_IMAGE_U8* is supported.
:param: [in] thresh The thresholding object that defines the parameters of
the operation.
:param: [out] output The output Boolean image. Values are either 0 or 255.
:ingroup: group_vision_function_threshold
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuThreshold(context, input, thresh, output)
    
def IntegralImage(context, input, output):
    '''
:brief: [Immediate] Computes the integral image of the input.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U32* format.
:ingroup: group_vision_function_integral_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuIntegralImage(context, input, output)
    
def Erode3x3(context, input, output):
    '''
:brief: [Immediate] Erodes an image by a 3x3 window.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_erode_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuErode3x3(context, input, output)
    
def Dilate3x3(context, input, output):
    '''
:brief: [Immediate] Dilates an image by a 3x3 window.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_dilate_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuDilate3x3(context, input, output)
    
def Median3x3(context, input, output):
    '''
:brief: [Immediate] Computes a median filter on the image by a 3x3 window.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_median_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuMedian3x3(context, input, output)
    
def Box3x3(context, input, output):
    '''
:brief: [Immediate] Computes a box filter on the image by a 3x3 window.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_box_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuBox3x3(context, input, output)
    
def Gaussian3x3(context, input, output):
    '''
:brief: [Immediate] Computes a gaussian filter on the image by a 3x3 window.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_gaussian_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuGaussian3x3(context, input, output)
    
def Convolve(context, input, matrix, output):
    '''
:brief: [Immediate] Computes a convolution on the input image with the supplied
matrix.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* format.
:param: [in] matrix The convolution matrix.
:param: [out] output The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_custom_convolution
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuConvolve(context, input, matrix, output)
    
def GaussianPyramid(context, input, gaussian):
    '''
:brief: [Immediate] Computes a Gaussian pyramid from an input image.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8*
:param: [out] gaussian The Gaussian pyramid with *VX_DF_IMAGE_U8* to construct.
:ingroup: group_vision_function_gaussian_pyramid
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuGaussianPyramid(context, input, gaussian)
    
def AccumulateImage(context, input, accum):
    '''
:brief: [Immediate] Computes an accumulation.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in,out] accum The accumulation image in *VX_DF_IMAGE_S16*
:ingroup: group_vision_function_accumulate
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAccumulateImage(context, input, accum)
    
def AccumulateWeightedImage(context, input, scale, accum):
    '''
:brief: [Immediate] Computes a weighted accumulation.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] scale A *VX_TYPE_FLOAT32* type, the input value with the range :f:$ 0.0 :le: :alpha: :le: 1.0 :f:$.
:param: [in,out] accum The *VX_DF_IMAGE_U8* accumulation image.
:ingroup: group_vision_function_accumulate_weighted
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAccumulateWeightedImage(context, input, scale, accum)
    
def AccumulateSquareImage(context, input, shift, accum):
    '''
:brief: [Immediate] Computes a squared accumulation.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] shift A *VX_TYPE_UINT32* type, the input value with the range :f:$ 0 :le: shift :le: 15 :f:$.
:param: [in,out] accum The accumulation image in *VX_DF_IMAGE_S16*
:ingroup: group_vision_function_accumulate_square
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAccumulateSquareImage(context, input, shift, accum)
    
def MinMaxLoc(context, input, minVal, maxVal, minLoc, maxLoc, minCount, maxCount):
    '''
:brief: [Immediate] Computes the minimum and maximum values of the image.
:param: [in] context The reference to the overall context.
:param: [in] input The input image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:param: [out] minVal The minimum value in the image.
:param: [out] maxVal The maximum value in the image.
:param: [out] minLoc The minimum locations (optional). If the input image has several minimums, the kernel will return all of them).
:param: [out] maxLoc The maximum locations (optional). If the input image has several maximums, the kernel will return all of them).
:param: [out] minCount The total number of detected minimums in image (optional).
:param: [out] maxCount The total number of detected maximums in image (optional).
:ingroup: group_vision_function_minmaxloc
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuMinMaxLoc(context, input, minVal, maxVal, minLoc, maxLoc, minCount, maxCount)
    
def ConvertDepth(context, input, output, policy, shift):
    '''
:brief: [Immediate] Converts the input images bit-depth into the output image.
:param: [in] context The reference to the overall context.
:param: [in] input The input image.
:param: [out] output The output image.
:param: [in] policy A vx_convert_policy_e enumeration.
:param: [in] shift The shift value.
:ingroup: group_vision_function_convertdepth
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*..
    '''
    return lib.vxuConvertDepth(context, input, output, policy, shift)
    
def CannyEdgeDetector(context, input, hyst, gradient_size, norm_type, output):
    '''
:brief: [Immediate] Computes Canny Edges on the input image into the output image.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] hyst The double threshold for hysteresis.
:param: [in] gradient_size The size of the Sobel filter window, must support at least 3, 5 and 7.
:param: [in] norm_type A flag indicating the norm used to compute the gradient, VX_NORM_L1 or VX_NORM_L2.
:param: [out] output The output image in *VX_DF_IMAGE_U8* format.
:ingroup: group_vision_function_canny
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuCannyEdgeDetector(context, input, hyst, gradient_size, norm_type, output)
    
def HalfScaleGaussian(context, input, output, kernel_size):
    '''
:brief: [Immediate] Performs a Gaussian Blur on an image then half-scales it.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:param: [in] kernel_size The input size of the Gaussian filter. Supported values are 3 and 5.
:ingroup: group_vision_function_scale_image
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuHalfScaleGaussian(context, input, output, kernel_size)
    
def And(context, in1, in2, out):
    '''
:brief: [Immediate] Computes the bitwise and between two images.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image
:param: [in] in2 A *VX_DF_IMAGE_U8* input image
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_and
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAnd(context, in1, in2, out)
    
def Or(context, in1, in2, out):
    '''
:brief: [Immediate] Computes the bitwise inclusive-or between two images.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image
:param: [in] in2 A *VX_DF_IMAGE_U8* input image
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_or
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuOr(context, in1, in2, out)
    
def Xor(context, in1, in2, out):
    '''
:brief: [Immediate] Computes the bitwise exclusive-or between two images.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* input image
:param: [in] in2 A *VX_DF_IMAGE_U8* input image
:param: [out] out The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_xor
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuXor(context, in1, in2, out)
    
def Not(context, input, output):
    '''
:brief: [Immediate] Computes the bitwise not of an image.
:param: [in] context The reference to the overall context.
:param: [in] input The *VX_DF_IMAGE_U8* input image
:param: [out] output The *VX_DF_IMAGE_U8* output image.
:ingroup: group_vision_function_not
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuNot(context, input, output)
    
def Multiply(context, in1, in2, scale, overflow_policy, rounding_policy, out):
    '''
:brief: [Immediate] Performs elementwise multiplications on pixel values in the input images and a scale.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image.
:param: [in] in2 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image.
:param: [in] scale The scale value.
:param: [in] overflow_policy A *vx_convert_policy_e* enumeration.
:param: [in] rounding_policy A *vx_round_policy_e* enumeration.
:param: [out] out The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_mult
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuMultiply(context, in1, in2, scale, overflow_policy, rounding_policy, out)
    
def Add(context, in1, in2, policy, out):
    '''
:brief: [Immediate] Performs arithmetic addition on pixel values in the input images.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image.
:param: [in] in2 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image.
:param: [in] policy A vx_convert_policy_e enumeration.
:param: [out] out The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_add
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuAdd(context, in1, in2, policy, out)
    
def Subtract(context, in1, in2, policy, out):
    '''
:brief: [Immediate] Performs arithmetic subtraction on pixel values in the input images.
:param: [in] context The reference to the overall context.
:param: [in] in1 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image, the minuend.
:param: [in] in2 A *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* input image, the subtrahend.
:param: [in] policy A vx_convert_policy_e enumeration.
:param: [out] out The output image in *VX_DF_IMAGE_U8* or *VX_DF_IMAGE_S16* format.
:ingroup: group_vision_function_sub
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuSubtract(context, in1, in2, policy, out)
    
def WarpAffine(context, input, matrix, type, output):
    '''
:brief: [Immediate] Performs an Affine warp on an image.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] matrix The affine matrix. Must be 2x3 of type VX_TYPE_FLOAT32.
:param: [in] type The interpolation type from vx_interpolation_type_e.
VX_INTERPOLATION_TYPE_AREA is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:ingroup: group_vision_function_warp_affine
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuWarpAffine(context, input, matrix, type, output)
    
def WarpPerspective(context, input, matrix, type, output):
    '''
:brief: [Immediate] Performs an Perspective warp on an image.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] matrix The perspective matrix. Must be 3x3 of type VX_TYPE_FLOAT32.
:param: [in] type The interpolation type from vx_interpolation_type_e.
VX_INTERPOLATION_TYPE_AREA is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:ingroup: group_vision_function_warp_perspective
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuWarpPerspective(context, input, matrix, type, output)
    
def HarrisCorners(context, input, strength_thresh, min_distance, sensitivity, gradient_size, block_size, corners, num_corners):
    '''
:brief: [Immediate] Computes the Harris Corners over an image and produces the array of scored points.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] strength_thresh The *VX_TYPE_FLOAT32* minimum threshold which to eliminate Harris Corner scores (computed using the normalized Sobel kernel).
:param: [in] min_distance The *VX_TYPE_FLOAT32* radial Euclidean distance for non-maximum suppression.
:param: [in] sensitivity The *VX_TYPE_FLOAT32* scalar sensitivity threshold :f:$ k :f:$ from the Harris-Stephens equation.
:param: [in] gradient_size The gradient window size to use on the input. The
implementation must support at least 3, 5, and 7.
:param: [in] block_size The block window size used to compute the harris corner score.
The implementation must support at least 3, 5, and 7.
:param: [out] corners The array of *VX_TYPE_KEYPOINT* structs.
:param: [out] num_corners The total number of detected corners in image (optional). Use a VX_TYPE_SIZE scalar
:ingroup: group_vision_function_harris
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuHarrisCorners(context, input, strength_thresh, min_distance, sensitivity, gradient_size, block_size, corners, num_corners)
    
def FastCorners(context, input, strength_thresh, nonmax_suppression, corners, num_corners):
    '''
:brief: [Immediate] Computes corners on an image using FAST algorithm and produces the array of feature points.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] strength_thresh Threshold on difference between intensity of the central pixel and pixels on Bresenham's circle of radius 3 (*VX_TYPE_FLOAT32* scalar)
:param: [in] nonmax_suppression If true, non-maximum suppression is applied to
detected corners before being places in the *vx_array* of *VX_TYPE_KEYPOINT* structs.
:param: [out] corners Output corner *vx_array* of *VX_TYPE_KEYPOINT*.
:param: [out] num_corners The total number of detected corners in image (optional). Use a VX_TYPE_SIZE scalar.
:ingroup: group_vision_function_fast
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:         An error occurred. See *vx_status_e*.
    '''
    return lib.vxuFastCorners(context, input, strength_thresh, nonmax_suppression, corners, num_corners)
    
def OpticalFlowPyrLK(context, old_images, new_images, old_points, new_points_estimates, new_points, termination, epsilon, num_iterations, use_initial_estimate, window_dimension):
    '''
:brief: [Immediate] Computes an optical flow on two images.
:param: [in] context The reference to the overall context.
:param: [in] old_images Input of first (old) image pyramid
:param: [in] new_images Input of destination (new) image pyramid
:param: [in] old_points an array of key points in a vx_array of *VX_TYPE_KEYPOINT* those key points are defined at
 the old_images high resolution pyramid
:param: [in] new_points_estimates an array of estimation on what is the output key points in a *vx_array* of
*VX_TYPE_KEYPOINT* those keypoints are defined at the new_images high resolution pyramid
:param: [out] new_points an output array of key points in a *vx_array* of *VX_TYPE_KEYPOINT* those key points are
 defined at the new_images high resolution pyramid
:param: [in] termination termination can be *VX_TERM_CRITERIA_ITERATIONS* or *VX_TERM_CRITERIA_EPSILON* or
*VX_TERM_CRITERIA_BOTH*
:param: [in] epsilon is the *vx_float32* error for terminating the algorithm
:param: [in] num_iterations is the number of iterations. Use a *VX_TYPE_UINT32* scalar.
:param: [in] use_initial_estimate Can be set to either *vx_false_e* or *vx_true_e*.
:param: [in] window_dimension The size of the window on which to perform the algorithm. See 
 *VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION*

:ingroup: group_vision_function_opticalflowpyrlk
:return: A *vx_status_e* enumeration.
:retval: VX_SUCCESS Success
:retval:An error occurred. See *vx_status_e*.
    '''
    return lib.vxuOpticalFlowPyrLK(context, old_images, new_images, old_points, new_points_estimates, new_points, termination, epsilon, num_iterations, use_initial_estimate, window_dimension)
    
def Remap(context, input, table, policy, output):
    '''
:brief: [Immediate] Remaps an output image from an input image.
:param: [in] context The reference to the overall context.
:param: [in] input The input *VX_DF_IMAGE_U8* image.
:param: [in] table The remap table object.
:param: [in] policy The interpolation policy from vx_interpolation_type_e.
VX_INTERPOLATION_TYPE_AREA is not supported.
:param: [out] output The output *VX_DF_IMAGE_U8* image.
:return: A *vx_status_e* enumeration.
:ingroup: group_vision_function_remap
    '''
    return lib.vxuRemap(context, input, table, policy, output)
    