"""Voice: high-pass 70 Hz + two-pass loudness normalisation to -16 LUFS (linear). No cutting, no speed change; padded with silence to the 40.5 s reel."""
import json, subprocess
def run(*a): return subprocess.run(a, capture_output=True, text=True)
CH = "highpass=f=70"
m = run("ffmpeg", "-hide_banner", "-i", "source/voice.mov", "-vn", "-af", CH + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
m = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = CH + ",loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true,apad=whole_dur=40.5" % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "source/voice.mov", "-vn", "-af", af, "-ar", "48000", "-c:a", "pcm_s24le", "voice_norm.wav"], check=True)
