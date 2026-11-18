"""Stories 1080x1920 pra soltar com sticker de LINK de ingressos (o texto termina antes da área do sticker).
  - quinta 19.11: special bday Cleber Davidson (lavanda), DJ Duarte em destaque
  - sexta 21.11: afterzin, ingressos (grafite)
Só Fraunces (itálico nos títulos, romano no apoio), caixa baixa com vírgula e ponto.
Uso: python3 stories_link.py <pasta fontes> <pasta fotos stock>   (fotos do Adobe Stock ficam FORA do repositório)"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
PAL = {  # base, tom claro do duotone, destaque, médio, logo
 'lavanda': ((8, 8, 10), (232, 224, 246), '#ece6f4', '#b3a9c4', R + '/assets/logo/lavanda/logo-why-not-lavanda.png'),
 'grafite': ((8, 9, 10), (236, 236, 236), '#ececec', '#a9adb1', R + '/assets/logo/grafite/logo-why-not-grafite.png'),
}

def fundo(foto, pal, foco, zoom, brilho, base_em):
    base, claro = PAL[pal][:2]
    im = Image.open(f'{ST}/AdobeStock_{foto}.jpeg').convert('RGB')
    s = max(W / im.width, H / im.height) * zoom; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(foco[0] * im.width - W / 2)), im.width - W); y = min(max(0, round(foco[1] * im.height - H / 2)), im.height - H)
    g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), cutoff=.5).point(lambda v: round(255 * min(1, brilho * (v / 255) ** 1.28)))
    duo = Image.merge('RGB', [g.point(lambda v, k=k, b=b: round(b + (k - b) * v / 255)) for k, b in zip(claro, base)])
    m = Image.linear_gradient('L').resize((W, H)).point(lambda v: 0 if v < 255 * base_em else min(255, round((v - 255 * base_em) * 2.6)))
    duo = Image.composite(Image.new('RGB', (W, H), base), duo, m)
    t = ImageOps.flip(Image.linear_gradient('L')).resize((W, H)).point(lambda v: max(0, round((v - 150) * 1.5)))
    return Image.composite(Image.new('RGB', (W, H), base), duo, t)

def grao(im, seed=11, f=.13):
    random.seed(seed); n = Image.effect_noise(im.size, 24).convert('RGB'); return Image.blend(im, ImageChops.overlay(im, n), f)

def css(pal):
    _, _, dest, med, _ = PAL[pal]
    return f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:420;color:{dest};line-height:1.02;letter-spacing:-.01em;white-space:nowrap;font-variation-settings:"WONK" 0}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{med};letter-spacing:.012em;white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;font-feature-settings:"lnum"}}
.t,.m{{text-shadow:0 0 26px rgba(8,8,10,.85),0 1px 5px rgba(8,8,10,.7)}} .c{{color:{dest}}} .r{{position:absolute;left:72px;height:1px;width:130px;background:{med};opacity:.55}}"""

def topo(pal, canto):
    return (f"<img src='data:image/png;base64,{b64(PAL[pal][4])}' style='position:absolute;left:72px;top:250px;width:160px'>"
            f"<div class='m' style='left:auto;right:72px;top:268px;font-size:25px'>{canto}</div>")

QUINTA = ("<div style='position:absolute;left:-260px;top:700px;width:1250px;height:520px;background:radial-gradient(ellipse 50% 50% at 42% 50%,rgba(8,8,10,.86),rgba(8,8,10,.5) 55%,transparent 72%)'></div>" +   # véu atrás do texto, a foto ali é cheia de luzinhas
  topo('lavanda', 'quinta, por que não?') +
  "<div class='m c' style='top:872px;font-size:30px'>quinta, 19.11, na Bally Club</div>"
  "<div class='t' style='top:920px;font-size:104px'>special bday<br>Cleber Davidson.</div>"
  "<div class='r' style='top:1170px'></div>"
  "<div class='m' style='top:1202px;font-size:27px'>no som,</div>"
  "<div class='t' style='top:1238px;font-size:124px'>DJ Duarte</div>"
  "<div class='m c' style='top:1392px;font-size:33px;opacity:.9'>Coiote, Moov, Matheus Sanchez e Mexikanno.</div>"
  "<div class='r' style='top:1470px'></div>"
  "<div class='m' style='top:1498px;font-size:28px'>ingressos no link.</div>")

SEXTA = (topo('grafite', 'afterzin') +
  "<div class='m c' style='top:1040px;font-size:30px'>afterzin why not?, sexta pra sábado, 21.11</div>"
  "<div class='t' style='top:1088px;font-size:124px'>garante<br>o seu.</div>"
  "<div class='r' style='top:1384px'></div>"
  "<div class='m' style='top:1412px;font-size:28px'>a partir da 01h, na Bally Club.</div>"
  "<div class='m' style='top:1452px;font-size:28px'>ingressos no link.</div>")

# versões pras PROMOTERS postarem no perfil delas, com o link de cada uma
QUINTA_PROMO = QUINTA.replace('ingressos no link.', 'ingressos comigo, no link.')

LINE = [('01:00', 'Mexikanno'), ('02:00', 'Marquez'), ('03:00', 'Paganotti'), ('04:00', 'Polão'), ('05:00', 'Kaio Alves'), ('06:00', 'Possani')]
DESTAQUE = {'Paganotti', 'Kaio Alves'}
def grade(y, fs=74, hs=33, passo=98):
    h, yy = '', y
    for hora, nome in LINE:
        d = nome in DESTAQUE; f = round(fs * (1.34 if d else 1))
        h += (f"<div class='m{' c' if d else ''}' style='top:{yy+round(f*.40)}px;font-size:{hs}px;font-weight:500;font-feature-settings:\"tnum\",\"lnum\"'>{hora}</div>"
              f"<div class='t' style='left:236px;top:{yy}px;font-size:{f}px;{'' if d else 'opacity:.78'}'>{nome}</div>")
        yy += round(passo * (1.26 if d else 1))
    return h, yy
_g, _fim = grade(752)
SEXTA_PROMO = (topo('grafite', 'afterzin') +
  "<div class='m c' style='top:690px;font-size:30px'>afterzin why not?, sexta pra sábado, 21.11</div>" + _g +
  f"<div class='r' style='top:{_fim+22}px'></div>"
  f"<div class='m' style='top:{_fim+50}px;font-size:28px'>a partir da 01h, na Bally Club.</div>"
  f"<div class='m' style='top:{_fim+90}px;font-size:28px'>ingressos comigo, no link.</div>")

PECAS = [  # saída, paleta, foto, foco, zoom, brilho, base_em, html
 (R + '/quintas-bally/semanas/2026-11-19/story_special-bday_link.png', 'lavanda', '1885683718', (.5, .56), 1.0, 1.75, .37, QUINTA),
 (R + '/quintas-bally/semanas/2026-11-19/story_special-bday_promoter.png', 'lavanda', '1885683718', (.5, .56), 1.0, 1.75, .37, QUINTA_PROMO),
 (R + '/afterzin-2011/minimal/s6_story_promoter_link.png', 'grafite', '175742652', (.5, .5), 1.0, 1.05, .28, SEXTA_PROMO),
 (R + '/afterzin-2011/minimal/s5_story_ingressos_link.png', 'grafite', '354468011', (.56, .5), 1.0, 1.3, .44, SEXTA),
]
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for out, pal, foto, foco, zoom, bri, be, html in PECAS:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        pg.set_content(f"<style>{css(pal)}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
        pg.screenshot(path=out + '.t.png', omit_background=True); t = Image.open(out + '.t.png')
        bg = fundo(foto, pal, foco, zoom, bri, be); bg.paste(t, (0, 0), t); grao(bg).save(out); os.remove(out + '.t.png'); print(os.path.basename(out))
    br.close()
