#include "openvx.h"
#include <stdio.h>

int main(int ac, char **av) {
    if (ac != 2) {
        fprintf(stderr, "Usage %s <video>\n", av[0]);
        return -1;
    }

    vx_context context = vxCreateContext();
    vx_graph graph = vxCreateGraph(context);

    vx_image img = vxCreateVirtualImage(graph, 0, 0, FOURCC_VIRT);
    vxPlayNode(graph, av[1], img);
    vxShowNode(graph, img, "View");

    vx_status status = vxVerifyGraph(graph);
    if (status == VX_SUCCESS) {
        while (status == VX_SUCCESS) {
            status = vxProcessGraph(graph);
        }
    } else {
        fprintf(stderr, "Verification failed.\n");
    }
    vxReleaseContext(&context); // this will release everything 
    return 0;
}