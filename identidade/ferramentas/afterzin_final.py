"""afterzin why not? — arte FINAL com a line-up confirmada (Paganotti + Marquez, Kaio Alves, Possani, Mexikanno, Polão).
Paleta Grafite. Fotos tiradas do cartaz da Bally (fundo verde removido por cor), em P&B.
Gera feed 4:5 + story (2x) em afterzin-2011/final/ e o JPG do site em ../assets/after/.
Renderiza com o Chrome/Edge em modo headless (não precisa de Playwright).
Uso: python afterzin_final.py"""
import os, io, base64, random, subprocess, tempfile, shutil
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter, ImageDraw

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = R + '/afterzin-2011'; OUT = A + '/final'; os.makedirs(OUT, exist_ok=True)
SITE = os.path.dirname(R) + '/assets/after'; os.makedirs(SITE, exist_ok=True)
SRC = A + '/fotos/bally_2011_lineup_original.webp'
POLAO = A + '/fotos/polao_original.webp'
WN = R + '/assets/logo/grafite/logo-why-not-grafite.png'
AZ = A + '/assets/wordmark-afterzin-grafite.png'
BALLY = A + '/assets/bally_logo_grafite.png'
BASE, DEST, MED, LINE = '#08090a', '#ececec', '#a9adb1', '#2c2f33'

HEADLINER = 'Paganotti'
LINEUP = ['Marquez', 'Kaio Alves', 'Possani', 'Mexikanno', 'Polão']
QUANDO = 'SEXTA PRA SÁBADO · 21.11 · 01H'
FRASE = "o show acaba à meia-noite. <span style='color:%s'>a noite, não.</span>" % MED
INGRESSOS = 'INGRESSOS NO SITE DA BALLY OU NA PORTARIA'

BROWSER = next(p for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                           r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'] if os.path.exists(p))
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

# ---------- fotos: recorte do grupo tirando o fundo verde-água ----------
def grupo():
    im = Image.open(SRC).convert('RGB').crop((0, 290, 1080, 900))   # cabeças → peito, acima do logo "Paganotti"
    H, S, V = [np.array(c).astype(int) for c in im.convert('HSV').split()]
    teal = (H > 100) & (H < 150) & (S > 55) & (V > 30)
    c = Image.fromarray((teal * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    W, Hh = c.size
    for x in range(0, W, 8):                      # fundo = verde ligado às bordas
        for y in (0, Hh - 1):
            if c.getpixel((x, y)) == 255: ImageDraw.floodfill(c, (x, y), 128)
    for y in range(0, Hh, 8):
        for x in (0, W - 1):
            if c.getpixel((x, y)) == 255: ImageDraw.floodfill(c, (x, y), 128)
    a = np.array(c)
    fg = (a != 128) & ~((H > 110) & (H < 140) & (S > 90) & (V > 90))   # buracos verdes entre dedos/cabelo
    m = Image.fromarray((fg * 255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
    # sai a dupla Duha (cartaz da Bally), entra o Polão no mesmo lugar
    duo = Image.new('L', im.size, 0)
    ImageDraw.Draw(duo).polygon([(535, 610), (540, 470), (565, 390), (605, 362), (645, 372), (655, 420), (700, 425), (720, 400),
                                 (770, 400), (805, 430), (815, 480), (840, 520), (845, 610)], fill=255)
    m = ImageChops.subtract(m, duo.filter(ImageFilter.GaussianBlur(3)))
    pl = Image.open(POLAO).convert('RGB')
    pm = Image.new('L', pl.size, 0)
    ImageDraw.Draw(pm).polygon([(235, 330), (290, 305), (330, 312), (380, 300), (430, 290), (480, 298), (510, 315), (532, 360), (536, 440),
                                (520, 505), (490, 535), (465, 548), (455, 562), (456, 620), (448, 690), (432, 745), (405, 790), (385, 830),
                                (370, 923), (115, 923), (80, 820), (62, 700), (68, 560), (100, 475), (160, 400), (205, 380)], fill=255)
    # tira o halo da parede clara perto da borda do recorte
    Hp, Sp, Vp = [np.array(c).astype(int) for c in pl.convert('HSV').split()]
    borda = np.array(pm) > np.array(pm.filter(ImageFilter.MinFilter(21)))
    parede = borda & (Vp > 185) & (Sp < 45)
    pm = Image.fromarray(np.where(parede, 0, np.array(pm)).astype('uint8')).filter(ImageFilter.GaussianBlur(1.6))
    k = 0.45; x0, y0 = round(690 - 380 * k), round(335 - 290 * k)
    pl = pl.resize((round(pl.width * k), round(pl.height * k)), Image.LANCZOS); pm = pm.resize(pl.size, Image.LANCZOS)
    pl = ImageEnhance.Contrast(ImageEnhance.Brightness(pl).enhance(1.18)).enhance(1.3)   # aproxima do contraste das outras fotos
    im.paste(pl, (x0, y0), pm)
    lay = Image.new('L', im.size, 0); lay.paste(pm, (x0, y0))
    # P&B grafite
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.15)
    lo, hi = (8, 9, 10), (236, 236, 236)
    rgb = Image.merge('RGB', [g.point(lambda v, l=lo[i], h=hi[i]: round(l + (h - l) * v / 255)) for i in range(3)])
    # some embaixo e nas laterais
    fb = Image.linear_gradient('L').resize((W, Hh)).point(lambda v: 255 if v < 150 else max(0, 255 - (v - 150) * 2.4))
    side = Image.linear_gradient('L').rotate(90, expand=True).resize((W, Hh))
    side = ImageChops.multiply(side.point(lambda v: min(255, v * 9)), ImageOps.mirror(side).point(lambda v: min(255, v * 9)))
    a = ImageChops.multiply(ImageChops.multiply(m, fb), side)
    # o Polão some mais embaixo que o resto, pra o rosto não ficar apagado
    fp = Image.linear_gradient('L').resize((W, Hh)).point(lambda v: 255 if v < 205 else max(0, 255 - (v - 205) * 5))
    a = ImageChops.lighter(a, ImageChops.multiply(lay, fp))
    rgb.putalpha(a)
    buf = io.BytesIO(); rgb.save(buf, 'PNG'); return base64.b64encode(buf.getvalue()).decode(), rgb.size

FOTO, (FW, FH) = grupo()

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,900;1,9..144,400&family=Space+Mono:wght@700&display=block');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{BASE};overflow:hidden}}
body{{position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fraunces;font-style:italic;font-weight:400;color:{DEST}}}
.sm{{font-family:'Space Mono';font-weight:700;color:{MED};letter-spacing:.3em;text-indent:.3em}}
.nm{{font-family:Fraunces;font-weight:900;font-variation-settings:'opsz' 144;color:{DEST};letter-spacing:-.01em}}
.hl{{font-family:Fraunces;font-weight:900;font-variation-settings:'opsz' 144;color:{DEST};letter-spacing:-.03em;line-height:1;
     text-shadow:-2px 2px 0 #a9adb1,-4px 4px 0 #6e7276,-6px 6px 0 #3a3d40,-8px 8px 0 #1a1b1d,0 10px 40px rgba(0,0,0,.9)}}
.img{{position:absolute;left:50%;transform:translateX(-50%)}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{MED},transparent);opacity:.55}}
.sep{{color:{LINE};margin:0 .35em}}
"""

def bg(W, H, cy):
    s = f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#24272b 0,#121416 {W*.42:.0f}px,{BASE} {W*.9:.0f}px)'></div>"
    for ang, op, w in [(-34, .10, 7), (-18, .15, 5), (-6, .2, 4), (6, .2, 4), (18, .15, 5), (34, .10, 7)]:
        s += (f"<div style='position:absolute;left:50%;top:-60px;width:{W*.06:.0f}px;height:{H*1.2:.0f}px;transform-origin:50% 0;"
              f"transform:translateX(-50%) rotate({ang}deg);background:linear-gradient(to bottom,rgba(236,236,236,{op*.5:.2f}),rgba(236,236,236,0) 80%);filter:blur({w*6}px)'></div>")
    return s

def nomes(fs):
    return f"<div class='c nm' style='font-size:{fs}px'>" + "<span class='sep'>·</span>".join(LINEUP) + "</div>"

def render(name, W, H, html):
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, 'p.html'); shot = os.path.join(tmp, 's.png')
    open(page, 'w', encoding='utf-8').write(f"<!doctype html><meta charset=utf-8><style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
    subprocess.run([BROWSER, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--window-size={W},{H}', '--virtual-time-budget=6000', f'--screenshot={shot}', 'file:///' + page.replace('\\', '/')],
                   check=True, capture_output=True)
    im = Image.open(shot).convert('RGB').crop((0, 0, W * 2, H * 2)); shutil.rmtree(tmp)
    random.seed(13); n = Image.effect_noise(im.size, 26).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .14); im.save(f'{OUT}/{name}.png'); print(name, im.size)
    return im

foto = lambda top, w: f"<img class='img' src='data:image/png;base64,{FOTO}' style='top:{top}px;width:{w}px'>"

# FEED 4:5
feed = render('2011_feed_afterzin_final', 1080, 1350, bg(1080, 1350, 360) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:58px;width:190px'>
<div class='c sm' style='top:160px;font-size:19px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:205px;width:760px;transform:translateX(-50%) rotate(-6deg)'>
{foto(398, 1080)}
<div class='c hl' style='top:912px;font-size:118px'>{HEADLINER}</div>
<div class='c' style='top:1044px'>{nomes(40)}</div>
<div class='rule' style='top:1108px;width:420px'></div>
<div class='c sm' style='top:1124px;font-size:27px;color:{DEST}'>{QUANDO}</div>
<div class='c fr' style='top:1170px;font-size:31px'>{FRASE}</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1228px;width:120px;opacity:.9'>
<div class='c sm' style='top:1306px;font-size:14px'>{INGRESSOS}</div>
""")

# STORY 9:16 — área segura 250 topo / 330 base
render('2011_story_afterzin_final', 1080, 1920, bg(1080, 1920, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:250px;width:230px'>
<div class='c sm' style='top:372px;font-size:22px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:425px;width:880px;transform:translateX(-50%) rotate(-6deg)'>
{foto(680, 1080)}
<div class='c hl' style='top:1182px;font-size:140px'>{HEADLINER}</div>
<div class='c' style='top:1352px'>{nomes(40)}</div>
<div class='rule' style='top:1428px;width:460px'></div>
<div class='c sm' style='top:1452px;font-size:29px;color:{DEST}'>{QUANDO}</div>
<div class='c fr' style='top:1500px;font-size:36px'>{FRASE}</div>
<div class='c sm' style='top:1568px;font-size:17px'>BALLY CLUB · {INGRESSOS}</div>
""")

# site: JPG 1080×1350
feed.resize((1080, 1350), Image.LANCZOS).save(SITE + '/afterzin-2011.jpg', quality=84, optimize=True, progressive=True)
print('site ok')
