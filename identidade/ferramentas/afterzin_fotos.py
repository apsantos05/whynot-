"""afterzin why not? — versão com fotos dos DJs (P&B grafite). Feed 4:5 + story, 2x.
Uso: python3 afterzin_fotos.py <pasta fontes>"""
import os, base64, random, sys, io
from PIL import Image, ImageOps, ImageEnhance, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
A = R + '/afterzin-2011'; OUT = A + '/artes'; os.makedirs(OUT, exist_ok=True)
E1 = R + '/edicao-01/fotos-djs/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
WN = R + '/assets/logo/grafite/logo-why-not-grafite.png'
AZ = A + '/assets/wordmark-afterzin-grafite.png'
BALLY = A + '/assets/bally_logo_grafite.png'
BASE, DEST, MED, LINE = '#08090a', '#ececec', '#a9adb1', '#2c2f33'

# nome, arquivo recortado, fração da altura do recorte a manter (cabeça → cintura)
DJS = [('Mexikanno', E1 + 'mex.png', .62), ('Caio Alves', A + '/fotos/caio.png', 1.0),
       ('Coiote', E1 + 'coiote.png', .60), ('ALOIRA', A + '/fotos/aloira.png', .50),
       ('Maka', E1 + 'maka.png', .80)]

def prep(path, keep):
    im = Image.open(path).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    im = im.crop((0, 0, im.width, round(im.height * keep)))
    a = im.getchannel('A'); g = ImageOps.grayscale(im.convert('RGB'))
    g = ImageOps.autocontrast(g, cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.2)
    lo, hi = (8, 9, 10), (236, 236, 236)
    rgb = Image.merge('RGB', [g.point(lambda v, l=lo[i], h=hi[i]: round(l + (h - l) * v / 255)) for i in range(3)])
    rgb.putalpha(a)
    # esfuma a base
    fade = Image.linear_gradient('L').resize(rgb.size).point(lambda v: 255 if v < 150 else max(0, 255 - (v - 150) * 2.4))
    rgb.putalpha(ImageChops.multiply(a, fade))
    rgb.thumbnail((900, 1100), Image.LANCZOS)
    buf = io.BytesIO(); rgb.save(buf, 'PNG'); return base64.b64encode(buf.getvalue()).decode(), rgb.size

P = [prep(p, k) for _, p, k in DJS]

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BASE};overflow:hidden;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:{DEST}}}
.sm{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.3em;text-indent:.3em}}
.nm{{position:absolute;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:{DEST};text-align:center;white-space:nowrap;transform:translateX(-50%);text-shadow:0 4px 20px rgba(0,0,0,.9)}}
.img{{position:absolute;left:50%;transform:translateX(-50%)}}
.dj{{position:absolute;transform:translateX(-50%)}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{MED},transparent);opacity:.5}}
"""

def bg(W, H, cy):
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#1d2023 0,#101214 {W*.42:.0f}px,{BASE} {W*.9:.0f}px)'></div>")

def row(W, base_y, h_center, h_side, h_out, spread):
    # ordem visual: Mex, Caio, Coiote(centro), ALOIRA, Maka; o centro na frente
    xs = [W / 2 - 2 * spread, W / 2 - spread, W / 2, W / 2 + spread, W / 2 + 2 * spread]
    hs = [h_out, h_side, h_center, h_side, h_out]
    z = [1, 2, 3, 2, 1]
    html = ''
    for i, ((name, _, _), (data, (w, h))) in enumerate(zip(DJS, P)):
        hh = hs[i]; ww = w * hh / h
        html += (f"<img class='dj' src='data:image/png;base64,{data}' style='left:{xs[i]:.0f}px;top:{base_y-hh:.0f}px;height:{hh:.0f}px;z-index:{z[i]}'>")
    return html, xs

def names(xs, y, fs):
    return ''.join(f"<div class='nm' style='left:{x:.0f}px;top:{y}px;font-size:{fs}px;z-index:9'>{n}</div>" for (n, _, _), x in zip(DJS, xs))

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(13); n = Image.effect_noise(im.size, 26).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .16); im.save(f'{OUT}/{name}.png'); print(name, im.size)

# FEED 4:5
r, xs = row(1080, 960, 470, 470, 420, 208)
render('2011_feed_afterzin', 1080, 1350, bg(1080, 1350, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:56px;width:200px'>
<div class='c sm' style='top:158px;font-size:19px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:205px;width:760px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
{r}
<div style='position:absolute;left:0;right:0;top:860px;height:140px;background:linear-gradient(to bottom,transparent,{BASE} 70%);z-index:8'></div>
{names(xs, 930, 34)}
<div class='c sm' style='top:1035px;font-size:30px;color:{DEST};z-index:9'>SEXTA · 20.11 · 01H</div>
<div class='c fr' style='top:1088px;font-size:34px;color:{MED};z-index:9'>o show acaba à meia-noite. a noite, não.</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1170px;width:170px;opacity:.9'>
<div class='c sm' style='top:1275px;font-size:16px'>INGRESSOS NO SITE DA BALLY OU NA PORTARIA</div>
""")

# STORY — área segura 250 topo / 330 base
r, xs = row(1080, 1290, 590, 600, 540, 205)
render('2011_story_afterzin', 1080, 1920, bg(1080, 1920, 1000) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:250px;width:220px'>
<div class='c sm' style='top:360px;font-size:21px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:420px;width:900px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
{r}
<div style='position:absolute;left:0;right:0;top:1180px;height:160px;background:linear-gradient(to bottom,transparent,{BASE} 70%);z-index:8'></div>
{names(xs, 1262, 38)}
<div class='rule' style='top:1350px;width:460px;z-index:9'></div>
<div class='c fr' style='top:1380px;font-size:44px;z-index:9'>o show acaba à meia-noite.<br><span style='color:{MED}'>a noite, não.</span></div>
<div class='c sm' style='top:1515px;font-size:30px;color:{DEST}'>SEXTA · 20.11 · 01H · BALLY CLUB</div>
<div class='c sm' style='top:1565px;font-size:18px'>INGRESSOS NO SITE DA BALLY OU NA PORTARIA</div>
""")
