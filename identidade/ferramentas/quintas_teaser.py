"""quinta, por que não? — why not? × Bally Club, toda quinta. Paleta Lavanda noturna. Teaser + revelação (feed 4:5 + story), 2x."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
Q = R + '/quintas-bally'; OUT = Q + '/artes'; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
WN = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
QW = Q + '/assets/wordmark-quinta-lavanda.png'
QM = Q + '/assets/interrogacao-lavanda.png'
BALLY = Q + '/assets/bally_logo_lavanda.png'
BASE, DEST, MED, LINE = '#09080c', '#ece6f4', '#b1a6c4', '#3a3348'

if not os.path.exists(BALLY):
    im = Image.open(R + '/edicao-01/anuncio/site-bally/bally_logo_gelo.png').convert('RGBA')
    g = Image.new('RGBA', im.size, (236, 230, 244, 255)); g.putalpha(im.split()[3]); g.save(BALLY)

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BASE};overflow:hidden;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:{DEST}}}
.sm{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.3em;text-indent:.3em}}
.bk{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:{DEST};line-height:.95;letter-spacing:-.015em}}
.img{{position:absolute;left:50%;transform:translateX(-50%)}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{MED},transparent);opacity:.55}}
.duo{{position:absolute;left:0;right:0;display:flex;justify-content:center}}
.duo>div{{width:330px;text-align:center}}
.duo .v{{width:1px;background:{LINE}}}
.duo .t{{font-family:Fr;font-style:italic;color:{DEST};line-height:1}}
.duo .s{{font-family:SM;font-weight:700;color:{MED};letter-spacing:.24em;text-indent:.24em;margin-top:14px}}
"""

def bg(W, cy):
    return f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {cy}px,#261f33 0,#130f1a {W*.4:.0f}px,{BASE} {W*.85:.0f}px)'></div>"

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(11); n = Image.effect_noise(im.size, 24).convert('RGB')
    im = Image.blend(im, ImageChops.overlay(im, n), .14); im.save(f'{OUT}/{name}.png'); print(name, im.size)

def duo(top, fs, ss):
    return (f"<div class='duo' style='top:{top}px'>"
            f"<div><div class='t' style='font-size:{fs}px'>open gin</div><div class='s' style='font-size:{ss}px'>22H ÀS 23H</div></div>"
            f"<div class='v'></div>"
            f"<div><div class='t' style='font-size:{fs}px'>lista VIP</div><div class='s' style='font-size:{ss}px'>PARA ELAS</div></div></div>")

# ---------- 1) TEASER ----------
render('1_story_teaser', 1080, 1920, bg(1080, 900) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:270px;width:260px'>
<img class='img' src='data:image/png;base64,{b64(QM)}' style='top:470px;width:420px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c bk' style='top:1050px;font-size:118px'>toda quinta.<br>todo mês.</div>
<div class='c fr' style='top:1320px;font-size:52px;color:{MED}'>você vai entender o porquê.</div>
<div class='rule' style='top:1440px;width:420px'></div>
<div class='c sm' style='top:1475px;font-size:30px;color:{DEST}'>12.11 · BALLY CLUB</div>
""")
render('1_feed_teaser', 1080, 1350, bg(1080, 540) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:80px;width:240px'>
<img class='img' src='data:image/png;base64,{b64(QM)}' style='top:200px;width:330px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c bk' style='top:680px;font-size:104px'>toda quinta.<br>todo mês.</div>
<div class='c fr' style='top:920px;font-size:48px;color:{MED}'>você vai entender o porquê.</div>
<div class='rule' style='top:1040px;width:420px'></div>
<div class='c sm' style='top:1075px;font-size:30px;color:{DEST}'>12.11 · BALLY CLUB</div>
<div class='c sm' style='top:1220px;font-size:20px'>@WHYNOT.SJRP × @BALLYCLUB.OFICIAL</div>
""")

# ---------- 2) REVELAÇÃO DO NOME ----------
render('2_story_quinta-por-que-nao', 1080, 1920, bg(1080, 820) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:262px;width:240px'>
<div class='c sm' style='top:380px;font-size:20px'>× BALLY CLUB</div>
<div class='c sm' style='top:560px;font-size:24px;color:{DEST}'>TODA QUINTA · A PARTIR DE 12.11</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:630px;width:900px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:925px;font-size:120px'>por que não?</div>
<div class='rule' style='top:1150px;width:520px'></div>
{duo(1200, 72, 22)}
<div class='rule' style='top:1380px;width:520px'></div>
<div class='c sm' style='top:1420px;font-size:30px;color:{DEST}'>QUINTAS · 22H · BALLY CLUB</div>
<div class='c fr' style='top:1475px;font-size:38px;color:{MED}'>nome na lista só pelo grupo. link na bio.</div>
""")
render('2_feed_quinta-por-que-nao', 1080, 1350, bg(1080, 520) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:178px;font-size:19px'>× BALLY CLUB</div>
<div class='c sm' style='top:290px;font-size:22px;color:{DEST}'>TODA QUINTA · A PARTIR DE 12.11</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:345px;width:840px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:615px;font-size:110px'>por que não?</div>
<div class='rule' style='top:820px;width:500px'></div>
{duo(855, 64, 20)}
<div class='rule' style='top:1020px;width:500px'></div>
<div class='c sm' style='top:1055px;font-size:28px;color:{DEST}'>QUINTAS · 22H</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1130px;width:200px;opacity:.9'>
""")
