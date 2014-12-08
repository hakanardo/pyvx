#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include "../avplay.h"

static int libav_initiated = 0;

struct avplay *avplay_new(char *fn) {
    struct avplay *p = calloc(sizeof(struct  avplay), 1);
    if (!libav_initiated) {
        av_register_all();
        avcodec_register_all();
        avdevice_register_all();
        avformat_network_init();
        libav_initiated = 1;
    }

    AVInputFormat   *iFormat = NULL; 
    int v4l = 0;
    if (!strncmp(fn, "v4l2://", 7)) {
        fn += 7;
        v4l = 1;
    } else if (!strncmp(fn, "/dev/video", 10)) {
        v4l = 1;
    }
    if (v4l) {
        const char      formatName[] = "video4linux2";
        if (!(iFormat = av_find_input_format(formatName))) { 
             printf("can't find input format %s\n", formatName); 
             return NULL; 
        }
    } 

    
    p->format_ctx = avformat_alloc_context();
    if (avformat_open_input(&p->format_ctx, fn, iFormat, NULL) != 0) return NULL;
    if (avformat_find_stream_info(p->format_ctx, NULL) < 0) return NULL;
    int i;
    p->video_stream_index = -1;
    for (i=0; i < p->format_ctx->nb_streams; i++) {
        if (p->format_ctx->streams[i]->codec->coder_type == AVMEDIA_TYPE_VIDEO) {
            p->video_stream_index = i;
            break;
        }
    }
    if (p->video_stream_index == -1) return NULL;
    p->codec_ctx = p->format_ctx->streams[p->video_stream_index]->codec;
    p->codec = avcodec_find_decoder(p->codec_ctx->codec_id);
    if (p->codec == NULL) return NULL;
 
    if (avcodec_open2(p->codec_ctx, p->codec,NULL) < 0) return NULL;
#if LIBAVCODEC_VERSION_INT >= AV_VERSION_INT(55,28,1)
    p->frame    = av_frame_alloc();
#else
    p->frame = avcodec_alloc_frame();
#endif

    uint8_t *buffer;
    int numBytes;
 
#ifdef AV_PIX_FMT_RGB24
    enum AVPixelFormat pFormat = AV_PIX_FMT_RGB24;
#else
    enum PixelFormat pFormat = PIX_FMT_RGB24;
#endif

    numBytes = avpicture_get_size(pFormat, p->codec_ctx->width, p->codec_ctx->height);
    buffer = (uint8_t *) av_malloc(numBytes*sizeof(uint8_t));
    if (!buffer) return NULL;

    p->convert_ctx = sws_getCachedContext(NULL, p->codec_ctx->width, 
                                              p->codec_ctx->height, p->codec_ctx->pix_fmt,
                                              p->codec_ctx->width, p->codec_ctx->height, 
                                              pFormat, SWS_BICUBIC, NULL, NULL, NULL);

    p->width = p->codec_ctx->width;
    p->height = p->codec_ctx->height;
    return p;
}

int avplay_next(struct avplay *p, uint8_t *img) {
    while (1) {
        AVPacket packet;
        int frame_ok = av_read_frame(p->format_ctx, &packet);
        if (frame_ok < 0) packet.size = 0;
        if(packet.stream_index == p->video_stream_index) {
            if (packet.size == 54) { // Hack to remove Axis system-timestamps
                uint32_t *data = (uint32_t *) packet.data;
                if (data[4] == 0xAAAAAAAA) continue;
            }
            int frameFinished;
            avcodec_decode_video2(p->codec_ctx, p->frame, &frameFinished, &packet);
            if (frameFinished) {
                p->pts = p->frame->pkt_pts;
                uint8_t *const planes[] = {img};
                const int strides[] = {p->width * 3};
                sws_scale(p->convert_ctx, 
                          (const uint8_t * const *) ((AVPicture*)p->frame)->data, 
                          ((AVPicture*)p->frame)->linesize, 0,
                          p->codec_ctx->height,
                          planes, strides);
                return 0;
            } else if (frame_ok < 0) {
                return -1;
            }
        }
    }
}

void avplay_seek(struct avplay *p, int64_t pts) {
    av_seek_frame(p->format_ctx, p->video_stream_index, pts, 0);
}

