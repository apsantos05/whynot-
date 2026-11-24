"""Quinta 26.11, ressaca das provas, com a Baruc (A.A.A.E.K Odonto Unorte): story 1080x1920 e feed 1080x1350.
Nas cores da Baruc: bordô, vermelho e preto, com as duas logos. Tipografia da casa (só Fraunces).
Uso: python3 quinta_baruc.py <pasta fontes> <pasta fotos stock>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
P = R + '/quintas-bally/semanas/2026-11-26/'
LOGO_WN = R + '/assets/logo/grafite/logo-why-not-grafite.png'
LOGO_BR = P + 'logo_baruc.png'
PRETO, BORDO, VERM, BRANCO, ROSA = (12, 6, 8), (110, 18, 34), '#e3262e', '#f5eeee', '#d9b9bd'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
def coluna(W, H, f):
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))

def fundo(W, H, foto, foco, escuro):
    im = Image.open(f'{ST}/AdobeStock_{foto}.jpeg').convert('RGB')
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(foco[0] * im.width - W / 2)), im.width - W); y = min(max(0, round(foco[1] * im.height - H / 2)), im.height - H)
    g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), cutoff=.5).point(lambda v: round(255 * min(1, 1.1 * (v / 255) ** 1.2)))
    # duotone preto -> bordô -> vermelho claro nas luzes
    def tom(v, c0, c1, c2):
        t = v / 255; return round(c0 + (c1 - c0) * min(1, t * 1.6)) if t < .625 else round(c1 + (c2 - c1) * (t - .625) / .375)
    duo = Image.merge('RGB', [g.point(lambda v, a=a, b=b, c=c: tom(v, a, b, c)) for a, b, c in zip(PRETO, BORDO, (236, 92, 96))])
    return Image.composite(Image.new('RGB', (W, H), PRETO), duo, coluna(W, H, escuro))

def css(W, H):
    return f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:440;color:{BRANCO};line-height:.98;letter-spacing:-.014em;white-space:nowrap;font-variation-settings:"WONK" 0;text-shadow:0 2px 30px rgba(12,6,8,.6)}}
.v{{color:{VERM}}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{ROSA};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum","tnum";text-shadow:0 1px 16px rgba(12,6,8,.8)}}
.c{{color:{BRANCO}}} .r{{position:absolute;left:72px;height:2px;width:130px;background:{VERM}}}"""

LINE = [('22h', 'Mexikanno'), ('00h', 'DJ Camuri'), ('01h', 'Maycon Beats'), ('02h', 'Jhonatan Soares'), ('03h', 'Possani')]
def grade(y, fs, hs, passo, x=72):
    h = ''
    for i, (hora, nome) in enumerate(LINE):
        yy = y + i * passo
        h += (f"<div class='m' style='left:{x}px;top:{yy + round(fs * .30)}px;font-size:{hs}px;color:{VERM};font-weight:500'>{hora}</div>"
              f"<div class='t' style='left:{x + 120}px;top:{yy}px;font-size:{fs}px'>{nome}</div>")
    return h

def topo(top, wn_w):
    return (f"<img src='data:image/png;base64,{b64(LOGO_WN)}' style='position:absolute;left:72px;top:{top}px;width:{wn_w}px'>"
            f"<div class='m' style='left:auto;right:72px;top:{top + 18}px;font-size:25px'>quinta, por que não?</div>")

STORY = (topo(250, 160) +
  f"<img src='data:image/png;base64,{b64(LOGO_BR)}' style='position:absolute;left:50%;transform:translateX(-50%);top:360px;width:330px;filter:drop-shadow(0 12px 40px rgba(0,0,0,.6))'>"
  "<div class='m c' style='top:768px;font-size:31px'>quinta, 26.11, na Bally Club, com a Baruc Odonto Unorte</div>"
  "<div class='t' style='top:818px;font-size:150px'>ressaca<br>das <span class='v'>provas.</span></div>"
  "<div class='r' style='top:1150px'></div>"
  "<div class='m' style='top:1178px;font-size:28px'>line-up e horários</div>" + grade(1226, 62, 30, 80) +
  "<div class='m c' style='top:1650px;font-size:30px'>ingressos no link.</div>")

FEED = (topo(72, 150) +
  f"<img src='data:image/png;base64,{b64(LOGO_BR)}' style='position:absolute;right:66px;top:150px;width:250px;filter:drop-shadow(0 10px 30px rgba(0,0,0,.6))'>"
  "<div class='m c' style='top:452px;font-size:29px'>quinta, 26.11, na Bally Club</div>"
  "<div class='t' style='top:498px;font-size:132px'>ressaca<br>das <span class='v'>provas.</span></div>"
  "<div class='m' style='top:778px;font-size:27px'>com a Baruc, Odonto Unorte.</div>"
  "<div class='r' style='top:842px'></div>" + grade(872, 50, 26, 64) +
  "<div class='m c' style='top:1218px;font-size:28px'>ingressos no link da bio.</div>")

# lista VIP (link do grupo): valores com nome na lista até 00h
def precos(y, fs, gap):
    return (f"<div class='m' style='top:{y}px;font-size:{round(fs*.36)}px'>mulher, com nome na lista</div>"
            f"<div class='t' style='top:{y+round(fs*.52)}px;font-size:{fs}px'><span class='v'>free</span> até 00h.</div>"
            f"<div class='m' style='top:{y+gap}px;font-size:{round(fs*.36)}px'>homem, com nome na lista</div>"
            f"<div class='t' style='top:{y+gap+round(fs*.52)}px;font-size:{fs}px'><span class='v'>R$ 20</span> até 00h.</div>")

STORY_VIP = (topo(250, 160) +
  f"<img src='data:image/png;base64,{b64(LOGO_BR)}' style='position:absolute;left:72px;top:360px;width:210px;filter:drop-shadow(0 12px 40px rgba(0,0,0,.6))'>"
  "<div class='m c' style='top:640px;font-size:31px'>quinta, 26.11, na Bally Club</div>"
  "<div class='t' style='top:688px;font-size:156px'>lista <span class='v'>vip.</span></div>"
  "<div class='m' style='top:870px;font-size:30px'>ressaca das provas, com a Baruc.</div>"
  "<div class='r' style='top:940px'></div>" + precos(986, 96, 220) +
  "<div class='m c' style='top:1486px;font-size:31px'>entra no grupo e coloca seu nome.</div>")

FEED_VIP = (topo(72, 150) +
  f"<img src='data:image/png;base64,{b64(LOGO_BR)}' style='position:absolute;right:66px;top:150px;width:220px;filter:drop-shadow(0 10px 30px rgba(0,0,0,.6))'>"
  "<div class='m c' style='top:430px;font-size:29px'>quinta, 26.11, na Bally Club</div>"
  "<div class='t' style='top:474px;font-size:140px'>lista <span class='v'>vip.</span></div>"
  "<div class='m' style='top:640px;font-size:27px'>ressaca das provas, com a Baruc.</div>"
  "<div class='r' style='top:700px'></div>" + precos(736, 84, 196) +
  "<div class='m c' style='top:1180px;font-size:28px'>link do grupo na bio.</div>")

PECAS = [  # saída, W, H, html, foto, foco, escurecimento por altura
 ('story_lista-vip_baruc.png', 1080, 1920, STORY_VIP, '216002663', (.5, .5), lambda y: .55 * (1 - sm((y - 200) / 420)) + .80 * sm((y - 620) / 520)),
 ('feed_lista-vip_baruc.png', 1080, 1350, FEED_VIP, '216002663', (.5, .5), lambda y: .45 * (1 - sm((y - 40) / 300)) + .80 * sm((y - 420) / 420)),
 ('story_ressaca-das-provas_baruc.png', 1080, 1920, STORY, '317621805', (.30, .5), lambda y: .55 * (1 - sm((y - 200) / 420)) + .82 * sm((y - 760) / 520)),
 ('feed_ressaca-das-provas_baruc.png', 1080, 1350, FEED, '317621805', (.30, .5), lambda y: .45 * (1 - sm((y - 40) / 300)) + .80 * sm((y - 440) / 420)),
]
with sync_playwright() as p:
    br = p.chromium.launch()
    for nome, W, H, html, foto, foco, esc in PECAS:
        pg = br.new_page(viewport={'width': W, 'height': H})
        pg.set_content(f"<style>{css(W, H)}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=P + '_t.png', omit_background=True); pg.close()
        bg = fundo(W, H, foto, foco, esc).convert('RGBA'); bg.alpha_composite(Image.open(P + '_t.png'))
        random.seed(5); n = Image.effect_noise((W, H), 22).convert('RGB'); out = Image.blend(bg.convert('RGB'), ImageChops.overlay(bg.convert('RGB'), n), .08)
        out.save(P + nome); os.remove(P + '_t.png'); print(nome)
    br.close()
