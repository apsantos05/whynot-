"""Line-up da 'quinta, por que não?' com fotos dos DJs (P&B, tom lavanda). Feed 4:5 + story, 2x.
Uso: python3 quintas_lineup_fotos.py <pasta fontes> <DD.MM>   (DJs definidos em DJS abaixo)"""
import os, base64, random, sys, io
from PIL import Image, ImageOps, ImageEnhance, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, D = sys.argv[1], sys.argv[2]
Q = R + '/quintas-bally'; OUT = Q + '/semanas/' + D.replace('.', '-'); os.makedirs(OUT, exist_ok=True)
E1 = R + '/edicao-01/fotos-djs/'; QF = Q + '/fotos-djs/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
WN = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
QW = Q + '/assets/wordmark-quinta-lavanda.png'
BALLY = Q + '/assets/bally_logo_lavanda.png'
BASE, DEST, MED, LINE = '#09080c', '#ece6f4', '#b1a6c4', '#3a3348'

# nome, recorte, centro do rosto (fração da largura), topo da cabeça e altura da cabeça (frações da altura)
DJS = [('Mari Ferro', QF + 'mari.png', .39, .01, .18), ('Maycon', E1 + 'maycon.png', .48, 0, .30),
       ('Charles', E1 + 'possani.png', .48, 0, .28), ('Camuri', QF + 'camuri.png', .46, 0, .21),
       ('Mexikanno', E1 + 'mex.png', .38, 0, .25)]

def prep(path, top, hf):
    im = Image.open(path).convert('RGBA')
    a = im.getchannel('A').point(lambda v: 0 if v < 40 else v); im.putalpha(a)
    im = im.crop(a.getbbox())
    H0 = im.height
    keep = min(1, top + hf * 3.4)
    im = im.crop((0, round(H0 * top), im.width, round(H0 * keep)))
    a = im.getchannel('A'); g = ImageOps.grayscale(im.convert('RGB'))
    g = ImageOps.autocontrast(g, cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.15)
    lo, hi = (9, 8, 12), (236, 230, 244)   # duotom lavanda
    rgb = Image.merge('RGB', [g.point(lambda v, l=lo[i], h=hi[i]: round(l + (h - l) * v / 255)) for i in range(3)])
    fade = Image.linear_gradient('L').resize(rgb.size).point(lambda v: 255 if v < 140 else max(0, 255 - (v - 140) * 2.2))
    rgb.putalpha(ImageChops.multiply(a, fade))
    head_px = hf * H0
    buf = io.BytesIO(); rgb.save(buf, 'PNG'); return base64.b64encode(buf.getvalue()).decode(), rgb.size, head_px

P = [prep(p, t, hf) for _, p, _, t, hf in DJS]

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
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{MED},transparent);opacity:.55}}
.duo{{position:absolute;left:0;right:0;display:flex;justify-content:center}}
.duo>div{{width:300px;text-align:center}}
.duo .v{{width:1px;background:{LINE}}}
.duo .t{{font-family:Fr;font-style:italic;color:{DEST};line-height:1}}
.duo .s{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.24em;text-indent:.24em;margin-top:12px}}
"""

def bg(W, cy):
    return f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#261f33 0,#130f1a {W*.42:.0f}px,{BASE} {W*.9:.0f}px)'></div>"

def duo(top, fs, ss):
    return (f"<div class='duo' style='top:{top}px;z-index:9'><div><div class='t' style='font-size:{fs}px'>open gin</div><div class='s' style='font-size:{ss}px'>22H ÀS 23H</div></div>"
            f"<div class='v'></div><div><div class='t' style='font-size:{fs}px'>lista VIP</div><div class='s' style='font-size:{ss}px'>PARA ELAS</div></div></div>")

def row(W, head_top, head_h, spread):
    xs = [W / 2 + (k - 2) * spread for k in range(5)]
    z = [1, 2, 3, 2, 1]; html = ''
    for k, ((_, _, cx, _, _), (data, (w, h), head_px)) in enumerate(zip(DJS, P)):
        sc = head_h / head_px; ww, hh = w * sc, h * sc
        html += (f"<img src='data:image/png;base64,{data}' style='position:absolute;left:{xs[k]-cx*ww:.0f}px;top:{head_top:.0f}px;"
                 f"width:{ww:.0f}px;height:{hh:.0f}px;z-index:{z[k]}'>")
    return html, xs

def names(xs, y, fs):
    return ''.join(f"<div class='nm' style='left:{x:.0f}px;top:{y}px;font-size:{fs}px;z-index:9'>{n}</div>" for (n, *_), x in zip(DJS, xs))

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(11); n = Image.effect_noise(im.size, 24).convert('RGB')
    Image.blend(im, ImageChops.overlay(im, n), .14).save(f'{OUT}/{name}.png'); print(f'{OUT}/{name}.png')

r, xs = row(1080, 470, 140, 205)
render('feed_line-up', 1080, 1350, bg(1080, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:56px;width:200px'>
<div class='c sm' style='top:158px;font-size:20px;color:{DEST}'>QUINTA · {D} · 21H · ESTREIA</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:200px;width:520px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
<div class='c fr' style='top:350px;font-size:56px;z-index:5'>por que não?</div>
{r}
<div style='position:absolute;left:0;right:0;top:860px;height:140px;background:linear-gradient(to bottom,transparent,{BASE} 70%);-webkit-mask-image:linear-gradient(to right,transparent,#000 20%,#000 80%,transparent);z-index:8'></div>
{names(xs, 930, 34)}
<div class='rule' style='top:1010px;width:460px;z-index:9'></div>
<div class='c fr' style='top:1030px;font-size:38px;z-index:9'>coquetel de lançamento às 21h</div>
{duo(1095, 46, 16)}
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1225px;width:150px;opacity:.9'>
""")

r, xs = row(1080, 760, 160, 205)
render('story_line-up', 1080, 1920, bg(1080, 1000) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:250px;width:220px'>
<div class='c sm' style='top:360px;font-size:22px;color:{DEST}'>QUINTA · {D} · 21H · ESTREIA</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:420px;width:640px;transform:translateX(-50%) rotate(-6deg);z-index:5'>
<div class='c fr' style='top:610px;font-size:72px;z-index:5'>por que não?</div>
{r}
<div style='position:absolute;left:0;right:0;top:1180px;height:160px;background:linear-gradient(to bottom,transparent,{BASE} 70%);-webkit-mask-image:linear-gradient(to right,transparent,#000 20%,#000 80%,transparent);z-index:8'></div>
{names(xs, 1262, 38)}
<div class='rule' style='top:1350px;width:480px;z-index:9'></div>
<div class='c fr' style='top:1378px;font-size:44px;z-index:9'>coquetel de lançamento às 21h</div>
{duo(1450, 52, 18)}
""")
