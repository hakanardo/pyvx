#ifndef __GLVIEW__H__
#define __GLVIEW__H__

#include <GL/glut.h>

struct glview;
struct glview *glview_create(int width, int height, int pixel_type, int pixel_size, char *name);
void glview_next(struct glview *m, unsigned char *imageData);

#endif