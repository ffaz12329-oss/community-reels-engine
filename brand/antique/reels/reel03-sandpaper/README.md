# ANTIQUE reel 03 — coarse vs fine sandpaper (editable source)

Source of the reel `ANTIQUE_Reel03_Sandpaper_Draft02.mp4` (1080×1920, 30 fps, 40.5 s). Media is not stored here (the repository ignores mp4/mov).

1. Put the two supplied files in `source/`: `clips_gemini.mp4` (720×1280 generated video) and `voice.mov` (the voice recording).
2. Run `./make.sh` (needs ffmpeg and the repository's `npm ci`).

- `captions.json` — the subtitles (`<k>` marks keywords). `check: true` = wording to be confirmed by the creator; edit and re-run `build_overlay.py`, the HyperFrames render and `compose.sh`.
- `build_overlay.py` — every on-screen graphic and its timing (HyperFrames HTML + GSAP, Cairo font).
- `build_base.py` — picture timing from the voice (cuts, slow-downs, zoom, colour balance).
- `mix_audio.py` + `gen_sfx.py` + `build_foley.py` + `build_voice.py` — audio. All effects are synthesised, so there are no licensing issues.
- `timeline.md` — the list of graphics and sounds with times. `transcript_large_v3_*.json` — local Whisper large-v3 output used to time the speech.
