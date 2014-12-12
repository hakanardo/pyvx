#include <check.h>
#include <stdlib.h>
#include <VX/vx.h>

#suite Basic

#test params
    vx_context context = vxCreateContext();
    vx_graph graph = vxCreateGraph(context);
    vx_image img1 = vxCreateImage(context, 640, 480, VX_DF_IMAGE_UYVY);
    vx_image img2 = vxCreateImage(context, 640, 480, VX_DF_IMAGE_U8);
    vx_node node = vxChannelExtractNode(graph, img1, VX_CHANNEL_Y, img2);
    
    vx_parameter param = vxGetParameterByIndex(node, 1);
    vx_uint32 idx;
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_INDEX, 
                               &idx, sizeof(idx)) == VX_SUCCESS);
    ck_assert(idx == 1);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_INDEX, 
                               &idx, 0) != VX_SUCCESS);
    ck_assert(vxQueryParameter(param, VX_CHANNEL_Y, 
                               &idx, sizeof(idx)) != VX_SUCCESS);
    vx_enum e;
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_DIRECTION, 
                               &e, sizeof(e)) == VX_SUCCESS);
    ck_assert(e == VX_INPUT);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_TYPE, 
                               &e, sizeof(e)) == VX_SUCCESS);
    ck_assert(e == VX_TYPE_ENUM);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_STATE, 
                               &e, sizeof(e)) == VX_SUCCESS);    
    ck_assert(e == VX_PARAMETER_STATE_REQUIRED);
    vx_reference ref;
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(vxAccessScalarValue((vx_scalar) ref, &e) == VX_SUCCESS);
    ck_assert(e == VX_CHANNEL_Y);
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);

    param = vxGetParameterByIndex(node, 1);
    e = VX_CHANNEL_G;
    vx_scalar val = vxCreateScalar(context, VX_TYPE_ENUM, &e);
    ck_assert(vxSetParameterByIndex(node, 1, (vx_reference) val) == VX_SUCCESS);
    e = VX_CHANNEL_Y;
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(vxAccessScalarValue((vx_scalar) ref, &e) == VX_SUCCESS);
    ck_assert(e == VX_CHANNEL_G);
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);

    param = vxGetParameterByIndex(node, 0);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_TYPE, 
                               &e, sizeof(e)) == VX_SUCCESS);
    ck_assert(e == VX_TYPE_IMAGE);    
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(same_pyobj(ref, (vx_reference) img1));
    ck_assert(!same_pyobj(ref, (vx_reference) img2));
    ck_assert(vxSetParameterByIndex(node, 0, (vx_reference) img2) == VX_SUCCESS);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(!same_pyobj(ref, (vx_reference) img1));
    ck_assert(same_pyobj(ref, (vx_reference) img2));
    ck_assert(vxSetParameterByReference(param, (vx_reference) img1) == VX_SUCCESS);
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(same_pyobj(ref, (vx_reference) img1));
    ck_assert(!same_pyobj(ref, (vx_reference) img2));
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);

#test scalar
    vx_context context = vxCreateContext();
    uint8_t bval = 7;
    vx_scalar bscalar = vxCreateScalar(context, VX_TYPE_UINT8, &bval);

    vx_enum e;
    ck_assert(vxQueryScalar(bscalar, VX_SCALAR_ATTRIBUTE_TYPE, &e, sizeof(e)) == VX_SUCCESS);
    ck_assert(e == VX_TYPE_UINT8);

    uint8_t v;
    ck_assert(vxAccessScalarValue(bscalar, &v) == VX_SUCCESS);
    ck_assert(v == bval);

    v = 42;
    ck_assert(vxCommitScalarValue(bscalar, &v) == VX_SUCCESS);

    v = 0;
    ck_assert(vxAccessScalarValue(bscalar, &v) == VX_SUCCESS);
    ck_assert(v == 42);

    ck_assert(vxReleaseScalar(&bscalar) == VX_SUCCESS);
    ck_assert(!bscalar);

