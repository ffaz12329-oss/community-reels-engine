"""Foley: the clips' own paper / sanding sounds, high-passed (the generated clip carries a constant low hum), time-mapped with the same
speed changes as the picture (atempo), so every rustle stays in sync with the hand that makes it."""
import subprocess
SC = [(1.000, 9.958, 300), (9.958, 20.083, 303), (20.083, 31.0, 385), (31.0, 38.567, 227)]   # same as build_base.py
parts, labels = [], ""
for i, (ss, ee, n) in enumerate(SC):
    dur = n / 30; sp = (ee - ss) / dur
    f = f"[0:a]atrim=start={ss}:end={ee},asetpts=PTS-STARTPTS"
    if abs(sp - 1) > 0.01: f += f",atempo={sp:.5f}"
    parts.append(f + f",apad=whole_dur={dur:.4f},atrim=end={dur:.4f}[a{i}]"); labels += f"[a{i}]"
g = ";".join(parts) + ";" + labels + "concat=n=4:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=1500,lowpass=f=9500[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "source/clips_gemini.mp4", "-filter_complex", g, "-map", "[o]", "-c:a", "pcm_s24le", "foley_raw.wav"], check=True)
