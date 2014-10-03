#include "openvx.h"
#include <stdio.h>

int main() {
    vx_context c = vxCreateContext();
    printf("%d\n", c);
    return 0;
}