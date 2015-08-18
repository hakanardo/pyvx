#ifndef __GLVIEW__H__
#define __GLVIEW__H__

#include <GL/glut.h>

struct glview {
  int win;
  char *name;
  unsigned int tex;
  int width, height;
  int pixel_type, pixel_size;
};

struct glview *glview_create(int width, int height, int pixel_type, int pixel_size, char *name);
int glview_next(struct glview *m, unsigned char *imageData);
void glview_release(struct glview *m);

#endif