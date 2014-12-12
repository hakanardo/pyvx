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
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);

    param = vxGetParameterByIndex(node, 0);
    vx_reference ref;
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_REF, 
                               &ref, sizeof(ref)) == VX_SUCCESS);
    ck_assert(same_pyobj(ref, (vx_reference) img1));
    ck_assert(vxQueryParameter(param, VX_PARAMETER_ATTRIBUTE_TYPE, 
                               &e, sizeof(e)) == VX_SUCCESS);
    ck_assert(e == VX_TYPE_IMAGE);    
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);
