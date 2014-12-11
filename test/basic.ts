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
    ck_assert(vxReleaseParameter(&param) == VX_SUCCESS);
    ck_assert(!param);
