#include <check.h>
#include <stdlib.h>
#include <VX/vx.h>

#suite Demo

#test simple
    vx_context context = vxCreateContext();
    vx_image images[] = {
        vxCreateImage(context, 640, 480, VX_DF_IMAGE_UYVY),
        vxCreateImage(context, 640, 480, VX_DF_IMAGE_U8),
        vxCreateImage(context, 640, 480, VX_DF_IMAGE_U8),
    };
    vx_graph graph = vxCreateGraph(context);
    vx_image virts[] = {
        vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT),
        vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT),
        vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT),
        vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT),
    };
    vxChannelExtractNode(graph, images[0], VX_CHANNEL_Y, virts[0]),
    vxGaussian3x3Node(graph, virts[0], virts[1]),
    vxSobel3x3Node(graph, virts[1], virts[2], virts[3]),
    vxMagnitudeNode(graph, virts[2], virts[3], images[1]),
    vxPhaseNode(graph, virts[2], virts[3], images[2]);
    vx_status status = vxVerifyGraph(graph);
    ck_assert(status == VX_SUCCESS);
    vxReleaseContext(&context); // this will release everything 
    ck_assert(!context);

#test view
    if (!getenv("DISPLAY") || !getenv("DISPLAY")[0]) {
        printf("Skipping, no DISPLAY\n");
    } else {
        vx_context context = vxCreateContext();
        vx_graph graph = vxCreateGraph(context);

        vx_image img = vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT);
        vxPlayNode(graph, "test.avi", img);
        vxShowNode(graph, img, "View");

        vx_status status = vxVerifyGraph(graph);
        ck_assert(status == VX_SUCCESS);
        while (status == VX_SUCCESS) {
            status = vxProcessGraph(graph);
        }
        vxReleaseContext(&context); // this will release everything 
        ck_assert(!context);
    }
