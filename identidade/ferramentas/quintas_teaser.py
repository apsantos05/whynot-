"""Quintas why not? × Bally — teaser de suspense (feed 4:5 + story), paleta Lavanda noturna. Exporta 2x."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
OUT = R + '/quintas-bally/01-teaser'; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
BASE, DEST, MED, LINE = '#09080c', '#ece6f4', '#b1a6c4', '#3a3348'

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BASE};overflow:hidden;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:{DEST}}}
.sm{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.32em;text-indent:.32em}}
.q{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:#16131d;line-height:1}}
.strike{{position:relative;display:inline-block;color:{MED};opacity:.75}}
.strike:after{{content:'';position:absolute;left:-4%;right:-4%;top:56%;height:.055em;background:{DEST};transform:rotate(-4deg)}}
.logo{{position:absolute;left:50%;transform:translateX(-50%)}}
"""

def glow(W, H, cy):
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#221c2e 0,#120f19 {W*.38:.0f}px,{BASE} {W*.8:.0f}px)'></div>")

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(11); n = Image.effect_noise(im.size, 24).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .14); im.save(f'{OUT}/{name}.png'); print(name, im.size)

# STORY (área segura: 250 topo / 330 base)
render('0411_story_teaser-quintas', 1080, 1920, glow(1080, 1920, 900) + f"""
<div class='c q' style='top:330px;font-size:1300px;opacity:.9'>?</div>
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:270px;width:330px'>
<div class='c sm' style='top:390px;font-size:22px'>× BALLY CLUB</div>
<div class='c fr' style='top:700px;font-size:150px'><span class='strike'>quintinha</span></div>
<div class='c fr' style='top:930px;font-size:78px;line-height:1.1'>agora é<br>outra coisa.</div>
<div class='c sm' style='top:1250px;font-size:30px;color:{DEST}'>TODA QUINTA</div>
<div class='c sm' style='top:1300px;font-size:30px'>DE NOVEMBRO</div>
<div class='c fr' style='top:1440px;font-size:46px;color:{MED}'>uma novidade por semana.</div>
""")

# FEED 4:5
render('0411_feed_teaser-quintas', 1080, 1350, glow(1080, 1350, 640) + f"""
<div class='c q' style='top:120px;font-size:1100px;opacity:.9'>?</div>
<img class='logo' src='data:image/png;base64,{b64(LOGO)}' style='top:100px;width:300px'>
<div class='c sm' style='top:210px;font-size:20px'>× BALLY CLUB</div>
<div class='c fr' style='top:420px;font-size:140px'><span class='strike'>quintinha</span></div>
<div class='c fr' style='top:640px;font-size:72px;line-height:1.1'>agora é<br>outra coisa.</div>
<div class='c sm' style='top:930px;font-size:30px;color:{DEST}'>TODA QUINTA DE NOVEMBRO</div>
<div class='c fr' style='top:1000px;font-size:44px;color:{MED}'>uma novidade por semana.</div>
<div class='c sm' style='top:1190px;font-size:20px'>EM BREVE · @WHYNOT.SJRP</div>
""")
