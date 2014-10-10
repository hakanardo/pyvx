#include "openvx.h"
#include <stdio.h>

int main(int ac, char **av) {
    char *path;
    if (ac > 2) {
        fprintf(stderr, "Usage %s <video>\n", av[0]);
        return -1;
    } else if (ac == 2) {
        path = av[1];
    } else {
        path = "v4l2:///dev/video0";
    }

    vx_context context = vxCreateContext();
    vx_graph graph = vxCreateGraph(context);

    vx_image img = vxCreateVirtualImage(graph, 0, 0, FOURCC_VIRT);
    vxPlayNode(graph, path, img);
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