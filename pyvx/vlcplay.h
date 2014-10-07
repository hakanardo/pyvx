#ifndef __VLCPLAY__H__
#define __VLCPLAY__H__

#include <vlc/vlc.h>

struct vlcplay {
    libvlc_media_player_t *mp;
    libvlc_instance_t *inst;
    int width, height;
    unsigned char *buf;
    pthread_mutex_t main_mutex;
    pthread_mutex_t thrd_mutex;
};

struct vlcplay * vlcplay_create(char *path);
void vlcplay_next(struct vlcplay *m, unsigned char *buf);
void vlcplay_release(struct vlcplay **m);

#endif