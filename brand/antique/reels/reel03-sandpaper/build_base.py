"""ANTIQUE sandpaper Reel: base picture. Source: one 720x1280 / 24 fps Gemini video made of four hard-cut clips
(0-9.958 scratches | 9.958-20.083 grit comparison | 20.083-31.0 sanding the edge + dust sweep | 31.0-41.0 before/after).
Scene lengths follow the voice: out time == voice time. C3 is slowed to 0.85 so the dust sweep lands on the spoken 'clean the dust'."""
import subprocess, json
FPS = 30
SCENES = {   # (src_start, src_end, out_frames, zoom_expr, colour)
 1: (1.000, 9.958, 300, "1+0.20*(1-pow(1-min(on/27,1),3))+0.07*on/300", ("0.62", "0.5"), "colorchannelmixer=rr=1.19:rg=0:rb=0:gr=0:gg=1.15:gb=0:br=0:bb=1.12"),
 2: (9.958, 20.083, 303, "1+0.06*on/303", ("0.5", "0.5"), None),
 3: (20.083, 31.0, 385, "1+0.07*on/385", ("0.5", "0.55"), None),
 4: (31.0, 38.567, 227, "1+0.05*on/227", ("0.5", "0.5"), "colorchannelmixer=rr=1.03:gg=1.0:bb=0.97"),
}
N = [v[2] for v in SCENES.values()]
if __name__ == "__main__":
    for k, (ss, ee, n, z, (ax, ay), col) in SCENES.items():
        speed = (ee - ss) / (n / FPS)
        f = f"[0:v]trim=start={ss}:end={ee},setpts=(PTS-STARTPTS)/{speed:.6f},"
        f += "fps=30," if abs(speed - 1) < 0.01 else "framerate=fps=30:scene=100,"
        f += f"tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos"
        if col: f += "," + col
        f += ",unsharp=5:5:0.5:5:5:0.0,format=yuv420p,setsar=1"
        f += f",scale=2160:3840:flags=bilinear,zoompan=z='{z}':x='(iw-iw/zoom)*{ax}':y='(ih-ih/zoom)*{ay}':d=1:s=1080x1920:fps=30,setsar=1[v]"
        out = f"scenes/scene{k}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "source/clips_gemini.mp4", "-filter_complex", f, "-map", "[v]", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-an", out], check=True)
        pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "json", out], capture_output=True, text=True).stdout)["streams"][0]
        print(f"scene{k}: speed {speed:.4f}  expected {n} frames, got {pr['nb_read_frames']}", flush=True)
    OV = 6; H = OV // 2; chains = []
    for k, n in enumerate(N, 1):
        head, tail = (H if k > 1 else 0), (H if k < len(N) else 0)
        g = f"[{k-1}:v]"
        if head or tail:
            g += "tpad=" + ":".join(x for x in ([f"start_mode=clone:start={head}"] if head else []) + ([f"stop_mode=clone:stop={tail}"] if tail else [])) + ","
        chains.append(g + "setpts=PTS-STARTPTS,fps=30,format=yuv420p[s%d]" % k)
    acc, length = "s1", N[0] + H
    for k in range(2, len(N) + 1):
        ext = N[k - 1] + H + (H if k < len(N) else 0)
        chains.append(f"[{acc}][s{k}]xfade=transition=fade:duration={OV/30:.4f}:offset={(length - OV)/30:.4f}[x{k}]")
        acc, length = f"x{k}", length - OV + ext
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + sum([["-i", f"scenes/scene{k}.mp4"] for k in range(1, len(N) + 1)], []) + ["-filter_complex", ";".join(chains), "-map", f"[{acc}]", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-an", "base.mp4"], check=True)
    print(json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "json", "base.mp4"], capture_output=True, text=True).stdout)["streams"][0], "(+1 frame is padded at composite time; expected total", sum(N), ")")
