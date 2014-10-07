#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#include "vlcplay.h"


static unsigned setup(void **opaque, char *chroma, unsigned *width, unsigned *height, unsigned *pitches, unsigned *lines) {
    struct vlcplay *m = (*opaque);
    m->width = width[0];
    m->height = height[0];
    memcpy(chroma, "RV24", 4);
    pitches[0] = m->width * 3;
    pthread_mutex_lock(&m->thrd_mutex);    
    pthread_mutex_unlock(&m->main_mutex);    
    return 1;
}

static void *lock(void *opaque, void **planes) {
    struct vlcplay *m = opaque;
    pthread_mutex_lock(&m->thrd_mutex);        
    planes[0] = m->buf;
    return NULL;
}

static void unlock(void *opaque, void *picture, void *const *planes) {
    struct vlcplay *m = opaque;
    pthread_mutex_unlock(&m->main_mutex);        
}

static void event(const struct libvlc_event_t *e, void *opaque) {
    struct vlcplay *m = opaque;
    m->player_error = 1;
    pthread_mutex_unlock(&m->main_mutex);    
}




struct vlcplay * vlcplay_create(char *path) {
    libvlc_media_t *m;
    struct vlcplay *mod = malloc(sizeof(struct vlcplay));
    pthread_mutex_init(&mod->main_mutex, NULL);
    pthread_mutex_init(&mod->thrd_mutex, NULL);
    pthread_mutex_lock(&mod->main_mutex);


    const char *args[] = {"--no-drop-late-frames", "--no-skip-frames"};
    mod->inst = libvlc_new (2, args);
    mod->buf = NULL;
    mod->player_error = 0;
    //m = libvlc_media_new_location (mod->inst, "http://mycool.movie.com/test.mov");
    m = libvlc_media_new_path (mod->inst, path);
    if (!m) return NULL;

    mod->mp = libvlc_media_player_new_from_media (m);
    if (!mod->mp) return NULL;
    libvlc_media_release (m);
    libvlc_video_set_callbacks(mod->mp, lock, unlock, NULL, mod);
    libvlc_video_set_format_callbacks(mod->mp, setup, NULL);
    libvlc_event_manager_t *vlcEventManager = libvlc_media_player_event_manager(mod->mp);
    libvlc_event_attach(vlcEventManager, libvlc_MediaPlayerEncounteredError, event, mod);
    if (libvlc_media_player_play (mod->mp)) return NULL;

    pthread_mutex_lock (&mod->main_mutex);
    if (mod->player_error) {
        vlcplay_release(&mod);
        return NULL;
    }
    return mod;
}

void vlcplay_next(struct vlcplay *m, unsigned char *buf) {
    m->buf = buf;
    pthread_mutex_unlock(&m->thrd_mutex);
    pthread_mutex_lock(&m->main_mutex);
}


void vlcplay_release(struct vlcplay **m) {
     /* Stop playing */
     libvlc_media_player_stop ((*m)->mp);
     pthread_mutex_unlock(&(*m)->thrd_mutex);

     /* Free the media_player */
     libvlc_media_player_release ((*m)->mp);
 
     libvlc_release ((*m)->inst); 

     if ((*m)->buf) free((*m)->buf);
     pthread_mutex_destroy(&(*m)->main_mutex);
     pthread_mutex_destroy(&(*m)->thrd_mutex);

     free(*m);
     *m = NULL;
}
