#ifndef __AVPLAY_H__
#define __AVPLAY_H__

#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavdevice/avdevice.h>
#include <libswscale/swscale.h>
#include <libavutil/pixfmt.h>

struct avplay {
    AVCodecContext  *codec_ctx;
    AVFormatContext *format_ctx;
    AVCodec * codec;
    AVFrame *frame, *frame_rgb;
    struct SwsContext * convert_ctx;    
    int video_stream_index;
    int64_t pts;
    int width, height;
};


void avplay_seek(struct avplay *p, int64_t pts);
struct avplay *avplay_new(char *fn);
int avplay_next(struct avplay *p, uint8_t *img);

#endif