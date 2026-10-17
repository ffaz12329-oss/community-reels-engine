"""Voice (normalised, untouched) + synthesised SFX + the clips' own sanding/paper sounds, both ducked by the voice."""
import subprocess, json
DUR = 40.5
PEAK = json.load(open("sfx/peaks.json"))
EV = [  # (time, sound, target peak dBFS)
 (0.00, "whoosh_hook", -22), (0.30, "hit", -20), (0.70, "zip", -28),
 (6.45, "swish_label", -31), (6.55, "zip", -30),
 (9.87, "swish_paper", -26),
 (11.15, "swish_label", -31), (11.15, "tick", -33),
 (13.15, "swish_label", -31), (13.15, "tick", -33), (15.85, "swish_label", -31), (15.85, "tick", -33),
 (19.78, "whoosh_soft", -27),
 (20.80, "swish_label", -31), (20.80, "tick", -33), (21.00, "tick", -34),
 (23.15, "swish_label", -31), (23.15, "tick", -33), (23.95, "tick", -33), (23.95, "pop", -29),
 (28.78, "tick", -34), (29.33, "tick", -34), (29.88, "tick", -34), (30.43, "tick", -34), (29.05, "swish_label", -31),
 (31.60, "brush", -31),
 (32.10, "swish_label", -31), (32.10, "tick", -33), (32.35, "tick", -34),
 (32.53, "breath", -26),
 (33.95, "zip", -30), (34.15, "tick", -33), (34.45, "tick", -33),
 (34.80, "swish_label", -31), (34.80, "tick", -33), (34.96, "tick", -34), (35.12, "tick", -34), (35.55, "swish_label", -31), (36.10, "pop", -30),
 (37.30, "chime", -27),
]
EV.sort()
if __name__ == "__main__":
    inputs = ["-i", "voice_norm.wav", "-i", "foley_raw.wav"] + sum([["-i", f"sfx/{n}.wav"] for _, n, _ in EV], [])
    parts = ["[1:a]agate=threshold=0.006:ratio=6:attack=8:release=120,alimiter=limit=0.0625:attack=2:release=40:level=disabled,volume=-1dB,apad=whole_dur=%s[fol]" % DUR]
    for i, (t, n, g) in enumerate(EV, 2):
        ms = int(round(max(0, t) * 1000))
        parts.append(f"[{i}:a]volume={g - PEAK[n]:.1f}dB,adelay={ms}|{ms},apad=whole_dur={DUR}[e{i}]")
    n_ev = len(EV)
    parts.append("[fol]" + "".join(f"[e{i}]" for i in range(2, 2 + n_ev)) + f"amix=inputs={n_ev + 1}:normalize=0:duration=longest[bus]")
    parts.append("[0:a]asplit=2[v1][v2]")
    parts.append("[bus][v1]sidechaincompress=threshold=0.04:ratio=4:attack=6:release=160:makeup=1,asplit=2[duck][duckout]")
    parts.append("[v2][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.84:level=disabled:latency=1[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-t", str(DUR), "-ar", "48000", "-c:a", "pcm_s24le", "mix.wav", "-map", "[duckout]", "-t", str(DUR), "-ar", "48000", "-c:a", "pcm_s24le", "sfx_only.wav"], check=True)
    json.dump([{"t": t, "sound": n, "peak_dbfs": g} for t, n, g in EV], open("sfx_events.json", "w"), indent=1)
    print(n_ev, "sound events + foley mixed")
