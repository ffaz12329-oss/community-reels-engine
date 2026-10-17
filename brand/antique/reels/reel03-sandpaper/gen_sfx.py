"""Synthesised, licence-free sound effects for the sandpaper Reel (FFmpeg only). Every sound has a different character."""
import subprocess
def ff(graph, out, dur):
    subprocess.run(["ffmpeg","-v","error","-y","-filter_complex",graph,"-map","[o]","-t",str(dur),"-ar","48000","-ac","2","-c:a","pcm_s16le",out],check=True)
ST="pan=stereo|c0=c0|c1=c0"
# 1 hit: soft low-impact body + a short mid 'knock' (hook headline)
ff("aevalsrc='0.85*sin(2*PI*(44+70*exp(-t*28))*t)*exp(-t*6.5)*min(1,t*500)':d=0.9:s=48000,"+ST+"[a];"
   "anoisesrc=d=0.9:c=pink:r=48000:a=0.5,bandpass=f=900:w=1400,volume='exp(-t*38)':eval=frame,"+ST+"[b];[a][b]amix=inputs=2:normalize=0[o]","sfx/hit.wav",0.9)
# 2 whoosh_hook: rises into the hit (peak at 0.30 s, then cut)
ff("anoisesrc=d=0.5:c=white:r=48000:a=0.8,asplit=3[a][b][c];"
   "[a]lowpass=f=800,volume='exp(-pow((t-0.22)/0.09,2))':eval=frame[a1];"
   "[b]highpass=800,lowpass=4200,volume='exp(-pow((t-0.27)/0.08,2))':eval=frame[b1];"
   "[c]highpass=4200,lowpass=10000,volume='exp(-pow((t-0.30)/0.06,2))':eval=frame[c1];"
   "[a1][b1][c1]amix=inputs=3:normalize=0,"+ST+"[o]","sfx/whoosh_hook.wav",0.5)
# 3 swish_paper: short bright paper-like swish (transition 1)
ff("anoisesrc=d=0.32:c=white:r=48000:a=0.8,highpass=f=2200,lowpass=f=8500,volume='exp(-pow((t-0.13)/0.07,2))':eval=frame,"+ST+"[o]","sfx/swish_paper.wav",0.32)
# 4 whoosh_soft: low soft whoosh moving right -> left (transition 2)
ff("anoisesrc=d=0.6:c=white:r=48000:a=0.8,asplit=2[l][r];[l]lowpass=f=2500,highpass=f=250,volume='exp(-pow((t-0.32)/0.13,2))':eval=frame[L];"
   "[r]lowpass=f=2500,highpass=f=250,volume='exp(-pow((t-0.18)/0.13,2))':eval=frame[R];[L][R]amerge=inputs=2,pan=stereo|c0=c0|c1=c1[o]","sfx/whoosh_soft.wav",0.6)
# 5 breath: longer airy sweep, mid band (transition 3)
ff("anoisesrc=d=0.8:c=pink:r=48000:a=0.9,highpass=f=700,lowpass=f=3800,volume='exp(-pow((t-0.40)/0.16,2))':eval=frame,"+ST+"[o]","sfx/breath.wav",0.8)
# 6 tick: crisp label tick
ff("anoisesrc=d=0.05:c=white:r=48000:a=0.9,highpass=f=2800,lowpass=f=9000,volume='exp(-t*190)':eval=frame,"+ST+"[o]","sfx/tick.wav",0.05)
# 7 swish_label: tactile micro swish under a label reveal
ff("anoisesrc=d=0.2:c=white:r=48000:a=0.8,highpass=f=3200,lowpass=f=9500,volume='exp(-pow((t-0.08)/0.045,2))':eval=frame,"+ST+"[o]","sfx/swish_label.wav",0.2)
# 8 zip: scratch-trace sweep, bright and narrow
ff("anoisesrc=d=0.45:c=white:r=48000:a=0.8,highpass=f=5000,lowpass=f=11000,asplit=2[l][r];[l]volume='exp(-pow((t-0.26)/0.07,2))':eval=frame[L];"
   "[r]volume='exp(-pow((t-0.16)/0.07,2))':eval=frame[R];[L][R]amerge=inputs=2,pan=stereo|c0=c0|c1=c1[o]","sfx/zip.wav",0.45)
# 9 pop: decision-graphic accent (round, soft)
ff("aevalsrc='0.9*sin(2*PI*(380+360*exp(-t*55))*t)*exp(-t*30)*min(1,t*700)':d=0.2:s=48000,"+ST+"[o]","sfx/pop.wav",0.2)
# 10 chime: soft two-note final accent
ff("aevalsrc='(0.5*sin(2*PI*659.3*t)+0.18*sin(2*PI*1318.6*t))*exp(-t*3.2)*min(1,t*300)+(0.45*sin(2*PI*987.8*t)+0.16*sin(2*PI*1975.6*t))*exp(-(t-0.18)*3.0)*min(1,max(0,t-0.18)*300)*gt(t,0.18)':d=1.8:s=48000,"+ST+"[o]","sfx/chime.wav",1.8)
# 11 brush: soft brushing strokes (about 4.5 strokes per second)
ff("anoisesrc=d=1.8:c=white:r=48000:a=0.8,highpass=f=1800,lowpass=f=7200,volume='pow(abs(sin(2*PI*2.4*t)),1.6)*min(1,t*4)*min(1,(1.8-t)*4)':eval=frame,"+ST+"[o]","sfx/brush.wav",1.8)
import json
peaks={}
for n in ("hit","whoosh_hook","swish_paper","whoosh_soft","breath","tick","swish_label","zip","pop","chime","brush"):
    r=subprocess.run(["ffmpeg","-hide_banner","-i",f"sfx/{n}.wav","-af","astats=metadata=0","-f","null","-"],capture_output=True,text=True).stderr
    pk=[float(l.split(":")[1]) for l in r.splitlines() if "Peak level dB" in l][0]; peaks[n]=pk
json.dump(peaks,open("sfx/peaks.json","w")); print(peaks)
