#include "openvx.h"
#include <stdio.h>

int main() {
    vx_context c = vxCreateContext();
    vx_image img = vxCreateImage(c, 640, 480, FOURCC_RGB);
    printf("%d, %d\n", c, img);
    return 0;
}