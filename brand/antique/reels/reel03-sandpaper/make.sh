#!/bin/sh
# Rebuild the reel. Put the two supplied files in ./source/ as clips_gemini.mp4 (the 720x1280 Gemini video) and voice.mov (the voice recording).
# Needs: ffmpeg/ffprobe, python3, and the repository's `npm ci` (HyperFrames, GSAP, @fontsource/cairo).
set -e
python3 gen_sfx.py && python3 build_voice.py && python3 build_foley.py && python3 build_base.py && python3 mix_audio.py
python3 build_overlay.py
HYPERFRAMES_NO_TELEMETRY=1 ../../../../node_modules/.bin/hyperframes render overlay --format webm --output overlay.webm --fps 30 --quality high --workers 2
./compose.sh
