"""ANTIQUE sandpaper Reel: transparent graphics + subtitle layer (HyperFrames -> alpha WebM). One design system: Cairo, ivory / sand / caramel / espresso."""
import json, re, shutil
from pathlib import Path
ROOT = Path("/home/user/community-reels-engine"); OUT = Path("overlay"); (OUT / "assets").mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "node_modules/gsap/dist/gsap.min.js", OUT / "assets/gsap.min.js")
face = ""
for subset, fam in (("arabic", "ReelArabic"), ("latin", "ReelLatin")):
    for w in (500, 700, 800):
        f = ROOT / f"node_modules/@fontsource/cairo/files/cairo-{subset}-{w}-normal.woff2"; shutil.copy2(f, OUT / "assets" / f.name)
        face += f"@font-face{{font-family:{fam};src:url(assets/{f.name});font-weight:{w}}}"
DUR = 40.5
CAPS = json.load(open("captions.json"))

def kw_times(c):
    """Estimate when each keyword is spoken: position of its first letter within the phrase, spread over the phrase length."""
    plain = re.sub(r"</?k>", "", c["text"]); out = []
    for m in re.finditer(r"<k>(.*?)</k>", c["text"]):
        before = re.sub(r"</?k>", "", c["text"][:m.start()])
        out.append(round(c["start"] + max(0.0, (c["end"] - c["start"] - 0.25)) * len(before) / max(1, len(plain)), 2))
    return out

TRK = json.load(open("scratch_track.json"))
def kf(name, t0=0.5, t1=7.6, step=0.5):
    pts = TRK[name]; ks = sorted(float(k) for k in pts); out = []
    t = t0
    while t <= t1 + 1e-6:
        k = min(ks, key=lambda q: abs(q - t)); out.append([round(t, 2), pts[str(k) if str(k) in pts else "%.1f" % k][0], pts[str(k) if str(k) in pts else "%.1f" % k][1]]); t += step
    return out
TRACK_JS = json.dumps({"A": kf("A"), "B": kf("B")})
CUTS = [10.0, 20.1, 32.93]     # the picture cuts (frames 300 / 603 / 988) that the swipes cover
els = []
def sec(id_, start, end, track, inner, cls="full"):
    els.append(f'<section id="{id_}" class="clip {cls}" data-start="{start}" data-duration="{end - start:.2f}" data-track-index="{track}">{inner}</section>')

PANEL = '<div class="pan"><div class="pw" data-layout-allow-overflow="true"><div class="bg"></div><div class="e1"></div><div class="e2"></div><div class="e3"></div><div class="e4"></div><div class="mk"></div><div class="dt"></div></div></div>'
for n, tc in enumerate(CUTS):
    sec(f"tr{n}", round(tc - 0.50, 2), round(tc + 0.55, 2), 1 + n, PANEL, "full")
# ---- subtitles: every spoken phrase (Cairo Medium; keywords Cairo ExtraBold in caramel) ----
caps_js = []
for i, c in enumerate(CAPS):
    html_ = re.sub(r"<k>(.*?)</k>", r'<k><i class="u"></i>\1</k>', c["text"])
    sec(f"cap{i}", c["start"], c["end"], 20, f'<p>{html_}</p>', "cap")
    caps_js.append({"i": i, "a": c["start"], "b": c["end"], "k": kw_times(c)})

# ---- 1. hook (0.30-3.6): brush stroke + kinetic headline + light sweep + scratch trace ----
sec("hook", 0.30, 7.70, 2, '''
<div class="sweep"></div>
<svg class="full" viewBox="0 0 1080 1920"><g id="brk" fill="none" stroke="#fbf6ee" stroke-width="6" stroke-linecap="round" opacity="0.92">
 <path d="M96 928 V892 Q96 884 104 884 H152"/><path d="M954 928 V892 Q954 884 946 884 H898"/>
 <path d="M96 1496 V1532 Q96 1540 104 1540 H152"/><path d="M954 1496 V1532 Q954 1540 946 1540 H898"/></g>
 <g id="rgA" opacity="0"><circle class="r1" cx="0" cy="0" r="150" fill="none" stroke="#fffaf0" stroke-width="6" stroke-linecap="round"/><circle class="r2" cx="0" cy="0" r="150" fill="none" stroke="#fffaf0" stroke-width="3" opacity="0"/><line class="ld" x1="0" y1="-152" x2="0" y2="-196" stroke="#fffaf0" stroke-width="4" stroke-linecap="round"/></g>
 <g id="rgB" opacity="0"><circle class="r1" cx="0" cy="0" r="104" fill="none" stroke="#fffaf0" stroke-width="5" stroke-linecap="round"/><circle class="r2" cx="0" cy="0" r="104" fill="none" stroke="#fffaf0" stroke-width="3" opacity="0"/></g></svg>
<div class="chip sc" id="sctag"><b>خدوش</b></div>
<div class="hk"><svg class="brush" viewBox="0 0 940 440"><defs><filter id="rough" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.09" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="26"/></filter></defs>
 <path d="M30 70 Q250 22 470 52 T910 40 L900 380 Q650 430 430 392 T36 404 Z" fill="#e4ceba" filter="url(#rough)"/></svg>
 <div class="l1" data-layout-allow-overlap="true">الصنفرة</div><div class="l2"><span class="w" data-layout-allow-overlap="true">زادت</span> <span class="w st" data-layout-allow-overlap="true">الخدوش؟!</span></div>
 <svg class="scr" viewBox="0 0 640 40"><path d="M10 12 L250 24 M60 30 L330 14 M300 28 L620 20" stroke="#8c3d1c" stroke-width="5" stroke-linecap="round" fill="none"/></svg></div>''')

# ---- 2a. risk phrase (spoken 'علامات واضحة') ----
sec("risk", 11.15, 12.80, 3, '<div class="chip dark" style="left:200px;top:262px;width:680px"><b>علامات واضحة</b><svg viewBox="0 0 520 26" class="uline"><path d="M6 12 L240 4 M40 20 L330 10 M300 18 L514 8" stroke="#d4a373" stroke-width="4" stroke-linecap="round" fill="none"/></svg></div>')

# ---- 2b. coarse / fine labels with pointer lines that follow the sheets (positions read from the footage) ----
def dots(n_cols, n_rows, r, w=120, h=64):
    return "".join(f'<circle cx="{8 + c * (w - 16) / max(1, n_cols - 1):.1f}" cy="{8 + rr * (h - 16) / max(1, n_rows - 1):.1f}" r="{r}"/>' for rr in range(n_rows) for c in range(n_cols))
sec("lab1", 13.15, 16.60, 4, f'''
<div class="chip" id="chip1" style="left:100px;top:262px;width:430px"><svg class="tex" viewBox="0 0 120 64" fill="#8c664a">{dots(4, 3, 7.5)}</svg><b>خشنة <span dir="ltr">120</span></b></div>
<div class="desc" id="desc1" style="left:100px;top:376px;width:430px"><svg viewBox="0 0 90 40"><path d="M10 30 L48 8 M30 34 L68 12 M50 36 L86 16" stroke="#fbf6ee" stroke-width="7" stroke-linecap="round"/></svg><span>تزيل الزوائد</span></div>
<svg class="full" viewBox="0 0 1080 1920"><line id="ln1" x1="315" y1="440" x2="335" y2="902" stroke="#fbf6ee" stroke-width="4" stroke-linecap="round"/><circle id="dot1" cx="335" cy="902" r="13" fill="none" stroke="#fbf6ee" stroke-width="5"/></svg>''')
sec("lab2", 15.85, 19.70, 5, f'''
<div class="chip" id="chip2" style="left:520px;top:262px;width:430px"><svg class="tex" viewBox="0 0 120 64" fill="#8c664a">{dots(10, 5, 2.7)}</svg><b>ناعمة <span dir="ltr">320</span></b></div>
<div class="desc" id="desc2" style="left:520px;top:376px;width:430px"><svg viewBox="0 0 90 40"><path d="M8 32 L30 18 M22 36 L44 22 M36 38 L58 24 M50 34 L72 20 M64 36 L86 22" stroke="#fbf6ee" stroke-width="3" stroke-linecap="round"/></svg><span>للتشطيب</span></div>
<svg class="full" viewBox="0 0 1080 1920"><line id="ln2" x1="735" y1="440" x2="810" y2="1152" stroke="#fbf6ee" stroke-width="4" stroke-linecap="round"/><circle id="dot2" cx="810" cy="1152" r="13" fill="none" stroke="#fbf6ee" stroke-width="5"/></svg>''')

# ---- 3a. the imperfection: a raised chip on the tray edge (camera is static there) ----
sec("edge", 20.80, 22.15, 6, '''
<svg class="full" viewBox="0 0 1080 1920"><circle id="ring" cx="594" cy="1047" r="46" fill="none" stroke="#fffaf0" stroke-width="5"/><circle id="ring2" cx="594" cy="1047" r="46" fill="none" stroke="#fffaf0" stroke-width="3" opacity="0.6"/>
<line id="ledge" x1="594" y1="1001" x2="594" y2="900" stroke="#fffaf0" stroke-width="4" stroke-linecap="round"/></svg>
<div class="chip" id="chipe" style="left:464px;top:790px;width:260px;padding:10px 20px"><b>العيب</b></div>''')

# ---- 3b. decision graphic ----
sec("decide", 23.15, 27.60, 7, '''
<div class="chip dec" id="dc1" style="left:600px;top:262px;width:340px"><b>نوع العيب</b></div>
<svg class="full" viewBox="0 0 1080 1920"><path id="dline" d="M596 312 H488" stroke="#3a2312" stroke-width="6" stroke-linecap="round" fill="none"/><path id="dhead" d="M506 292 L486 312 L506 332" stroke="#3a2312" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
<div class="chip dec" id="dc2" style="left:140px;top:262px;width:340px"><b>درجة الصنفرة</b></div>''')

# ---- 4. gradual finishing: grit ladder (coarse -> fine texture swatches) + step graphic ----
ladder = "".join(f'<div class="sw" id="sw{k}"><svg viewBox="0 0 120 64" fill="#8c664a">{dots(*cfg)}</svg></div>' for k, cfg in enumerate([(3, 2, 8.5), (5, 3, 5.5), (8, 4, 3.6), (12, 6, 2.2)]))
sec("steps", 28.70, 33.85, 8, f'''
<div class="ladder" id="lad">{ladder}</div>
<div class="chip step" id="st1" style="left:540px;top:262px;width:400px"><b>تشطيب تدريجي</b></div>
<svg class="full" viewBox="0 0 1080 1920"><path id="sarrow" d="M750 356 V420" stroke="#fbf6ee" stroke-width="6" stroke-linecap="round" fill="none"/><path id="shead" d="M730 404 L750 426 L770 404" stroke="#fbf6ee" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
<div class="chip step" id="st2" style="left:540px;top:436px;width:400px"><b>تنظيف الغبار</b></div>''')

# ---- 5. before / after + CTA ----
sec("ba", 33.90, DUR, 9, '''
<svg class="full" viewBox="0 0 1080 1920"><line id="bdiv" x1="550" y1="400" x2="550" y2="985" stroke="#fbf6ee" stroke-width="4" stroke-linecap="round" opacity="0.95"/><circle id="bnode" cx="550" cy="700" r="16" fill="#fbf6ee"/></svg>
<div class="chip tag" id="tb" style="left:110px;top:282px;width:330px"><b>قبل</b></div>
<div class="chip tag" id="ta" style="left:620px;top:282px;width:330px"><b>بعد</b></div>''')
sec("cta", 34.72, DUR, 10, '''
<div class="cta" id="ctat"><div class="ctab"><span class="cw">أرسليه</span> <span class="cw">لصاحبة</span> <span class="cw">مشروع</span></div></div>
<svg class="full" viewBox="0 0 1080 1920"><path id="share" d="M770 1010 C 830 960 880 930 905 870" stroke="#fbf6ee" stroke-width="6" stroke-linecap="round" fill="none"/><path id="shead2" d="M876 884 L905 862 L918 896" stroke="#fbf6ee" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>''')

sec("outro", 39.45, DUR, 30, PANEL.replace('class="pan"', 'class="pan" id="opan"'), "full")

css = face + """
*{box-sizing:border-box}html,body{margin:0;background:transparent}
#reel{position:relative;width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:ReelLatin,ReelArabic,sans-serif;font-weight:500;color:#2c1608;direction:rtl}
.full{position:absolute;left:0;top:0;width:1080px;height:1920px}
.vig{position:absolute;left:0;top:0;width:1080px;height:1920px;background:radial-gradient(ellipse at 50% 46%,rgba(0,0,0,0) 56%,rgba(32,16,6,.32) 100%)}
.chip.sc{left:240px;top:808px;width:300px;padding:4px 18px;height:104px;background:rgba(44,22,8,.92);border-color:#3a2312}.chip.sc b{color:#fbf6ee;font-size:50px}
.pan{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
.pw{position:absolute;left:0;top:0;width:1180px;height:1920px;transform:translateX(1180px);filter:drop-shadow(-18px 0 26px rgba(44,22,8,.34)) drop-shadow(18px 0 26px rgba(44,22,8,.34))}
.pw .bg{position:absolute;left:0;top:0;width:1180px;height:1920px;background:repeating-linear-gradient(112deg,rgba(140,102,74,.07) 0 2px,rgba(0,0,0,0) 2px 15px),radial-gradient(circle at 34% 38%,rgba(255,255,255,.62),rgba(255,255,255,0) 58%),linear-gradient(105deg,#f4eadb,#e9d7c0 58%,#dcc5a9)}
.pw .e1{position:absolute;left:-30px;top:0;width:12px;height:1920px;background:#b88a5e}.pw .e2{position:absolute;left:-70px;top:0;width:34px;height:1920px;background:#e8d4bb}
.pw .e3{position:absolute;right:-30px;top:0;width:12px;height:1920px;background:#b88a5e}.pw .e4{position:absolute;right:-70px;top:0;width:34px;height:1920px;background:#e8d4bb}
.pw .mk{position:absolute;left:410px;top:958px;width:360px;height:4px;background:#b88a5e;border-radius:2px;opacity:0;transform:scaleX(0)}
.pw .dt{position:absolute;left:581px;top:942px;width:36px;height:36px;border-radius:50%;background:#b88a5e;opacity:0;transform:scale(0)}
.fadeb{position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(to top,rgba(44,22,8,.38),rgba(44,22,8,0))}
.chip{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;padding:14px 26px;background:rgba(251,246,238,.96);border:1.5px solid #d3b6a1;border-radius:24px;box-shadow:0 14px 34px rgba(44,22,8,.30);visibility:hidden;opacity:0}
.chip b{font-size:60px;line-height:1.15;font-weight:800;color:#2c1608;white-space:nowrap}.chip b span{font-weight:800}
.chip.dark{background:rgba(44,22,8,.92);border-color:#3a2312;flex-direction:column;gap:2px}.chip.dark b{color:#fbf6ee;font-size:68px}
.chip.step{background:rgba(44,22,8,.90);border-color:#3a2312}.chip.step b{color:#fbf6ee;font-size:46px}.chip.dec b{font-size:48px}
.chip .tex{width:96px;height:52px;flex:none}.uline{width:480px;height:24px}
.chip.tag{background:rgba(251,246,238,.94)}.chip.tag b{font-size:64px}
.desc{position:absolute;display:flex;align-items:center;justify-content:center;gap:14px;visibility:hidden;opacity:0}
.desc span{font-size:48px;font-weight:700;color:#fbf6ee;text-shadow:0 2px 10px rgba(44,22,8,.6)}.desc svg{width:70px;height:32px;filter:drop-shadow(0 2px 6px rgba(44,22,8,.5))}
#ln1,#dot1,#ln2,#dot2,#ring,#ring2,#ledge,#bdiv,#bnode,#share,#shead2,#dline,#dhead,#sarrow,#shead,#brk{opacity:0}
.sweep{position:absolute;left:-460px;top:0;width:340px;height:1920px;background:linear-gradient(100deg,rgba(255,250,235,0),rgba(255,250,235,.50),rgba(255,250,235,0));transform:skewX(-14deg);opacity:0}
.hk{position:absolute;left:70px;top:236px;width:940px;height:520px;visibility:hidden}
.hk .brush{position:absolute;left:0;top:10px;width:940px;height:440px;clip-path:inset(0 0 0 100%)}
.hk .l1{position:absolute;left:0;right:0;top:62px;text-align:center;font-size:104px;font-weight:800;color:#2c1608;line-height:1.1}
.hk .l2{position:absolute;left:0;right:0;top:196px;text-align:center;font-size:136px;font-weight:800;color:#2c1608;line-height:1.1;white-space:nowrap}
.hk .l2 .st{color:#5b2a0e}.hk .w{display:inline-block}
.hk .scr{position:absolute;left:150px;top:352px;width:640px;height:40px;opacity:0}
.ladder{position:absolute;left:110px;top:262px;display:flex;gap:14px;direction:ltr}
.sw{width:96px;height:78px;background:rgba(251,246,238,.94);border:1.5px solid #d3b6a1;border-radius:16px;box-shadow:0 10px 24px rgba(44,22,8,.26);display:flex;align-items:center;justify-content:center;visibility:hidden;opacity:0}.sw svg{width:76px;height:42px}
.cta{position:absolute;left:80px;width:870px;top:1010px;text-align:center;visibility:hidden}
.ctab{display:inline-block;padding:24px 38px;background:rgba(44,22,8,.92);border-radius:28px;box-shadow:0 18px 44px rgba(44,22,8,.40);font-size:70px;font-weight:800;line-height:1.2;color:#fbf6ee;white-space:nowrap}.cw{display:inline-block;opacity:0}
.cap{position:absolute;left:70px;width:880px;bottom:420px;display:flex;justify-content:center;align-items:flex-end}
.cap p{margin:0;padding:12px 30px;background:rgba(44,22,8,.66);border-radius:20px;color:#fbf6ee;font-size:62px;line-height:1.42;font-weight:500;text-align:center;text-wrap:balance;max-width:880px;text-shadow:0 2px 8px rgba(0,0,0,.35);visibility:hidden;opacity:0}
.cap k{font-weight:800;color:#fff1de;position:relative;display:inline-block;font-style:normal;isolation:isolate}
.cap k .u{position:absolute;left:-10px;right:-10px;top:14%;bottom:4%;z-index:-1;background:rgba(176,118,66,.78);border-radius:14px;transform:scaleX(0);transform-origin:right center}
"""
js = """
const tl=gsap.timeline({paused:true});
const CAPS=__CAPS__;
const E='expo.out', I='power2.in';
// ---------- subtitles ----------
CAPS.forEach(c=>{
  const p='#cap'+c.i+' p';
  tl.set(p,{visibility:'visible'},c.a);
  tl.fromTo(p,{opacity:0,y:14,scale:.97,transformOrigin:'50% 100%'},{opacity:1,y:0,scale:1,duration:Math.min(.18,(c.b-c.a)/3),ease:E},c.a);
  document.querySelectorAll('#cap'+c.i+' k').forEach((k,j)=>{
    const t=c.k[j]||c.a, u=k.querySelector('.u');
    tl.fromTo(k,{scale:1},{scale:1.1,duration:.16,yoyo:true,repeat:1,ease:'power2.out',transformOrigin:'50% 60%'},t);
    tl.fromTo(u,{scaleX:0},{scaleX:1,duration:.38,ease:E},t);
  });
  tl.to(p,{opacity:0,duration:.07},c.b-.07);
  tl.set(p,{visibility:'hidden'},c.b);
});
// ---------- 1. hook ----------
tl.set('.hk',{visibility:'visible'},0.30);
tl.fromTo('.hk .brush',{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',duration:.42,ease:'power4.out'},0.30);
tl.fromTo('.hk .l1',{opacity:0,x:70,scale:.82},{opacity:1,x:0,scale:1,duration:.34,ease:'power4.out',transformOrigin:'50% 50%'},0.32);
tl.fromTo('.hk .w',{opacity:0,x:90,scale:.7},{opacity:1,x:0,scale:1,duration:.38,ease:'power4.out',stagger:.09,transformOrigin:'50% 50%'},0.40);
tl.fromTo('.hk .st',{scale:1},{scale:1.07,duration:.24,yoyo:true,repeat:1,ease:'power2.out',transformOrigin:'50% 60%'},0.92);
tl.fromTo('.hk .scr',{opacity:0,clipPath:'inset(0 0 0 100%)'},{opacity:1,clipPath:'inset(0 0 0 0%)',duration:.5,ease:'power2.out'},0.85);
tl.fromTo('.sweep',{x:0,opacity:1},{x:1700,opacity:1,duration:.85,ease:'power2.inOut'},0.52);
tl.set('.sweep',{opacity:0},1.4);
tl.set('#brk',{opacity:1},0.80); tl.fromTo('#brk',{strokeDasharray:300,strokeDashoffset:300},{strokeDashoffset:0,duration:.45,ease:'power2.out'},0.80);
tl.to('#brk',{opacity:0,duration:.4},2.6);
tl.to('.hk',{opacity:0,y:-26,duration:.34,ease:I},3.22); tl.set('.hk',{visibility:'hidden'},3.6);
tl.set('#brk',{opacity:1},6.45); tl.fromTo('#brk',{strokeDasharray:300,strokeDashoffset:300},{strokeDashoffset:0,duration:.45,ease:'power2.out'},6.45);
tl.to('#brk',{opacity:0,duration:.35},7.5);
// ---------- scratch rings: follow the scratches (positions tracked from the footage) ----------
const TRK=__TRK__, CUTS=__CUTS__;
function follow(g,keys,t0,t1,extra){
  const P=keys.filter(k=>k[0]>=t0-.6&&k[0]<=t1+.5); const first=P[0];
  tl.set(g,{x:first[1],y:first[2]},t0-.05);
  for(let i=1;i<P.length;i++){ tl.to(g,{x:P[i][1],y:P[i][2],duration:P[i][0]-P[i-1][0],ease:'none'},P[i-1][0]); }
  if(extra){ extra(P); }
}
function ringIn(g,t0,t1,r){
  tl.set(g,{opacity:1},t0);
  tl.fromTo(g+' .r1',{strokeDasharray:r*6.4,strokeDashoffset:r*6.4,rotation:-90,svgOrigin:'0 0'},{strokeDashoffset:0,duration:.55,ease:'power3.inOut'},t0);
  tl.fromTo(g+' .r2',{attr:{r:r},opacity:.7},{attr:{r:r*1.55},opacity:0,duration:.9,ease:'power1.out',repeat:2,repeatDelay:.25},t0+.45);
  tl.to(g,{opacity:0,duration:.35},t1);
}
[[0.78,3.2],[6.45,7.5]].forEach(([a,b])=>{
  ringIn('#rgA',a,b-.35,150); ringIn('#rgB',a+.22,b-.35,104);
});
follow('#rgA',TRK.A,0.78,7.5); follow('#rgB',TRK.B,0.78,7.5);
tl.set('#sctag',{visibility:'visible'},1.0);
tl.fromTo('#sctag',{opacity:0,y:18,scale:.88,transformOrigin:'50% 100%'},{opacity:1,y:0,scale:1,duration:.4,ease:'back.out(1.6)'},1.0);
tl.to('#sctag',{opacity:0,y:-8,duration:.3,ease:I},2.9); tl.set('#sctag',{visibility:'hidden'},3.25);
// ---------- luxury swipes over the three picture cuts + closing swipe ----------
function swipe(id,tc){
  const q=s=>'#'+id+' '+s;
  tl.fromTo(q('.pw'),{x:1180},{x:0,duration:.32,ease:'power3.inOut'},tc-.44);
  tl.fromTo(q('.mk'),{scaleX:0,opacity:1},{scaleX:1,duration:.26,ease:'expo.out'},tc-.14);
  tl.fromTo(q('.dt'),{scale:0,opacity:1},{scale:1,duration:.26,ease:'back.out(2.4)',transformOrigin:'50% 50%'},tc-.06);
  tl.to(q('.mk'),{opacity:0,duration:.14},tc+.10);
  tl.to(q('.dt'),{opacity:0,scale:.2,duration:.14},tc+.10);
  tl.to(q('.pw'),{x:-1180,duration:.36,ease:'power3.inOut'},tc+.12);
}
CUTS.forEach((tc,n)=>swipe('tr'+n,tc));
// closing: graphics drift away, the sand panel sweeps in and settles into a clean ivory card
tl.to(['#tb','#ta','#ctat','#bdiv','#bnode','#share','#shead2'],{opacity:0,y:-18,duration:.34,ease:I,stagger:.04},39.38);
tl.fromTo('#opan .pw',{x:1180},{x:0,duration:.5,ease:'power3.inOut'},39.58);
tl.fromTo('#opan .mk',{scaleX:0,opacity:1},{scaleX:1,duration:.5,ease:'expo.out'},40.0);
tl.fromTo('#opan .dt',{scale:0,opacity:1},{scale:1,duration:.3,ease:'back.out(2.4)',transformOrigin:'50% 50%'},40.12);
// ---------- 2a. risk ----------
tl.set('.chip.dark',{visibility:'visible'},11.15);
tl.fromTo('.chip.dark',{opacity:0,scale:.9,y:16,transformOrigin:'50% 50%'},{opacity:1,scale:1,y:0,duration:.36,ease:E},11.15);
tl.fromTo('.chip.dark .uline path',{strokeDasharray:260,strokeDashoffset:260},{strokeDashoffset:0,duration:.5,ease:'power2.out',stagger:.1},11.45);
tl.to('.chip.dark',{opacity:0,y:-10,duration:.28,ease:I},12.50); tl.set('.chip.dark',{visibility:'hidden'},12.8);
// ---------- 2b. coarse / fine ----------
function label(chip,desc,t0,t1){
  tl.set([chip,desc],{visibility:'visible'},t0);
  tl.fromTo(chip,{opacity:0,scale:.88,y:18,transformOrigin:'50% 50%'},{opacity:1,scale:1,y:0,duration:.38,ease:E},t0);
  tl.fromTo(desc,{opacity:0,x:30},{opacity:1,x:0,duration:.34,ease:E},t0+.16);
  tl.to([chip,desc],{opacity:0,y:-10,duration:.3,ease:I},t1-.3); tl.set([chip,desc],{visibility:'hidden'},t1);
}
function pointer(ln,dot,t0,t1,keys){
  tl.set([ln,dot],{opacity:1},t0);
  tl.fromTo(ln,{attr:{x2:+document.querySelector(ln).getAttribute('x1'),y2:+document.querySelector(ln).getAttribute('y1')}},{attr:{x2:keys[0][1],y2:keys[0][2]},duration:.4,ease:E},t0+.1);
  tl.fromTo(dot,{attr:{cx:+document.querySelector(ln).getAttribute('x1'),cy:+document.querySelector(ln).getAttribute('y1'),r:2}},{attr:{cx:keys[0][1],cy:keys[0][2],r:13},duration:.4,ease:E},t0+.1);
  for(let i=1;i<keys.length;i++){
    const a=keys[i-1], b=keys[i], d=Math.max(.2,b[0]-a[0]);
    tl.to(ln,{attr:{x2:b[1],y2:b[2]},duration:d,ease:'sine.inOut'},a[0]+.5>t0+.5?a[0]:t0+.5);
    tl.to(dot,{attr:{cx:b[1],cy:b[2]},duration:d,ease:'sine.inOut'},a[0]+.5>t0+.5?a[0]:t0+.5);
  }
  tl.to([ln,dot],{opacity:0,duration:.3},t1-.3);
}
label('#chip1','#desc1',13.15,16.60);
pointer('#ln1','#dot1',13.15,16.60,[[13.2,335,902],[13.5,378,864],[14.0,389,902],[14.5,324,1152],[15.0,281,1210],[16.4,302,1210]]);
label('#chip2','#desc2',15.85,19.70);
pointer('#ln2','#dot2',15.85,19.70,[[15.9,810,1152],[16.1,788,1056],[16.6,648,1075],[17.1,648,1114],[17.6,562,1190],[18.6,562,1190],[19.1,842,1190],[19.5,860,1170]]);
// ---------- 3a. imperfection ring ----------
tl.set(['#ring','#ring2','#ledge'],{opacity:1},20.80);
tl.fromTo('#ring',{attr:{r:90},opacity:0},{attr:{r:46},opacity:1,duration:.45,ease:E},20.80);
tl.fromTo('#ring2',{attr:{r:46},opacity:.6},{attr:{r:82},opacity:0,duration:.8,ease:'power1.out',repeat:1},20.95);
tl.fromTo('#ledge',{strokeDasharray:110,strokeDashoffset:110,opacity:1},{strokeDashoffset:0,duration:.35,ease:'power2.out'},21.0);
tl.set('#chipe',{visibility:'visible'},21.0);
tl.fromTo('#chipe',{opacity:0,y:14,scale:.9,transformOrigin:'50% 100%'},{opacity:1,y:0,scale:1,duration:.34,ease:E},21.0);
tl.to(['#ring','#ring2','#ledge','#chipe'],{opacity:0,duration:.28},21.85); tl.set('#chipe',{visibility:'hidden'},22.15);
// ---------- 3b. decision graphic ----------
tl.set(['#dc1','#dc2'],{visibility:'visible'},23.15);
tl.fromTo('#dc1',{opacity:0,x:50,scale:.92,transformOrigin:'50% 50%'},{opacity:1,x:0,scale:1,duration:.4,ease:E},23.15);
tl.set('#dline',{opacity:1},23.5); tl.fromTo('#dline',{strokeDasharray:130,strokeDashoffset:130},{strokeDashoffset:0,duration:.5,ease:'power2.inOut'},23.5);
tl.set('#dhead',{opacity:1},23.95); tl.fromTo('#dhead',{scale:.4,transformOrigin:'486px 312px'},{scale:1,duration:.2,ease:'back.out(2)'},23.95);
tl.fromTo('#dc2',{opacity:0,x:-50,scale:.92,transformOrigin:'50% 50%'},{opacity:1,x:0,scale:1,duration:.4,ease:E},23.95);
tl.fromTo('#dc2',{scale:1},{scale:1.05,duration:.18,yoyo:true,repeat:1,ease:'power2.out',transformOrigin:'50% 50%'},24.5);
tl.to(['#dc1','#dc2','#dline','#dhead'],{opacity:0,y:-10,duration:.3,ease:I},27.25); tl.set(['#dc1','#dc2'],{visibility:'hidden'},27.6);
// ---------- 4. gradual finishing ----------
tl.set('.sw',{visibility:'visible'},28.70);
tl.fromTo('.sw',{opacity:0,y:20,scale:.85,transformOrigin:'50% 50%'},{opacity:1,y:0,scale:1,duration:.34,ease:E,stagger:.55},28.78);
tl.set('#st1',{visibility:'visible'},29.05);
tl.fromTo('#st1',{opacity:0,y:20,scale:.92,transformOrigin:'50% 50%'},{opacity:1,y:0,scale:1,duration:.4,ease:E},29.05);
tl.set(['#sarrow','#shead'],{opacity:1},31.95);
tl.fromTo('#sarrow',{strokeDasharray:70,strokeDashoffset:70},{strokeDashoffset:0,duration:.35,ease:'power2.out'},31.95);
tl.fromTo('#shead',{opacity:0,y:-10},{opacity:1,y:0,duration:.2},32.25);
tl.set('#st2',{visibility:'visible'},32.10);
tl.fromTo('#st2',{opacity:0,y:20,scale:.92,transformOrigin:'50% 50%'},{opacity:1,y:0,scale:1,duration:.4,ease:E},32.35);
tl.to(['#st1','#st2','#sarrow','#shead','.sw'],{opacity:0,y:-10,duration:.3,ease:I},33.50); tl.set(['#st1','#st2','.sw'],{visibility:'hidden'},33.85);
// ---------- 5. before / after + CTA ----------
tl.set(['#bdiv','#bnode'],{opacity:1},33.95);
tl.fromTo('#bdiv',{strokeDasharray:600,strokeDashoffset:600},{strokeDashoffset:0,duration:.7,ease:'power2.inOut'},33.95);
tl.fromTo('#bnode',{scale:0,transformOrigin:'550px 700px'},{scale:1,duration:.3,ease:'back.out(2)'},34.5);
tl.set('#tb',{visibility:'visible'},34.15); tl.fromTo('#tb',{opacity:0,x:-40,scale:.92,transformOrigin:'50% 50%'},{opacity:1,x:0,scale:1,duration:.4,ease:E},34.15);
tl.set('#ta',{visibility:'visible'},34.45); tl.fromTo('#ta',{opacity:0,x:40,scale:.92,transformOrigin:'50% 50%'},{opacity:1,x:0,scale:1,duration:.4,ease:E},34.45);
tl.set('#ctat',{visibility:'visible'},34.72);
tl.fromTo('.cw',{opacity:0,y:50,scale:.8,transformOrigin:'50% 100%'},{opacity:1,y:0,scale:1,duration:.42,ease:'power4.out',stagger:.16},34.80);
tl.set(['#share','#shead2'],{opacity:1},35.55);
tl.fromTo('#share',{strokeDasharray:200,strokeDashoffset:200},{strokeDashoffset:0,duration:.6,ease:'power2.inOut'},35.55);
tl.fromTo('#shead2',{opacity:0,scale:.5,transformOrigin:'905px 862px'},{opacity:1,scale:1,duration:.22,ease:'back.out(2)'},36.1);
tl.fromTo('.ctab',{scale:1},{scale:1.035,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',transformOrigin:'50% 50%'},36.4);
window.__timelines=window.__timelines||{}; window.__timelines.reel=tl;
"""
js = js.replace("__CAPS__", json.dumps(caps_js)).replace("__TRK__", TRACK_JS).replace("__CUTS__", json.dumps(CUTS))
doc = f'''<!doctype html><html lang="ar"><head><meta charset="utf-8"><title>ANTIQUE sandpaper reel overlay</title><script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><main id="reel" data-composition-id="reel" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="30"><div class="fadeb"></div><div class="vig"></div>
{''.join(els)}</main><script>{js}</script></body></html>'''
(OUT / "index.html").write_text(doc, encoding="utf-8"); (OUT / "hyperframes.json").write_text(json.dumps({"name": "antique-sandpaper-reel-overlay"}))
print("overlay written:", len(els), "sections,", len(CAPS), "captions")
