"""afterzin why not? — after pós Vintage Culture, Bally Club, 20.11, 01h. Paleta Grafite. Feed 4:5 + story, 2x."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
A = R + '/afterzin-2011'; OUT = A + '/artes'; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
WN = R + '/assets/logo/grafite/logo-why-not-grafite.png'
AZ = A + '/assets/wordmark-afterzin-grafite.png'
BALLY = A + '/assets/bally_logo_grafite.png'
BASE, DEST, MED, LINE = '#08090a', '#ececec', '#a9adb1', '#2c2f33'
LINEUP = ['Mexikanno', 'Caio Alves', 'Coiote', 'ALOIRA', 'Maka']

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BASE};overflow:hidden;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:{DEST}}}
.sm{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.3em;text-indent:.3em}}
.nm{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:{DEST};line-height:1.02;letter-spacing:-.01em}}
.dot{{display:block;color:{LINE};font-family:SM;font-weight:700}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{MED},transparent);opacity:.6}}
.img{{position:absolute;left:50%;transform:translateX(-50%)}}
.big{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:#191b1e;line-height:1;letter-spacing:-.04em}}
"""

def beams(W, H, top):
    # feixes de luz de palco saindo do alto, desfocados (grafite)
    s = ''
    for ang, op, w in [(-38, .10, 7), (-22, .16, 5), (-8, .22, 4), (8, .22, 4), (22, .16, 5), (38, .10, 7)]:
        s += (f"<div style='position:absolute;left:50%;top:{top}px;width:{W*.06:.0f}px;height:{H*1.25:.0f}px;transform-origin:50% 0;"
              f"transform:translateX(-50%) rotate({ang}deg);background:linear-gradient(to bottom,rgba(236,236,236,{op*.55:.2f}),rgba(236,236,236,0) 85%);"
              f"filter:blur({w*6}px)'></div>")
    s += (f"<div style='position:absolute;left:0;right:0;bottom:0;height:{H*.42:.0f}px;background:radial-gradient(ellipse at 50% 100%,rgba(40,43,47,.9),transparent 70%)'></div>")
    return s

def bg(W, H, cy):
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#24272b 0,#121416 {W*.4:.0f}px,{BASE} {W*.85:.0f}px)'></div>"
            + beams(W, H, -60))

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(13); n = Image.effect_noise(im.size, 26).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .16); im.save(f'{OUT}/{name}.png'); print(name, im.size)

def names(size, gap):
    return ''.join(f"<div class='nm' style='font-size:{size}px;margin:{gap}px 0'>{n}</div>" for n in LINEUP)

# STORY — área segura 250 topo / 330 base
render('2011_story_afterzin', 1080, 1920, bg(1080, 1920, 760) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:262px;width:250px'>
<div class='c sm' style='top:400px;font-size:22px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:470px;width:900px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:745px;font-size:54px'>o show acaba à meia-noite.<br><span style='color:{MED}'>a noite, não.</span></div>
<div class='rule' style='top:925px;width:460px'></div>
<div class='c sm' style='top:960px;font-size:20px'>LINE-UP</div>
<div class='c' style='top:1000px'>{names(76, 2)}</div>
<div class='rule' style='top:1460px;width:460px'></div>
<div class='c sm' style='top:1495px;font-size:30px;color:{DEST}'>SEXTA · 20.11 · 01H</div>
<div class='c sm' style='top:1545px;font-size:24px'>BALLY CLUB</div>
<div class='c fr' style='top:1595px;font-size:36px;color:{MED}'>ingressos no site da Bally ou na portaria.</div>
""")

# FEED 4:5
render('2011_feed_afterzin', 1080, 1350, bg(1080, 1350, 420) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:190px;font-size:20px;color:{DEST}'>ACABOU O VINTAGE CULTURE?</div>
<img class='img' src='data:image/png;base64,{b64(AZ)}' style='top:255px;width:860px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:520px;font-size:46px'>o show acaba à meia-noite. <span style='color:{MED}'>a noite, não.</span></div>
<div class='rule' style='top:610px;width:420px'></div>
<div class='c' style='top:630px'>{''.join(f"<span class='nm' style='font-size:62px;display:inline-block;margin:6px 18px'>{n}</span>" for n in LINEUP)}</div>
<div class='rule' style='top:800px;width:420px'></div>
<div class='c sm' style='top:835px;font-size:30px;color:{DEST}'>SEXTA · 20.11 · 01H</div>
<div class='c fr' style='top:890px;font-size:34px;color:{MED}'>ingressos no site da Bally ou na portaria.</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1010px;width:250px;opacity:.9'>
<div class='c sm' style='top:1180px;font-size:18px'>AV. DR. ALBERTO ANDALÓ, 3837 · RIO PRETO</div>
""")
