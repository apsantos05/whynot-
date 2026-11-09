"""Peças semanais da 'quinta, por que não?' (lavanda): chamada 'é hoje' e line-up da segunda. Feed 4:5 + story, 2x.
Uso: python3 quintas_semana.py <pasta fontes> ehoje <DD.MM> [estreia]
     python3 quintas_semana.py <pasta fontes> lineup <DD.MM> "DJ 1" "DJ 2" ...
"""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, KIND, DATA = sys.argv[1], sys.argv[2], sys.argv[3]
EXTRA = sys.argv[4:]
Q = R + '/quintas-bally'; OUT = Q + '/semanas/' + DATA.replace('.', '-'); os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
WN = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
QW = Q + '/assets/wordmark-quinta-lavanda.png'
BALLY = Q + '/assets/bally_logo_lavanda.png'
BASE, DEST, MED, LINE = '#09080c', '#ece6f4', '#b1a6c4', '#3a3348'

CSS = f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BASE};overflow:hidden;position:relative}}
.c{{position:absolute;left:60px;right:60px;text-align:center}}
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

def duo(top, fs, ss):
    return (f"<div class='duo' style='top:{top}px'><div><div class='t' style='font-size:{fs}px'>open gin</div><div class='s' style='font-size:{ss}px'>22H ÀS 23H</div></div>"
            f"<div class='v'></div><div><div class='t' style='font-size:{fs}px'>lista VIP</div><div class='s' style='font-size:{ss}px'>PARA ELAS</div></div></div>")

def render(name, W, H, html):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/_t.png'); br.close()
    im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    random.seed(11); n = Image.effect_noise(im.size, 24).convert('RGB')
    Image.blend(im, ImageChops.overlay(im, n), .14).save(f'{OUT}/{name}.png'); print(OUT + '/' + name + '.png')

D = DATA
if KIND == 'ehoje':
    est = 'estreia' in EXTRA
    kick = f'HOJE · {D} · ESTREIA' if est else f'HOJE · QUINTA · {D}'
    hora = ("<div class='c fr' style='top:{t}px;font-size:{f}px'>coquetel de lançamento às <b style=\"font-family:FrV;font-style:normal\">21h</b></div>"
            if est else "<div class='c fr' style='top:{t}px;font-size:{f}px'>a partir das <b style=\"font-family:FrV;font-style:normal\">21h</b></div>")
    render('feed_e-hoje', 1080, 1350, bg(1080, 560) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:180px;font-size:22px;color:{DEST}'>{kick}</div>
<div class='c bk' style='top:300px;font-size:300px'>é hoje.</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:610px;width:560px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:775px;font-size:64px'>por que não?</div>
{hora.format(t=885, f=44)}
<div class='rule' style='top:960px;width:480px'></div>
{duo(985, 54, 18)}
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1170px;width:170px;opacity:.9'>
""")
    render('story_e-hoje', 1080, 1920, bg(1080, 860) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:260px;width:230px'>
<div class='c sm' style='top:380px;font-size:24px;color:{DEST}'>{kick}</div>
<div class='c bk' style='top:500px;font-size:330px'>é hoje.</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:850px;width:640px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:1040px;font-size:76px'>por que não?</div>
{hora.format(t=1170, f=50)}
<div class='rule' style='top:1265px;width:520px'></div>
{duo(1300, 60, 20)}
<div class='c sm' style='top:1480px;font-size:20px'>BALLY CLUB · LISTA PELO GRUPO, LINK NA BIO</div>
""")
elif KIND == 'lineup':
    djs = EXTRA
    fs_f = 82 if len(djs) <= 4 else 66
    fs_s = 92 if len(djs) <= 4 else 76
    lst = lambda fs: ''.join(f"<div class='bk' style='font-size:{fs}px;margin:{fs*.12:.0f}px 0'>{d}</div>" for d in djs)
    render('feed_line-up', 1080, 1350, bg(1080, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:180px;font-size:22px;color:{DEST}'>QUINTA · {D} · 21H</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:240px;width:560px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:400px;font-size:60px'>por que não?</div>
<div class='rule' style='top:500px;width:480px'></div>
<div class='c sm' style='top:530px;font-size:18px'>LINE-UP</div>
<div class='c' style='top:575px'>{lst(fs_f)}</div>
<div class='rule' style='top:1010px;width:480px'></div>
{duo(1035, 50, 17)}
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1195px;width:160px;opacity:.9'>
""")
    render('story_line-up', 1080, 1920, bg(1080, 900) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:260px;width:230px'>
<div class='c sm' style='top:380px;font-size:24px;color:{DEST}'>QUINTA · {D} · 21H</div>
<img class='img' src='data:image/png;base64,{b64(QW)}' style='top:450px;width:640px;transform:translateX(-50%) rotate(-6deg)'>
<div class='c fr' style='top:640px;font-size:72px'>por que não?</div>
<div class='rule' style='top:765px;width:520px'></div>
<div class='c sm' style='top:800px;font-size:20px'>LINE-UP</div>
<div class='c' style='top:850px'>{lst(fs_s)}</div>
<div class='rule' style='top:1340px;width:520px'></div>
{duo(1370, 56, 19)}
""")
elif KIND == 'linha':   # 2 artes que fecham a fileira da line-up: contagem (direita) e frase (esquerda)
    render('feed_1_contagem', 1080, 1350, bg(1080, 600) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:180px;font-size:22px;color:{DEST}'>ESTREIA · QUINTA · {D}</div>
<div class='c sm' style='top:330px;font-size:26px'>FALTAM</div>
<div class='c bk' style='top:360px;font-size:560px;line-height:1'>3</div>
<div class='c bk' style='top:870px;font-size:96px'>dias.</div>
<div class='rule' style='top:1030px;width:480px'></div>
<div class='c fr' style='top:1060px;font-size:46px;color:{MED}'>hoje, às 18h, sai a line-up.</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1195px;width:160px;opacity:.9'>
""")
    render('feed_3_frase', 1080, 1350, bg(1080, 640) + f"""
<img class='img' src='data:image/png;base64,{b64(WN)}' style='top:70px;width:220px'>
<div class='c sm' style='top:180px;font-size:22px;color:{DEST}'>A PARTIR DE {D} · TODA QUINTA</div>
<div class='c bk' style='top:350px;font-size:170px'>quinta<br>é a nova<br>sexta.</div>
<div class='rule' style='top:900px;width:480px'></div>
<div class='c fr' style='top:930px;font-size:46px'>coquetel às 21h · open gin 22h às 23h</div>
<div class='c fr' style='top:1000px;font-size:46px;color:{MED}'>lista VIP pra elas, nome pelo grupo.</div>
<div class='c sm' style='top:1100px;font-size:20px'>LINK NA BIO</div>
<img class='img' src='data:image/png;base64,{b64(BALLY)}' style='top:1195px;width:160px;opacity:.9'>
""")
