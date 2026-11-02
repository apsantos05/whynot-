"""'é hoje.' v2 — mais impacto: tipografia gigante iluminada pela vela, brasas, line-up e 18h."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HN = R + '/halloween-no-one-leaves'
FD = sys.argv[1]
OUT = HN + '/stories-diarios'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = R + '/assets/logo/halloween/logo-why-not-halloween.png'
FOOT = HN + '/patrocinadores/rodape_patrocinadores_2160.png'
VELA = HN + '/fotos-base/vela-castical.jpg'

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0b0706;overflow:hidden;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:#efe4d0;text-shadow:0 4px 30px rgba(0,0,0,.95)}}
.sm{{font-family:SM;font-weight:700;color:#c4a582;letter-spacing:.3em;text-indent:.3em;text-shadow:0 3px 16px rgba(0,0,0,.95)}}
.hoje{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;line-height:1;padding-bottom:.2em;letter-spacing:-.02em;
      background:linear-gradient(to bottom,#ffd9a0 0%,#f3e2c4 30%,#efe4d0 60%,#c4a582 100%);
      -webkit-background-clip:text;background-clip:text;color:transparent;
      filter:drop-shadow(0 0 40px rgba(255,150,60,.35)) drop-shadow(0 14px 30px rgba(0,0,0,.95))}}
.n18{{font-family:FrV;font-style:normal;font-weight:900;font-variation-settings:'opsz' 144;color:#efe4d0}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#c4a582,transparent)}}
.logo{{position:absolute;left:50%;transform:translateX(-50%);filter:drop-shadow(0 6px 30px rgba(0,0,0,.85))}}
"""

def embers(W, H, fx, fy, n, seed):
    random.seed(seed); s = ''
    for _ in range(n):
        x = fx + random.gauss(0, W * .2); y = fy + random.uniform(-H * .3, H * .12)
        r = random.uniform(2, 6); a = random.uniform(.35, .95); bl = random.uniform(0, 2.5)
        s += (f"<div style='position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;"
              f"background:radial-gradient(circle,#ffd08a 0,#e07a2a 55%,transparent 75%);opacity:{a:.2f};filter:blur({bl:.1f}px);"
              f"box-shadow:0 0 {r*3:.0f}px rgba(255,140,50,.8)'></div>")
    return s

def bg(W, H, size, pos, fx, fy, dark_from):
    return (f"<div style=\"position:absolute;inset:0;background:url(data:image/jpeg;base64,{b64(VELA)}) {pos}/{size} no-repeat;"
            f"filter:sepia(.3) saturate(1.2) brightness(.95) contrast(1.08)\"></div>"
            f"<div style='position:absolute;inset:0;background:radial-gradient(circle at {fx}px {fy}px,rgba(255,140,50,.28) 0,rgba(122,58,22,.22) {W*.28:.0f}px,transparent {W*.62:.0f}px);mix-blend-mode:screen'></div>"
            f"<div style='position:absolute;inset:0;background:linear-gradient(to bottom,rgba(11,7,6,.8) 0%,transparent 16%,transparent {dark_from}%,rgba(11,7,6,.9) {dark_from+12}%,#0b0706 100%)'></div>"
            "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,transparent 40%,rgba(11,7,6,.9) 100%)'></div>"
            + embers(W, H, fx, fy, 34, 3))

def render(name, W, H, html, scale=1, foot=False):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=scale)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        tmp = f'{OUT}/_{name}.png'; pg.screenshot(path=tmp); br.close()
    im = Image.open(tmp).convert('RGB'); os.remove(tmp)
    if foot:
        ft = Image.open(FOOT).convert('RGBA'); k = im.width / ft.width
        ft = ft.resize((im.width, round(ft.height * k)), Image.LANCZOS)
        im = im.convert('RGBA'); im.alpha_composite(ft, (0, im.height - ft.height - round(36 * scale))); im = im.convert('RGB')
    random.seed(7); n = Image.effect_noise(im.size, 22).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .16)
    im.save(f'{OUT}/{name}.png'); print(name, im.size)

DJS1 = 'Caio Tofole · Oliver · Matheus Sanchez'
DJS2 = 'Possani · Maka · Coiote'

# STORY 1080x1920 — vela: chama ~ (540, 540)
render('0211_story_e-hoje', 1080, 1920, bg(1080, 1920, '1250px auto', '50% -170px', 540, 520, 44) + f"""
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:120px;width:300px'>
<div class='c fr' style='top:206px;font-size:30px;opacity:.85'>no one leaves.</div>
<div class='c fr' style='top:798px;font-size:110px;color:#ffe2b8'>é</div>
<div class='c hoje' style='top:876px;font-size:340px'>hoje.</div>
<div class='c fr' style='top:1268px;font-size:62px'>a partir das <span class='n18'>18h</span></div>
<div class='rule' style='top:1380px;width:420px'></div>
<div class='c sm' style='top:1415px;font-size:18px'>LINE-UP</div>
<div class='c fr' style='top:1452px;font-size:38px'>{DJS1}</div>
<div class='c fr' style='top:1502px;font-size:38px'>{DJS2}</div>
<div class='c sm' style='top:1568px;font-size:20px;color:#efe4d0'>+ ALOIRA <span style='color:#c4a582'>· ATRAÇÃO SURPRESA</span></div>
<div class='rule' style='top:1640px;width:420px'></div>
<div class='c fr' style='top:1668px;font-size:40px;color:#c4a582'>vem fantasiado. tem prêmio.</div>
<div class='c sm' style='top:1752px;font-size:21px'>THE WEEK · JK RIO PRETO</div>
<div class='c sm' style='top:1800px;font-size:16px;color:#efe4d0;opacity:.75'>INGRESSOS NO LINK DA BIO</div>
""")

# FEED 4:5 — 1080x1350 @2x
render('0211_feed_e-hoje', 1080, 1350, bg(1080, 1350, '900px auto', '50% -150px', 540, 330, 40) + f"""
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:52px;width:250px'>
<div class='c fr' style='top:124px;font-size:25px;opacity:.85'>no one leaves.</div>
<div class='c fr' style='top:468px;font-size:86px;color:#ffe2b8'>é</div>
<div class='c hoje' style='top:540px;font-size:270px'>hoje.</div>
<div class='c fr' style='top:870px;font-size:50px'>a partir das <span class='n18'>18h</span></div>
<div class='rule' style='top:956px;width:380px'></div>
<div class='c fr' style='top:974px;font-size:30px'>{DJS1} · {DJS2}</div>
<div class='c sm' style='top:1024px;font-size:16px;color:#efe4d0'>+ ALOIRA <span style='color:#c4a582'>· ATRAÇÃO SURPRESA</span></div>
<div class='c fr' style='top:1066px;font-size:32px;color:#c4a582'>vem fantasiado. tem prêmio.</div>
<div class='c sm' style='top:1130px;font-size:18px'>02.11 · THE WEEK · JK RIO PRETO</div>
""", scale=2, foot=True)
