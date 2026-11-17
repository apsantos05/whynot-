"""afterzin why not? — campanha na linha MINIMALISTA (grafite). Ideia: o relógio. 00:00 o show acaba, 01:00 a noite continua.
2 feeds 4:5 (2x) + 3 stories 1080x1920. Sem nomes de DJ.
Uso: python3 minimal_afterzin.py <pasta fontes> <pasta fotos stock>   (fotos do Adobe Stock ficam FORA do repositório)"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
OUT = os.environ.get('OUT', R + '/afterzin-2011/minimal'); os.makedirs(OUT, exist_ok=True)
VAR = sys.argv[3] if len(sys.argv) > 3 else 'fraunces'   # fonte de apoio: mono | fraunces | archivo | shoulders
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ececec', '#a9adb1'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

def fundo(foto, W, H, foco=(.5, .5), zoom=1.0, brilho=1.0, base_em=.40):
    im = Image.open(f'{ST}/AdobeStock_{foto}.jpeg').convert('RGB')
    s = max(W / im.width, H / im.height) * zoom; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(foco[0] * im.width - W / 2)), im.width - W); y = min(max(0, round(foco[1] * im.height - H / 2)), im.height - H)
    g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), cutoff=.5)
    g = g.point(lambda v: round(255 * min(1, brilho * (v / 255) ** 1.3)))
    duo = Image.merge('RGB', [g.point(lambda v, b=b: round(b + (236 - b) * v / 255)) for b in BASE])
    m = Image.linear_gradient('L').resize((W, H)).point(lambda v: 0 if v < 255 * base_em else min(255, round((v - 255 * base_em) * 2.4)))
    duo = Image.composite(Image.new('RGB', (W, H), BASE), duo, m)
    t = ImageOps.flip(Image.linear_gradient('L')).resize((W, H)).point(lambda v: max(0, round((v - 150) * 1.5)))
    return Image.composite(Image.new('RGB', (W, H), BASE), duo, t)

def grao(im, seed=13, f=.14):
    random.seed(seed); n = Image.effect_noise(im.size, 24).convert('RGB'); return Image.blend(im, ImageChops.overlay(im, n), f)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1.02;letter-spacing:-.01em;white-space:nowrap}}
.m{{position:absolute;left:72px;font-family:SM;font-weight:700;color:{MED};letter-spacing:.26em;text-transform:uppercase;white-space:nowrap}}
.h{{position:absolute;left:72px;font-family:SM;font-weight:700;letter-spacing:.14em;white-space:nowrap}}
.r{{position:absolute;left:72px;height:1px;width:130px;background:{MED};opacity:.55}}
.d{{color:{MED};opacity:.78}}"""
N = FD + '/novas/node_modules/'
ff = lambda nome, arq, extra='': f"@font-face{{font-family:{nome};font-weight:100 900;{extra}src:url(data:font/woff2;base64,{b64(arq)})}}"
SEC = {
 'mono': '',
 'fraunces': ff('FrR', FD + '/fv/files/fraunces-latin-full-normal.woff2') +
   ".m{font-family:FrR;font-weight:400;letter-spacing:.012em;text-transform:none;transform:scale(1.42);transform-origin:left top;font-variation-settings:\"opsz\" 14,\"WONK\" 0}"
   ".h{font-family:FrR;font-weight:500;letter-spacing:.02em;font-feature-settings:\"tnum\",\"lnum\";transform:scale(1.14);transform-origin:left top}",
 'archivo': ff('Arc', N + '@fontsource-variable/archivo/files/archivo-latin-standard-normal.woff2', 'font-stretch:62% 125%;') +
   ".m{font-family:Arc;font-weight:600;font-stretch:125%;letter-spacing:.15em;transform:scale(.92);transform-origin:left top}"
   ".h{font-family:Arc;font-weight:700;font-stretch:125%;letter-spacing:.04em;transform:scale(.96);transform-origin:left top}",
 'shoulders': ff('BS', N + '@fontsource/big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2') +
   ".m{font-family:BS;font-weight:800;letter-spacing:.13em;transform:scale(1.42);transform-origin:left top}"
   ".h{font-family:BS;font-weight:800;letter-spacing:.07em;transform:scale(1.34);transform-origin:left top}",
}
CSS += SEC[VAR] + ".cr{transform-origin:right top !important}"
def topo(H, canto='afterzin'):
    y = 250 if H == 1920 else 70
    return (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:{y}px;width:{160 if H==1920 else 150}px'>"
            f"<div class='m cr' style='left:auto;right:72px;top:{y+26}px;font-size:{17 if H==1920 else 16}px'>{canto}</div>")

def relogio(y, fs, hs, gap, info, extra='', t1='o show acaba.', t2='a noite continua.'):
    """o relógio: 00:00 apagado / 01:00 aceso"""
    a = y; b = a + hs + 14; c = b + fs + gap; d = c + hs + 14; e = d + fs + 44
    return (f"<div class='h d' style='top:{a}px;font-size:{hs}px'>00:00</div><div class='t d' style='top:{b}px;font-size:{fs}px'>{t1}</div>"
            f"<div class='h' style='top:{c}px;font-size:{hs}px;color:{DEST}'>01:00</div><div class='t' style='top:{d}px;font-size:{fs}px'>{t2}</div>"
            f"<div class='r' style='top:{e}px'></div>" + ''.join(f"<div class='m' style='top:{e+28+i*34}px;font-size:{round(hs*.62)}px'>{l}</div>" for i, l in enumerate(info)) + extra)

def bloco(base_y, fs, kicker, titulo, info, ks):
    n = titulo.count('<br>') + 1; ty = base_y - n * fs * 1.02
    return (f"<div class='m' style='top:{ty-46:.0f}px;font-size:{ks}px;color:{DEST}'>{kicker}</div><div class='t' style='top:{ty:.0f}px;font-size:{fs}px'>{titulo}</div>"
            f"<div class='r' style='top:{base_y+34}px'></div>" + ''.join(f"<div class='m' style='top:{base_y+62+i*34}px;font-size:{ks-2}px'>{l}</div>" for i, l in enumerate(info)))

LINE = [('01:00', 'Mexikanno'), ('02:00', 'Marquez'), ('03:00', 'Paganotti'), ('04:00', 'Polão'), ('05:00', 'Kaio Alves'), ('06:00', 'Possani')]
DESTAQUE = {'Paganotti', 'Kaio Alves'}     # atrações principais: nome maior e mais claro
def grade(y, fs, hs, passo, info, kicker='line-up e horários'):
    """grade de horários: hora + nome (itálico), no mesmo relógio da campanha; destaques em corpo maior"""
    h = f"<div class='m' style='top:{y}px;font-size:{round(hs*.72)}px;color:{DEST}'>{kicker}</div>"; yy = y + 58
    for hora, nome in LINE:
        d = nome in DESTAQUE; f = round(fs * (1.34 if d else 1)); p_ = round(passo * (1.26 if d else 1))
        h += (f"<div class='h' style='top:{yy+round(f*.36)}px;font-size:{hs}px;color:{DEST if d else MED}'>{hora}</div>"
              f"<div class='t' style='left:{72+round(hs*5.6)}px;top:{yy}px;font-size:{f}px;font-variation-settings:\"WONK\" 0;{'' if d else 'opacity:.78'}'>{nome}</div>")
        yy += p_
    e = yy + 18
    return h + f"<div class='r' style='top:{e}px'></div>" + ''.join(f"<div class='m' style='top:{e+28+i*34}px;font-size:{round(hs*.66)}px'>{l}</div>" for i, l in enumerate(info))

PECAS = [  # nome, W, H, foto, foco, zoom, brilho, base_em, html
 ('1_feed_anuncio', 1080, 1350, '317621805', (.25, .5), 1.0, 1.1, .40,
  topo(1350) + relogio(838, 88, 27, 30, ['afterzin why not?, sexta pra sábado, 21.11.', 'na Bally Club.'])),
 ('1b_feed_anuncio_sem-show', 1080, 1350, '317621805', (.25, .5), 1.0, 1.1, .40,
  topo(1350) + relogio(838, 88, 27, 30, ['afterzin why not?, sexta pra sábado, 21.11.', 'na Bally Club.'], t1='é cedo.')),
 ('2_feed_e-hoje', 1080, 1350, '587737046', (.62, .5), 1.0, 1.0, .40,
  topo(1350, 'é hoje') + bloco(1168, 96, 'afterzin why not?, hoje', 'a noite<br>continua.', ['a partir da 01h, na Bally Club.', 'ingressos no site da Bally ou na portaria.'], 19)),
 ('s1_story_teaser', 1080, 1920, '216002663', (.5, .5), 1.0, 1.1, .40,
  topo(1920) + bloco(1490, 112, 'sexta,', 'meia-noite<br>é cedo.', ['afterzin why not?, a partir da 01h, na Bally Club.'], 21)),
 ('s2_story_info', 1080, 1920, '317621805', (.2, .5), 1.0, 1.1, .40,
  topo(1920) + relogio(1118, 100, 30, 34, ['afterzin why not?, sexta pra sábado, 21.11, na Bally Club.', 'ingressos no site da Bally ou na portaria.'])),
 ('3_feed_line', 1080, 1350, '175742652', (.5, .5), 1.0, 1.05, .26,
  topo(1350) + grade(556, 66, 26, 88, ['sexta pra sábado, 21.11, na Bally Club, até as 07h.', 'ingressos no site da Bally ou na portaria.'])),
 ('s4_story_line', 1080, 1920, '175742652', (.5, .5), 1.0, 1.05, .30,
  topo(1920) + grade(800, 74, 29, 98, ['sexta pra sábado, 21.11, na Bally Club, até as 07h.', 'ingressos no site da Bally ou na portaria.'])),
 ('s3_story_e-hoje', 1080, 1920, '587737046', (.72, .5), 1.0, 1.0, .40,
  topo(1920, 'é hoje') + bloco(1490, 108, 'afterzin why not?, hoje', 'saiu do show,<br>cola na bally.', ['a partir da 01h. ingressos na portaria.'], 21)),
]
with sync_playwright() as p:
    br = p.chromium.launch()
    for nome, W, H, foto, foco, zoom, bri, be, html in PECAS:
        if os.environ.get('ONLY') and nome not in os.environ['ONLY'].split(','): continue
        sf = 2 if H == 1350 else 1
        pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=sf)
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250); pg.screenshot(path=OUT + '/_t.png', omit_background=True); pg.close()
        t = Image.open(OUT + '/_t.png'); bg = fundo(foto, W * sf, H * sf, foco, zoom, bri, be); bg.paste(t, (0, 0), t)
        grao(bg).save(f'{OUT}/{nome}.png'); print(nome)
    br.close()
os.path.exists(OUT + '/_t.png') and os.remove(OUT + '/_t.png')
