"""Track the scratch crossings in the opening shot (final 1080x1920 coordinates) so the highlight rings follow them. Template matching, template refreshed each step."""
import cv2, json, numpy as np, subprocess
cap = cv2.VideoCapture("base.mp4"); frames = {}
def frame(t):
    k = int(round(t * 30))
    if k not in frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, k); ok, f = cap.read(); frames[k] = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    return frames[k]
def clahe(g): return cv2.createCLAHE(2.0, (8, 8)).apply(g)
START = {"A": (385, 1090, 150), "B": (770, 1085, 110)}
out = {}
for name, (x0, y0, h) in START.items():
    pts = {1.5: (x0, y0)}
    for direction in (1, -1):
        t, (cx, cy) = 1.5, (x0, y0)
        while True:
            t2 = round(t + direction * 0.1, 2)
            if t2 < 0.1 or t2 > 8.0: break
            a, b = clahe(frame(t)), clahe(frame(t2))
            tpl = a[int(cy - h):int(cy + h), int(cx - h):int(cx + h)]
            S = 70; x1, y1 = int(max(0, cx - h - S)), int(max(0, cy - h - S)); win = b[y1:int(cy + h + S), x1:int(cx + h + S)]
            r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(r)
            cx, cy = x1 + loc[0] + h, y1 + loc[1] + h; pts[t2] = (cx, cy); t = t2
            if mx < 0.35: print(name, "low match", t2, round(mx, 2))
    out[name] = {str(k): [round(v[0], 1), round(v[1], 1)] for k, v in sorted(pts.items())}
json.dump(out, open("scratch_track.json", "w"))
for n in out: print(n, [(k, v) for k, v in out[n].items() if float(k) in (0.3,0.5,0.8,1.0,1.5,2.0,3.0,4.0,5.0,6.0,6.5,7.0,7.5)])
