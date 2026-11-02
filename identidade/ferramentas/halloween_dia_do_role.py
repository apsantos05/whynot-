"""Dia do rolê (02/11): 'é hoje.' (story + feed) e aviso de horário 18h (story)."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HN = R + '/halloween-no-one-leaves'
FD = sys.argv[1] if len(sys.argv) > 1 else '/tmp/fonts'
OUT = sys.argv[2] if len(sys.argv) > 2 else HN + '/stories-diarios'
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
.fr{{font-family:Fr;font-style:italic;color:#efe4d0;text-shadow:0 4px 30px rgba(0,0,0,.9)}}
.sm{{font-family:SM;font-weight:700;color:#c4a582;letter-spacing:.3em;text-indent:.3em;text-shadow:0 4px 20px rgba(0,0,0,.9)}}
.big{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:#efe4d0;line-height:1;
     text-shadow:0 0 60px rgba(196,165,130,.3),0 8px 40px rgba(0,0,0,.95)}}
.logo{{position:absolute;left:50%;transform:translateX(-50%);filter:drop-shadow(0 6px 30px rgba(0,0,0,.85))}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 45%,rgba(11,7,6,.85) 100%)}}
"""

def photo_bg(W, H, y='0px', scale=1.05, dark_from=58):
    return (f"<div style=\"position:absolute;inset:0;background:url(data:image/jpeg;base64,{b64(VELA)}) center {y}/{scale*100}% auto no-repeat;"
            f"filter:sepia(.25) saturate(1.1) brightness(.92)\"></div>"
            f"<div style='position:absolute;inset:0;background:linear-gradient(to bottom,rgba(11,7,6,.75) 0%,transparent 22%,transparent {dark_from-10}%,rgba(11,7,6,.96) {dark_from+14}%)'></div>"
            "<div class='vig'></div>")

def glow_bg(cy):
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,rgba(122,58,22,.55) 0,rgba(46,22,10,.35) 380px,transparent 760px)'></div>"
            "<div class='vig'></div>")

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
        im = im.convert('RGBA'); im.alpha_composite(ft, (0, im.height - ft.height - round(40 * scale))); im = im.convert('RGB')
    random.seed(7); n = Image.effect_noise(im.size, 22).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .18)
    im.save(f'{OUT}/{name}.png'); print(name, im.size)

INFO = '02.11 · 18H · THE WEEK · JK RIO PRETO'

# 1) É HOJE — story
render('0211_story_e-hoje', 1080, 1920, photo_bg(1080, 1920, '120px', 1.55, 62) + f"""
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:170px;width:330px'>
<div class='c fr' style='top:262px;font-size:32px;opacity:.85'>no one leaves.</div>
<div class='c fr' style='top:1150px;font-size:96px'>é</div>
<div class='c big' style='top:1250px;font-size:250px'>hoje.</div>
<div class='c sm' style='top:1560px;font-size:22px'>{INFO}</div>
<div class='c fr' style='top:1610px;font-size:38px'>vem fantasiado.</div>
<div class='c sm' style='top:1720px;font-size:18px;color:#efe4d0;opacity:.8'>INGRESSOS NO LINK DA BIO</div>
""")

# 2) É HOJE — feed 4:5 (2160x2700) com patrocinadores
render('0211_feed_e-hoje', 1080, 1350, photo_bg(1080, 1350, '-40px', 1.25, 52) + f"""
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:70px;width:300px'>
<div class='c fr' style='top:156px;font-size:28px;opacity:.85'>no one leaves.</div>
<div class='c fr' style='top:700px;font-size:80px'>é</div>
<div class='c big' style='top:780px;font-size:210px'>hoje.</div>
<div class='c sm' style='top:1030px;font-size:19px'>{INFO}</div>
<div class='c fr' style='top:1072px;font-size:32px'>vem fantasiado.</div>
""", scale=2, foot=True)

# 3) AVISO DE HORÁRIO — story
render('0211_story_aviso-horario-18h', 1080, 1920, glow_bg(1050) + f"""
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:170px;width:330px'>
<div class='c fr' style='top:262px;font-size:32px;opacity:.85'>no one leaves.</div>
<div class='c sm' style='top:520px;font-size:24px'>AVISO · NOVO HORÁRIO</div>
<div class='c fr' style='top:600px;font-size:50px;line-height:1.25'>a chuva atrasou a<br>montagem do palco.</div>
<div class='c fr' style='top:800px;font-size:60px'>a festa começa às</div>
<div class='c big' style='top:880px;font-size:330px'>18h</div>
<div class='c sm' style='top:1240px;font-size:36px;color:#c4a582;opacity:.75'><span style='text-decoration:line-through;text-decoration-thickness:3px'>17H</span></div>
<div class='c fr' style='top:1360px;font-size:44px;color:#c4a582'>a gente te espera.</div>
<div class='c sm' style='top:1560px;font-size:22px'>{INFO}</div>
<div class='c fr' style='top:1610px;font-size:38px'>vem fantasiado.</div>
""")
