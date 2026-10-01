import numpy as np, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(D, "pos")
W, H, FPS = 1080, 1920, 30
FD = os.path.join(D, "fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/")
BLACK = FD + "Fraunces144pt-Black.ttf"; ITA = FD + "Fraunces72pt-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
ICE = (228, 242, 246); MUTED = (157, 188, 196)
EXT = [(179,207,214),(155,189,198),(133,171,181),(113,153,164),(95,135,146),(79,117,128),(65,100,110),(53,83,92),(42,67,75),(32,52,58),(23,38,43),(15,25,29)]
BAND_Y, BAND_H = 400, 1100
rng = np.random.default_rng(3)

SRC = os.path.join(T, "video.mp4")
TAKES = [(2.4,None),(7.0,None),(16.0,(270,480,20,150)),(31.1,None),(33.2,None)]
SEG = 1.2
def load_take(start, crop, n):
    raw = subprocess.run(["ffmpeg","-loglevel","error","-ss",str(start),"-i",SRC,"-t",str(SEG+0.1),
        "-vf",(f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else "")+f"scale={W}:{H},fps={FPS},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    fr = np.frombuffer(raw,np.uint8).reshape(-1,H,W)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n-len(fr), 0)])
    fr = fr[:n].astype(np.float32); lo, hi = np.percentile(fr, 1.5), np.percentile(fr, 99.2)
    return np.clip((fr - lo) / max(1, hi - lo) * 255, 0, 255).astype(np.uint8)

def grade(g):
    g = g.astype(np.float32) / 255.0
    g = np.clip((g - 0.5) * 1.25 + 0.52, 0, 1) ** 1.05
    lo = np.array([6, 10, 12], np.float32); hi = np.array(ICE, np.float32)
    return lo + g[..., None] * (hi - lo)

def txt(t, f, fill, track=0):
    bb = f.getbbox(t); w = bb[2]-bb[0] + track*len(t) + 20; h = bb[3]-bb[1] + 40
    im = Image.new("RGBA", (int(w), int(h)), (0,0,0,0)); d = ImageDraw.Draw(im); x = 10
    for ch in t: d.text((x-bb[0], 20-bb[1]), ch, font=f, fill=fill); x += f.getlength(ch) + track
    return im
def ext(t, size, layers=12, step=3, rot=8):
    f = ImageFont.truetype(BLACK, size); bb = f.getbbox(t); pad = step*12+30
    im = Image.new("RGBA", (bb[2]-bb[0]+pad*2, bb[3]-bb[1]+pad*2), (0,0,0,0)); d = ImageDraw.Draw(im)
    ox, oy = pad-bb[0], pad-bb[1]
    for k in range(int(layers), 0, -1): d.text((ox-k*step, oy+k*step), t, font=f, fill=EXT[k-1]+(255,))
    d.text((ox, oy), t, font=f, fill=ICE+(255,))
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)
def put(cv, im, cx, cy, a=1.0):
    if a <= 0: return
    if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v*a)))
    cv.alpha_composite(im, (int(cx-im.width/2), int(cy-im.height/2)))
ease = lambda t: 1-(1-max(0,min(1,t)))**3

yy, xx = np.mgrid[0:H, 0:W]
r = np.clip(np.sqrt((xx-W/2)**2 + ((yy-H*0.5)*0.75)**2)/(W*0.9), 0, 1)
BG = (np.array([16,32,31])[None,None]*(1-r[...,None]) + np.array([6,10,12])[None,None]*r[...,None]).astype(np.float32)

lab_top = txt("WHY NOT? APRESENTA", ImageFont.truetype(MONO, 36), MUTED+(255,), 8)
num = {k: ext("line-up.", 220, layers=k) for k in range(13)}
hdr = txt("LINE-UP · WHY NOT?", ImageFont.truetype(MONO, 34), ICE+(255,), 6)
hdr2 = txt("09.10", ImageFont.truetype(MONO, 34), ICE+(255,), 6)
name_small = txt("POSSANI", ImageFont.truetype(MONOB, 52), ICE+(255,), 10)
cred = txt("@_POSSANI04", ImageFont.truetype(MONO, 36), MUTED+(255,), 8)
cover = np.asarray(Image.open(os.path.join(D, "r17s/DJ04Capa.png")).convert("RGB")).astype(np.float32)

yv = np.linspace(0,1,H)[:,None,None]
SHADE = np.clip(1 - 0.92*np.clip((0.30-yv)/0.30,0,1)**0.9 - 0.8*np.clip((yv-0.72)/0.28,0,1)**1.1, 0, 1)
INTRO, TK, END = 1.2, SEG*len(TAKES), 10 - 1.2 - SEG*len(TAKES)
seg_n = int(SEG*FPS)
takes = [load_take(st, cr, seg_n) for st, cr in TAKES]
N = FPS*10
out = os.path.join(D, "whynot-dj04-possani.mp4")
p = subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-f","lavfi","-t","10","-i","anullsrc=r=44100:cl=stereo","-c:v","libx264","-pix_fmt","yuv420p","-b:v","12M",
    "-maxrate","14M","-bufsize","20M","-preset","slow","-movflags","+faststart","-c:a","aac","-shortest",out],
    stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
for i in range(N):
    t = i/FPS
    if t < INTRO:
        cv = Image.fromarray(BG.astype(np.uint8)).convert("RGBA")
        put(cv, lab_top, W/2, 720, ease(t/0.4))
        put(cv, num[int(min(12, t/0.6*12))], W/2, 960, ease((t-0.1)/0.3))
        arr = np.asarray(cv.convert("RGB")).astype(np.float32)
    elif t < INTRO + TK:
        tt = t - INTRO; k = min(int(tt // SEG), len(TAKES)-1); fi = min(int((tt - k*SEG)*FPS), seg_n-1)
        band = grade(takes[k][fi])
        z = 1 + 0.05 * ((tt - k*SEG)/SEG)
        bi = Image.fromarray(band.astype(np.uint8)); bw, bh = int(W*z), int(H*z)
        bi = bi.resize((bw, bh), Image.BILINEAR).crop(((bw-W)//2, (bh-H)//2, (bw-W)//2+W, (bh-H)//2+H))
        arr = np.asarray(bi).astype(np.float32) * SHADE
        cv = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
        put(cv, hdr, 80 + hdr.width/2, 320); put(cv, hdr2, W - 80 - hdr2.width/2, 320)
        put(cv, name_small, W/2, 1610, ease((tt-0.2)/0.4)); put(cv, cred, W/2, 1690, ease((tt-0.5)/0.4))
        arr = np.asarray(cv.convert("RGB")).astype(np.float32)
        ph = tt - k*SEG
        if ph < 0.08 and k > 0: arr = arr*0.3 + np.array(ICE, np.float32)*0.7   # flash on cut
    else:
        et = t - INTRO - TK
        arr = cover.copy()
        if et < 0.12: arr = arr*0.4 + 255*0.6
    g = rng.normal(0, 8, (H//2, W//2)).astype(np.float32)
    arr = np.clip(arr + np.repeat(np.repeat(g,2,0),2,1)[...,None], 0, 255)
    if t > 9.85: arr *= max(0, (10-t)/0.15)
    p.stdin.write(arr.astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print("ok", os.path.getsize(out))
