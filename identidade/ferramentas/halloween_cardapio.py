"""Cardápio de drinks Halloween — impressão A3 (297x420mm) com sangria de 3mm. Gera PDF vetorial + PNG."""
import os, base64, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HN = R + '/halloween-no-one-leaves'
FD = sys.argv[1]
OUT = HN + '/cardapio'; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = R + '/assets/logo/halloween/logo-why-not-halloween.png'
TW = HN + '/patrocinadores/logo_theweek_osso.png'

BL = 3                     # sangria mm
PW, PH = 297 + 2 * BL, 420 + 2 * BL

# fundo raster (200 dpi)
dpi = 200; W, H = round(PW / 25.4 * dpi), round(PH / 25.4 * dpi)
bg = Image.new('RGB', (W, H), (11, 7, 6))
def glow(cx, cy, r, col, a):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=a)
    m = m.filter(ImageFilter.GaussianBlur(r * .55)); bg.paste(col, (0, 0), m)
glow(W * .5, H * .13, W * .55, (40, 18, 8), 170)
glow(W * .5, H * .62, W * .75, (20, 11, 7), 120)
glow(W * .5, H * .95, W * .5, (30, 14, 7), 140)
vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-W * .25, -H * .15, W * 1.25, H * 1.15), fill=255)
vg = vg.filter(ImageFilter.GaussianBlur(W * .18))
bg = Image.composite(bg, Image.new('RGB', (W, H), (6, 4, 3)), vg)
random.seed(5); n = Image.effect_noise((W, H), 26).convert('RGB')
bg = Image.blend(bg, ImageChops.overlay(bg, n), .14)
BGP = OUT + '/_bg.jpg'; bg.save(BGP, quality=92)

MENU = [
    ('drinks', [('Sex on the Beach', '38'), ('Gin Tropical', '45'), ('Aperol Spritz', '40'),
                ('Ramazzotti', '38'), ('Mojito', '38'), ('Pink Gin', '45')]),
    ('garrafas', [('Tanqueray', '270'), ('Tanqueray Bossa Nova', '290'), ('Absolut', '270'),
                  ('Cîroc Red Berry', '450'), ('Red Label', '270'), ('Old Parr', '390'),
                  ('Licor', '380'), ('Gold Label', '580')]),
    ('cervejas', [('Heineken', '16'), ('Heineken Ultimate', '16'), ('Corona', '16'),
                  ('Chopp 300 ml', '18'), ('Chopp 500 ml', '20')]),
    ('sem álcool', [('Água sem gás', '8'), ('Água com gás', '8'), ('Água tônica', '10'),
                    ('Coca-Cola', '10'), ('Coca-Cola Zero', '10'), ('Red Bull', '20'),
                    ('Combo Red Bull · 6 un.', '110'), ('Balde de gelo', '10')]),
]

def section(i, name, items):
    rows = ''.join(f"<div class='row'><span class='it'>{a}</span><span class='dots'></span><span class='pr'><small>R$</small>{p}</span></div>" for a, p in items)
    return (f"<section><div class='hd'><span class='num'>0{i+1}</span><span class='nm'>{name}</span></div>"
            f"<div class='rule'></div>{rows}<i class='c tl'></i><i class='c tr'></i><i class='c bl'></i><i class='c br'></i></section>")

secs = ''.join(section(i, n, it) for i, (n, it) in enumerate(MENU))

HTML = f"""<!doctype html><html><head><meta charset='utf-8'><style>
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
@page{{size:{PW}mm {PH}mm;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{PW}mm;height:{PH}mm}}
body{{background:#0b0706 url(data:image/jpeg;base64,{b64(BGP)}) center/cover;color:#efe4d0;position:relative;overflow:hidden;
     -webkit-print-color-adjust:exact;print-color-adjust:exact}}
.safe{{position:absolute;left:{BL+18}mm;right:{BL+18}mm;top:{BL+20}mm;bottom:{BL+16}mm;display:flex;flex-direction:column;align-items:center}}
.logo{{width:92mm;filter:drop-shadow(0 2mm 6mm rgba(0,0,0,.8))}}
.tag{{font-family:Fr;font-style:italic;font-size:15pt;color:#efe4d0;opacity:.8;margin-top:2mm}}
.kick{{font-family:SM;font-weight:700;font-size:10pt;letter-spacing:.42em;text-indent:.42em;color:#c4a582;margin-top:13mm}}
h1{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:118pt;line-height:.9;letter-spacing:-.02em;
   background:linear-gradient(to bottom,#ffd9a0,#efe4d0 55%,#c4a582);-webkit-background-clip:text;background-clip:text;color:transparent;
   padding-bottom:.12em;margin-top:2mm}}
.sub{{font-family:Fr;font-style:italic;font-size:19pt;color:#c4a582;margin-top:-1mm}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:9mm 10mm;width:100%;margin-top:13mm}}
section{{position:relative;padding:8mm 8mm 7mm;border:.3mm solid rgba(196,165,130,.28);background:rgba(11,7,6,.45)}}
.c{{position:absolute;width:5mm;height:5mm;border-color:#c4a582;border-style:solid;border-width:0}}
.tl{{left:-.3mm;top:-.3mm;border-left-width:.6mm;border-top-width:.6mm}}.tr{{right:-.3mm;top:-.3mm;border-right-width:.6mm;border-top-width:.6mm}}
.bl{{left:-.3mm;bottom:-.3mm;border-left-width:.6mm;border-bottom-width:.6mm}}.br{{right:-.3mm;bottom:-.3mm;border-right-width:.6mm;border-bottom-width:.6mm}}
.hd{{display:flex;align-items:baseline;gap:3.5mm}}
.num{{font-family:SM;font-weight:700;font-size:10pt;color:#7a3a16;letter-spacing:.1em;color:#a0522d}}
.nm{{font-family:FrV;font-weight:800;font-variation-settings:'opsz' 144;font-size:30pt;line-height:1;color:#efe4d0;letter-spacing:-.01em}}
.rule{{height:.3mm;background:linear-gradient(90deg,#c4a582,rgba(196,165,130,0));margin:4mm 0 4.5mm}}
.row{{display:flex;align-items:baseline;gap:2.5mm;padding:1.55mm 0}}
.it{{font-family:Fr;font-style:italic;font-size:15.5pt;color:#efe4d0;white-space:nowrap}}
.dots{{flex:1;border-bottom:.45mm dotted rgba(196,165,130,.45);transform:translateY(-1.2mm)}}
.pr{{font-family:SM;font-weight:700;font-size:13.5pt;color:#c4a582;white-space:nowrap}}
.pr small{{font-size:8.5pt;margin-right:1.2mm;opacity:.75}}
.foot{{margin-top:auto;width:100%;display:flex;flex-direction:column;align-items:center}}
.fr2{{font-family:Fr;font-style:italic;font-size:14pt;color:#efe4d0;opacity:.85}}
.brands{{display:flex;align-items:center;gap:9mm;margin-top:7mm}}
.brands .sep{{width:.3mm;height:16mm;background:rgba(196,165,130,.5)}}
.note{{font-family:SM;font-weight:700;font-size:7.5pt;letter-spacing:.3em;text-indent:.3em;color:#c4a582;opacity:.8;margin-top:6mm}}
</style></head><body><div class='safe'>
<img class='logo' src='data:image/png;base64,{b64(LOGO)}'>
<div class='tag'>no one leaves.</div>
<div class='kick'>HALLOWEEN · THE WEEK · 02.11</div>
<h1>cardápio.</h1>
<div class='sub'>escolha seu veneno.</div>
<div class='grid'>{secs}</div>
<div class='foot'>
  <div class='brands'><img src='data:image/png;base64,{b64(TW)}' style='height:22mm'><span class='sep'></span>
  <img src='data:image/png;base64,{b64(LOGO)}' style='width:52mm'></div>
  <div class='note'>BEBA COM MODERAÇÃO · PROIBIDA A VENDA PARA MENORES DE 18 ANOS</div>
</div></div></body></html>"""

open(OUT + '/_cardapio.html', 'w').write(HTML)
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    pg.set_content(HTML); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(600)
    pg.pdf(path=OUT + '/0211_cardapio-drinks_A3_sangria-3mm.pdf', width=f'{PW}mm', height=f'{PH}mm', print_background=True)
    # PNG (corte final, sem sangria) a 150 dpi pra conferência / tela
    pxmm = 300 / 25.4
    pg2 = br.new_page(viewport={'width': round(PW * 96 / 25.4), 'height': round(PH * 96 / 25.4)}, device_scale_factor=pxmm / (96 / 25.4))
    pg2.set_content(HTML); pg2.evaluate('document.fonts.ready.then(()=>0)'); pg2.wait_for_timeout(600)
    pg2.screenshot(path=OUT + '/_full.png'); br.close()
im = Image.open(OUT + '/_full.png'); b = round(BL * pxmm)
im.crop((b, b, im.width - b, im.height - b)).convert('RGB').save(OUT + '/0211_cardapio-drinks_A3.png')
for f in ['/_full.png', '/_bg.jpg', '/_cardapio.html']: os.remove(OUT + f)
print('ok')
