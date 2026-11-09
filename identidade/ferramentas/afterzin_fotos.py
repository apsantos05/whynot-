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

# nome, arquivo recortado, centro do rosto (fração da largura), altura da cabeça (fração da altura)
DJS = [('Mexikanno', E1 + 'mex.png', .38, .25), ('Kaio Alves', A + '/fotos/kaio.png', .51, .39),
       ('Coiote', E1 + 'coiote.png', .47, .23), ('ALOIRA', A + '/fotos/aloira.png', .40, .20),
       ('Maka', E1 + 'maka.png', .48, .31)]

def prep(path, hf):
    im = Image.open(path).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    im = im.crop((0, 0, im.width, round(im.height * min(1, hf * 3.4))))   # cabeça → cintura
    a = im.getchannel('A'); g = ImageOps.grayscale(im.convert('RGB'))
    g = ImageOps.autocontrast(g, cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.2)
    lo, hi = (8, 9, 10), (236, 236, 236)
    rgb = Image.merge('RGB', [g.point(lambda v, l=lo[i], h=hi[i]: round(l + (h - l) * v / 255)) for i in range(3)])
    fade = Image.linear_gradient('L').resize(rgb.size).point(lambda v: 255 if v < 140 else max(0, 255 - (v - 140) * 2.2))
    rgb.putalpha(ImageChops.multiply(a, fade))
    full_h = im.height / min(1, hf * 3.4)
    buf = io.BytesIO(); rgb.save(buf, 'PNG'); return base64.b64encode(buf.getvalue()).decode(), rgb.size, full_h

P = [prep(p, hf) for _, p, _, hf in DJS]

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

def row(W, head_top, head_h, spread):
    # uma fileira, rostos todos na mesma altura e sem se sobrepor; ombros podem se cruzar
    xs = [W / 2 + (k - 2) * spread for k in range(5)]
    z = [1, 2, 3, 2, 1]
    html = ''
    for k, ((name, _, cx, hf), (data, (w, h), full_h)) in enumerate(zip(DJS, P)):
        sc = head_h / (hf * full_h); ww, hh = w * sc, h * sc
        html += (f"<img src='data:image/png;base64,{data}' style='position:absolute;left:{xs[k]-cx*ww:.0f}px;top:{head_top:.0f}px;"
                 f"width:{ww:.0f}px;height:{hh:.0f}px;z-index:{z[k]}'>")
    return html, xs

def names(xs, y, fs):
    return ''.join(f"<div class='nm' style='left:{x:.0f}px;top:{y}px;font-size:{fs}px;z-index:9'>{n}</div>" for (n, _, _, _), x in zip(DJS, xs))

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
def feed(name, kick, date):
  r, xs = row(1080, 470, 140, 205)
  render(name, 1080, 1350, bg(1080, 1350, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:56px;width:200px'>
<div class='c sm' style='top:158px;font-size:19px;color:{DEST}'>{kick}</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:205px;width:760px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
{r}
<div style='position:absolute;left:0;right:0;top:860px;height:140px;background:linear-gradient(to bottom,transparent,{BASE} 70%);z-index:8'></div>
{names(xs, 930, 34)}
<div class='c sm' style='top:1037px;font-size:27px;color:{DEST};z-index:9'>{date}</div>
<div class='c fr' style='top:1088px;font-size:34px;color:{MED};z-index:9'>o show acaba à meia-noite. a noite, não.</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1170px;width:170px;opacity:.9'>
<div class='c sm' style='top:1275px;font-size:16px'>INGRESSOS NO SITE DA BALLY OU NA PORTARIA</div>
""")

# STORY — área segura 250 topo / 330 base
def story(name, kick, date):
  r, xs = row(1080, 760, 160, 205)
  render(name, 1080, 1920, bg(1080, 1920, 1000) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:250px;width:220px'>
<div class='c sm' style='top:360px;font-size:21px;color:{DEST}'>{kick}</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:420px;width:900px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
{r}
<div style='position:absolute;left:0;right:0;top:1180px;height:160px;background:linear-gradient(to bottom,transparent,{BASE} 70%);z-index:8'></div>
{names(xs, 1262, 38)}
<div class='rule' style='top:1350px;width:460px;z-index:9'></div>
<div class='c fr' style='top:1380px;font-size:44px;z-index:9'>o show acaba à meia-noite.<br><span style='color:{MED}'>a noite, não.</span></div>
<div class='c sm' style='top:1505px;font-size:28px;color:{DEST}'>{date}</div>
<div class='c sm' style='top:1550px;font-size:22px'>BALLY CLUB</div>
<div class='c sm' style='top:1590px;font-size:16px'>INGRESSOS NO SITE DA BALLY OU NA PORTARIA</div>
""")

feed('2011_feed_afterzin', 'ACABOU O VINTAGE CULTURE?', 'SEXTA PRA SÁBADO · 21.11 · 01H')
story('2011_story_afterzin', 'ACABOU O VINTAGE CULTURE?', 'SEXTA PRA SÁBADO · 21.11 · 01H')
feed('2011_feed_afterzin_E-HOJE', 'É HOJE · ACABOU O VINTAGE? VEM.', 'HOJE · A PARTIR DA 01H · BALLY CLUB')
story('2011_story_afterzin_E-HOJE', 'É HOJE · ACABOU O VINTAGE? VEM.', 'HOJE · A PARTIR DA 01H')
