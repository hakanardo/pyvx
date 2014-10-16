#include <string.h>
#include "../glview.h"

void glutMainLoopEvent(void);

static int glut_initiated=0;
static struct glview **windows;
static int n_windows=0;
static int escaped_pressed=0;

#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

void keyboard(unsigned char key, int x, int y) {
  if (key == 27) {
    escaped_pressed=1;
  }
}

void reshape(int w, int h) {
  int i = glutGetWindow();
  if (i < n_windows) {
    float scale=min( ((float)w)/((float)(windows[i]->width)), 
                     ((float)h)/((float)(windows[i]->height)) );
    float dx=(w-scale*(windows[i]->width))/2;
    float dy=(h-scale*(windows[i]->height))/2;
    glViewport(dx, dy, scale*windows[i]->width, scale*windows[i]->height);
  }
}



struct glview *glview_create(int width, int height, int pixel_type, int pixel_size, char *name) {
  if (!glut_initiated) {
    int ac=0;
    char *av[]={"pr"};
    glutInit(&ac,av);
    glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE);
    glut_initiated = 1;
  }

  struct glview *m = malloc(sizeof(struct glview));
  m->name = strdup(name);

  int w=width, h=height;
  while (w<600) {w*=2; h*=2;}
  glutInitWindowSize(w,h);
  m->win=glutCreateWindow(m->name);

  n_windows = max(m->win + 1, n_windows);
  windows = realloc(windows, n_windows * sizeof(struct glview *));
  windows[m->win] = m;

  m->width = width;
  m->height = height;
  m->pixel_type = pixel_type;
  m->pixel_size = pixel_size;

  glEnable(GL_TEXTURE_RECTANGLE_NV);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0, 1, 0, 1);

  unsigned int tex;
  glGenTextures(1, &tex);
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, tex);
  glTexParameteri(GL_TEXTURE_RECTANGLE_NV,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
  glTexParameteri(GL_TEXTURE_RECTANGLE_NV,GL_TEXTURE_MIN_FILTER,GL_NEAREST);

  glTexImage2D(
    GL_TEXTURE_RECTANGLE_NV,    /* texture target */
    0,                          /* mipmap level */
    pixel_type,                 /* texture internal format */
    width,                      /* width */
    height,                     /* height */
    0,                          /* border */
    pixel_type,                 /* pixel format of the image */
    pixel_size,                 /* channel type */
    NULL                        /* image data */
    );
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, 0);
  m->tex=tex;
  glutKeyboardFunc(keyboard);
  glutReshapeFunc(reshape); 

  return m;
}

int glview_next(struct glview *m, unsigned char *imageData) {
  glutSetWindow(m->win);
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, m->tex);
  glTexSubImage2D(GL_TEXTURE_RECTANGLE_NV,0,
      0,0,m->width,m->height,
      m->pixel_type, m->pixel_size, imageData);
  glClearColor(0.0, 0.0, 0.0, 1.0);
  glClear(GL_COLOR_BUFFER_BIT);

  glBegin(GL_QUADS);
  {
    glTexCoord2i(0, m->height);        glVertex2i(0, 0);
    glTexCoord2i(m->width, m->height); glVertex2i(1, 0);
    glTexCoord2i(m->width, 0);         glVertex2i(1, 1);
    glTexCoord2i(0, 0);                glVertex2i(0, 1);
  }
  glEnd();

  glutSwapBuffers();

  //glutMainLoop();
  glutMainLoopEvent();
  return escaped_pressed;
}

void glview_release(struct glview *m) {
  free(m);
}
