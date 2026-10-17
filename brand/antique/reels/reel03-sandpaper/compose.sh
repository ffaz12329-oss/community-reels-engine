#!/bin/sh
# base picture + transparent graphics/subtitles layer + mixed audio -> final MP4 (1080x1920, 30 fps, H.264 + AAC)
set -e
OUT="${1:-ANTIQUE_Reel03_Sandpaper_Draft01.mp4}"
ffmpeg -v error -y -i base.mp4 -c:v libvpx-vp9 -i overlay.webm -i mix.wav \
 -filter_complex "[0:v]tpad=stop_mode=clone:stop=1,setpts=PTS-STARTPTS[b];[1:v]format=yuva420p,setpts=PTS-STARTPTS[o];[b][o]overlay=format=auto:eof_action=pass,format=yuv420p,setsar=1[v]" \
 -map "[v]" -map 2:a -t 40.5 -r 30 -c:v libx264 -preset medium -crf 17 -profile:v high -level 4.2 -pix_fmt yuv420p \
 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
