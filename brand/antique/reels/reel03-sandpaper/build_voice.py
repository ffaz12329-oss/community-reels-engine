"""Voice Draft02: the user's own recording, repaired - never re-recorded or synthesised.
 1. the dead pause between 'لصاحبة مشروع' and 'تعاني' is removed (short crossfade inside the silence)
 2. high-pass 70 Hz, two-pass loudness normalisation to -16 LUFS (linear)
 3. the hard word-tail chops of the recording get a soft natural-sounding decay (band-limited noise tail at the level the word ended at)
 4. a continuous room-tone bed fills the dead-silent gaps between phrases (the 'choppy' feel)."""
import json, subprocess, numpy as np
SR = 48000
CUT_A, CUT_B, XF = 37.295, 37.455, 0.02          # keep [0, CUT_A] + [CUT_B, end]; net removed = CUT_B - CUT_A + XF - ... see SHIFT
SHIFT = (CUT_B - CUT_A) + XF - 0.0                # later material moves earlier by this many seconds
DUR = 40.5
def run(*a): return subprocess.run(a, capture_output=True, text=True)
def pcm(p): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32).reshape(-1, 2)[:, 0].copy()   # left channel (both are identical)
splice = f"[0:a]atrim=0:{CUT_A},asetpts=PTS-STARTPTS[a];[0:a]atrim=start={CUT_B},asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d={XF}:c1=tri:c2=tri,pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1,aresample={SR}[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "source/voice.mov", "-filter_complex", splice, "-map", "[o]", "-c:a", "pcm_s24le", "voice_spliced.wav"], check=True)
CH = "highpass=f=70"
m = run("ffmpeg", "-hide_banner", "-i", "voice_spliced.wav", "-af", CH + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
m = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = CH + ",loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "voice_spliced.wav", "-af", af, "-ar", str(SR), "-c:a", "pcm_s24le", "voice_norm_raw.wav"], check=True)
x = pcm("voice_norm_raw.wav")
# --- hard chops: loud -> near-silence inside 10 ms ---
w = SR // 200; n = len(x) // w
e = 20 * np.log10(np.maximum(1e-7, np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1))))
chops = []; last = -99
for i in range(2, n - 3):
    if e[i - 1:i + 1].max() > -32 and e[i - 1:i + 1].max() - e[i + 1:i + 3].min() >= 22 and i - last > 20:
        chops.append(i); last = i
rng = np.random.default_rng(7)
def bandnoise(L):
    z = rng.standard_normal(L + 2000); S = np.fft.rfft(z); f = np.fft.rfftfreq(len(z), 1 / SR)
    S *= ((f > 150) & (f < 3800)) * (1 / np.sqrt(np.maximum(f, 150) / 150)); z = np.fft.irfft(S)[1000:1000 + L]; return z / np.sqrt((z ** 2).mean())
y = x.copy(); L = int(0.16 * SR); tail_log = []
for i in chops:
    # the chop lands within 1 ms: first sample after the last loud 1-ms block
    a = int((i - 1) * w); b = int((i + 3) * w); blk = SR // 1000
    lv = [np.sqrt((x[k:k + blk] ** 2).mean()) for k in range(a, b, blk)]
    d = a + blk * next((j for j in range(1, len(lv)) if lv[j] < lv[0] * 0.3), 1)
    ref = np.sqrt((x[max(0, d - int(0.02 * SR)):d] ** 2).mean())
    t = np.arange(L) / SR; env = np.exp(-t / 0.045) * np.minimum(1, t / 0.004)
    y[d:d + L] += (bandnoise(L) * env * ref * 0.45).astype(np.float32)
    tail_log.append(round(d / SR, 3))
# --- room-tone bed: continuous, quiet, spectrally soft (pink-ish, 120 Hz - 5 kHz) ---
N = int(DUR * SR); bed = bandnoise(N + SR)[:N]
S = np.fft.rfft(bed); f = np.fft.rfftfreq(N, 1 / SR); S *= (f > 120) * (f < 5000); bed = np.fft.irfft(S, N); bed /= np.sqrt((bed ** 2).mean())
bed *= 10 ** (-47 / 20)
ramp = np.minimum(1, np.arange(N) / (0.15 * SR)); bed *= ramp * np.minimum(1, (N - np.arange(N)) / (0.9 * SR))
out = np.zeros(N, dtype=np.float32); out[:min(N, len(y))] = y[:N]
out += bed.astype(np.float32)
pk = np.abs(out).max()
assert pk < 0.9, pk
import wave
with wave.open("voice_norm.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR)
    q = np.repeat(np.clip(out * 8388607, -8388608, 8388607).astype(np.int32), 2)
    b = np.stack([(q) & 255, (q >> 8) & 255, (q >> 16) & 255], 1).astype(np.uint8).tobytes(); wf.writeframes(b)
json.dump({"cut": [CUT_A, CUT_B, XF], "shift": SHIFT, "tails_at": tail_log, "peak": float(pk)}, open("voice_edit.json", "w"), indent=1)
print("splice shift %.3f s; soft tails at %s; peak %.3f" % (SHIFT, tail_log, pk))
