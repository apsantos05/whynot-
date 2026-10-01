import numpy as np, subprocess, os, sys, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(D)
VD = os.path.join(D, sys.argv[1] if len(sys.argv) > 1 else "C")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(S, "whynot-anuncio-narrado.mp4")
W, H, FPS, SR = 1080, 1920, 30, 44100
FD = os.path.join(S, "fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/")
BLACK = FD + "Fraunces144pt-Black.ttf"; ITA = FD + "Fraunces72pt-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
ICE = (228, 242, 246); MUTED = (157, 188, 196)
EXT = [(179,207,214),(155,189,198),(133,171,181),(113,153,164),(95,135,146),(79,117,128),(65,100,110),(53,83,92),(42,67,75),(32,52,58),(23,38,43),(15,25,29)]

def txt(t, size, fill=ICE, font=MONO, track=0):
    f = ImageFont.truetype(font, size); bb = f.getbbox(t)
    w = bb[2]-bb[0] + track*len(t) + 20; h = bb[3]-bb[1] + 40
    im = Image.new("RGBA", (int(w), int(h)), (0,0,0,0)); d = ImageDraw.Draw(im); x = 10
    for ch in t: d.text((x-bb[0], 20-bb[1]), ch, font=f, fill=fill+(255,)); x += f.getlength(ch) + track
    return im
_ec = {}
def ext(t, size, layers=12, step=3, rot=8):
    k = (t, size, layers)
    if k in _ec: return _ec[k]
    f = ImageFont.truetype(BLACK, size); bb = f.getbbox(t); pad = step*12+30
    im = Image.new("RGBA", (bb[2]-bb[0]+pad*2, bb[3]-bb[1]+pad*2), (0,0,0,0)); d = ImageDraw.Draw(im)
    ox, oy = pad-bb[0], pad-bb[1]
    for j in range(int(layers), 0, -1): d.text((ox-j*step, oy+j*step), t, font=f, fill=EXT[j-1]+(255,))
    d.text((ox, oy), t, font=f, fill=ICE+(255,))
    _ec[k] = im.rotate(rot, resample=Image.BICUBIC, expand=True); return _ec[k]
def put(cv, im, cx, cy, a=1.0, sc=1.0):
    if a <= 0.01: return
    if sc != 1.0: im = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.BICUBIC)
    if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v*a)))
    cv.alpha_composite(im, (int(cx-im.width/2), int(cy-im.height/2)))
cl = lambda x: max(0.0, min(1.0, x))
ease = lambda t: 1-(1-cl(t))**3
def grow(t): return int(min(12, cl(t/0.45)*12))
def fade(t, t0, t1, fi=0.25, fo=0.25): return cl((t-t0)/fi) * cl((t1-t)/fo)

# ---------- voz e linha do tempo ----------
def wav(p):
    w = wave.open(p); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
    n = int(len(x)*SR/sr); return np.interp(np.linspace(0, len(x)-1, n), np.arange(len(x)), x)
L = [wav(os.path.join(VD, f"{i:02d}.wav")) for i in range(1, 15)]
dur = [len(x)/SR for x in L]
gaps = [0.35, 0.45, 0.35, 0.25, 0.55, 0.22, 0.22, 0.22, 0.22, 0.22, 0.45, 0.35, 0.55, 0.30]
st = []; t = 0
for i in range(14): t += gaps[i]; st.append(t); t += dur[i]
TOTAL = st[13] + dur[13] + 1.6
en = [st[i]+dur[i] for i in range(14)]
# cenas: A(0) B(1) C(2,3) D(4..9) E(10,11) F(12,13)
SC = [0, st[1]-0.2, st[2]-0.2, st[4]-0.15, st[10]-0.2, st[12]-0.2, TOTAL]

# ---------- assets ----------
yy, xx = np.mgrid[0:H, 0:W]
r = np.clip(np.sqrt((xx-W/2)**2 + ((yy-H*0.5)*0.75)**2)/(W*0.95), 0, 1)
BG = (np.array([14,26,28])[None,None]*(1-r[...,None]) + np.array([6,10,12])[None,None]*r[...,None]).astype(np.float32)
bgim = Image.fromarray(BG.astype(np.uint8)).convert("RGBA")
rng = np.random.default_rng(7)
GR = [rng.normal(0, 6, (H, W, 1)).astype(np.float32) for _ in range(6)]
top_l = txt("WHY NOT? · EDIÇÃO 01", 30, MUTED, track=6); top_r = txt("09.10", 30, MUTED, track=6)
bot_l = txt("BALLY CLUB", 28, MUTED, track=6); bot_r = txt("SÃO JOSÉ DO RIO PRETO", 28, MUTED, track=4)
DJ = [("coiote","Coiote","@DJCOIOTE"),("maka","Maka","@MAKAADJ"),("tom","Tom Keller","@TOMKELLERMUSIC"),
      ("maycon","Maycon Beats","@MAYCON_BEATS"),("mex","Mexikanno","@MEXSYMUSIC"),("possani","Possani","@_POSSANI04")]
PH = {}
for k, n, h in DJ:
    im = Image.open(os.path.join(S, f"lineup/{'y_' if k=='tom' else 'z_'}{k}.png")).convert("RGBA")
    s = 1150/im.height if im.width/im.height < 0.95 else 1000/im.width
    s = min(s, 1060/im.width)
    PH[k] = im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
logo = Image.open(os.path.join(S, "wn/logo.png")).convert("RGB")

def frame(t):
    cv = bgim.copy()
    a_hdr = cl(t/0.4) * cl((TOTAL-t)/0.4)
    put(cv, top_l, 70+top_l.width/2, 110, a_hdr*0.9); put(cv, top_r, W-70-top_r.width/2, 110, a_hdr*0.9)
    if t < SC[1]:                                   # A
        a = fade(t, 0.1, SC[1])
        put(cv, txt("nem toda noite", 92, ICE, ITA), W/2, 800, a*ease((t-st[0]+0.1)/0.4))
        put(cv, ext("é igual.", 230, grow(t-st[0]-0.55)), W/2, 1010, a*ease((t-st[0]-0.5)/0.3))
    elif t < SC[2]:                                 # B
        tt = t-SC[1]; a = fade(t, SC[1], SC[2], 0.2)
        put(cv, txt("sexta-feira", 96, ICE, ITA), W/2, 700, a*ease(tt/0.4))
        put(cv, ext("09.10", 330, grow(tt-0.6)), W/2, 960, a*ease((tt-0.55)/0.3), 1+0.03*cl(tt/3))
        put(cv, txt("OUTUBRO · 22H", 40, MUTED, track=10), W/2, 1240, a*ease((tt-1.1)/0.4))
    elif t < SC[3]:                                 # C
        tt = t-SC[2]; a = fade(t, SC[2], SC[3], 0.2)
        put(cv, txt("ONDE", 32, MUTED, track=10), W/2, 600, a*ease(tt/0.3))
        put(cv, ext("Bally Club.", 170, grow(tt-0.1)), W/2, 760, a*ease(tt/0.3))
        t4 = t-st[3]
        put(cv, ext("6 DJs.", 250, grow(t4)), W/2, 1060, a*ease(t4/0.3))
        put(cv, txt("uma noite só.", 92, ICE, ITA), W/2, 1300, a*ease((t-st[3]-1.2)/0.4))
    elif t < SC[4]:                                 # D
        i = 5
        for j in range(6):
            if t < (st[5+j] - 0.12 if j < 5 else 1e9): i = j; break
        t0 = SC[3] if i == 0 else st[4+i]-0.12; t1 = st[5+i]-0.12 if i < 5 else SC[4]
        tt = t-t0; a = cl(tt/0.12) * cl((t1-t)/0.12) if i < 5 else cl(tt/0.12)*cl((SC[4]-t)/0.2)
        k, n, h = DJ[i]; ph = PH[k]
        sc = 1.0 + 0.04*cl(tt/1.0)
        put(cv, ph, W/2, 1680-ph.height*sc/2, a, sc)
        fs = 200 if len(n) <= 7 else 150
        put(cv, ext(n, fs, grow(tt*1.6)), W/2, 1420, a)
        put(cv, txt(h, 36, ICE, track=6), W/2, 1610, a)
        put(cv, txt(f"0{i+1} / 06", 30, MUTED, track=6), W/2, 300, a*0.8)
        put(cv, txt("LINE-UP", 30, MUTED, track=10), W/2, 345, a*0.8)
    elif t < SC[5]:                                 # E
        tt = t-SC[4]; a = fade(t, SC[4], SC[5], 0.2)
        put(cv, ext("open gin.", 230, grow(tt)), W/2, 820, a*ease(tt/0.3))
        put(cv, txt("22H — 23H", 84, ICE, MONOB, track=10), W/2, 1060, a*ease((tt-0.8)/0.3))
        put(cv, txt("chega cedo.", 96, ICE, ITA), W/2, 1260, a*ease((t-st[11]+0.05)/0.35))
    else:                                           # F
        tt = t-SC[5]; a = cl(tt/0.2) * cl((TOTAL-t)/0.5)
        put(cv, txt("garante o seu", 86, ICE, ITA), W/2, 620, a*ease(tt/0.35))
        put(cv, ext("antecipado.", 170, grow(tt-0.3)), W/2, 790, a*ease((tt-0.25)/0.3))
        put(cv, txt("INGRESSOS NA BIO →", 44, ICE, MONOB, track=8), W/2, 1010, a*ease((t-st[12]-1.9)/0.3))
        t14 = t-st[13]
        put(cv, ext("why not?", 240, grow(t14)), W/2, 1330, a*ease(t14/0.25), 1.12-0.12*ease(t14/0.3))
    put(cv, bot_l, 70+bot_l.width/2, H-110, a_hdr*0.8); put(cv, bot_r, W-70-bot_r.width/2, H-110, a_hdr*0.8)
    arr = np.asarray(cv.convert("RGB")).astype(np.float32) + GR[int(t*FPS) % 6]
    return np.clip(arr, 0, 255).astype(np.uint8)

# ---------- áudio: voz tratada + trilha ambiente original ----------
def build_audio():
    n = int(TOTAL*SR); v = np.zeros(n, np.float32)
    for i in range(14):
        s = int(st[i]*SR); v[s:s+len(L[i])] += L[i][:n-s]
    tm = np.arange(n)/SR; bpm = 122; beat = 60/bpm
    m = np.zeros(n, np.float32)
    # kick suave
    kl = int(0.35*SR); kt = np.arange(kl)/SR
    kick = np.sin(2*np.pi*(45*kt + 55*(1-np.exp(-kt*28))/28*1.0)) * np.exp(-kt*9)
    k0 = 0.0
    b = SC[1]
    while b < TOTAL-1.2:
        s = int(b*SR); e = min(n, s+kl); m[s:e] += 0.55*kick[:e-s]; b += beat
    # hi-hat abafado no contratempo
    hl = int(0.05*SR); hat = rng.normal(0, 1, hl).astype(np.float32)*np.exp(-np.arange(hl)/SR*80)
    hat = np.diff(np.concatenate([[0], hat]))
    b = SC[1] + beat/2
    while b < TOTAL-1.2:
        s = int(b*SR); e = min(n, s+hl); m[s:e] += 0.10*hat[:e-s]; b += beat
    # pad escuro (Lá menor), entrando aos poucos
    pad = sum(np.sin(2*np.pi*f*tm + 0.3*np.sin(2*np.pi*0.2*tm*(j+1))) for j, f in enumerate([55, 110, 130.81, 164.81, 220]))
    pad *= 0.06 * np.clip(tm/2.0, 0, 1)
    m += pad.astype(np.float32)
    m *= np.clip((TOTAL-tm)/1.5, 0, 1)
    np.save(os.path.join(D, "v.npy"), v); np.save(os.path.join(D, "m.npy"), m)
    for name, arr in (("v.wav", v), ("m.wav", m)):
        w = wave.open(os.path.join(D, name), "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(arr, -1, 1)*32767).astype(np.int16).tobytes()); w.close()
    # voz: um pouco mais grave, compressão, eco curto de clube; trilha abaixa quando a voz entra
    fc = ("[0:a]highpass=f=60,equalizer=f=180:t=q:w=1:g=2,equalizer=f=4000:t=q:w=1.5:g=1.5,"
          "acompressor=threshold=-22dB:ratio=2.5:attack=5:release=150,volume=1.5,asplit=2[vo][sc];"
          "[1:a]lowpass=f=6000,volume=0.9[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
          "[vo][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,aformat=channel_layouts=stereo[a]")
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-i",os.path.join(D,"v.wav"),"-i",os.path.join(D,"m.wav"),
                    "-filter_complex",fc,"-map","[a]","-ar","44100",os.path.join(D,"mix.wav")], check=True)

if __name__ == "__main__":
    build_audio()
    if "--audio" in sys.argv: sys.exit()
    if "--frames" in sys.argv:
        for tt in [1.2, 3.5, 7.5, st[4]+0.4, st[7]+0.3, st[9]+0.3, st[11]+0.3, st[12]+2.4, st[13]+0.8]:
            Image.fromarray(frame(tt)).save(os.path.join(D, f"fr_{tt:.1f}.png"))
        print("TOTAL", round(TOTAL, 2)); sys.exit()
    p = subprocess.Popen(["ffmpeg","-nostdin","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-i",os.path.join(D,"mix.wav"),"-c:v","libx264","-pix_fmt","yuv420p","-b:v","8M","-maxrate","10M","-bufsize","16M",
        "-preset","slow","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",OUT], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(int(TOTAL*FPS)): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", OUT, round(TOTAL, 2))
