"""Special bday Cleber Davidson (quinta, 19.11): story 1080x1920 (com espaço pro link) e feed 1080x1350.
Fundo de pista em duotone lavanda (linha da quinta) e o Cleber em cor natural. Só Fraunces.
Uso: python3 special_bday_cleber.py <pasta fontes> <pasta fotos stock>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
P = R + '/quintas-bally/semanas/2026-11-19/'
LOGO = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
BASE, CLARO, DEST, MED = (9, 8, 12), (226, 216, 244), '#efe9f7', '#b6acc8'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
def coluna(W, H, f):
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))

def fundo(W, H, fim):
    im = Image.open(f'{ST}/AdobeStock_175742652.jpeg').convert('RGB')      # feixes de luz da pista
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = max(0, round(im.height * .40 - H / 2)); g = ImageOps.grayscale(im.crop((x, y, x + W, y + H)))
    g = ImageOps.autocontrast(g, cutoff=.5).point(lambda v: round(255 * min(1, 1.15 * (v / 255) ** 1.3))).filter(ImageFilter.GaussianBlur(4))
    duo = Image.merge('RGB', [g.point(lambda v, k=k, b=b: round(b + (k - b) * v / 255)) for k, b in zip(CLARO, BASE)])
    duo = Image.composite(Image.new('RGB', (W, H), BASE), duo, coluna(W, H, lambda y: .70 * (1 - sm((y - 60) / 360)) + .80 * sm((y - fim[0]) / (fim[1] - fim[0]))))
    return duo

def cleber(W, H, cab, cx, topo, fim):
    im = Image.open(P + 'fotos/cleber.png').convert('RGBA')
    sc = cab / 330; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)   # cabeça ~330 px na foto original
    rgb = ImageEnhance.Contrast(im.convert('RGB')).enhance(1.06); rgb = ImageEnhance.Color(rgb).enhance(1.05)
    lay = rgb.convert('RGBA'); pe = Image.linear_gradient('L').resize(im.size).point(lambda v: 255 if v < 200 else max(0, round(255 - (v - 200) * 4.5)))
    lay.putalpha(ImageChops.multiply(im.getchannel('A'), pe))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x0 = round(cx - .52 * im.width)       # rosto fica a ~52% da largura do recorte
    out.alpha_composite(lay, (max(0, x0), topo), (max(0, -x0), 0))
    out.putalpha(ImageChops.multiply(out.getchannel('A'), coluna(W, H, lambda y: 1 - sm((y - fim[0]) / (fim[1] - fim[0])))))
    sombra = Image.new('RGBA', (W, H), BASE + (255,)); sombra.putalpha(out.getchannel('A').point(lambda v: round(v * .55)).filter(ImageFilter.GaussianBlur(30)))
    return sombra, out

def css(W, H):
    return f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:430;color:{DEST};line-height:1.0;letter-spacing:-.012em;white-space:nowrap;font-variation-settings:"WONK" 0;text-shadow:0 2px 28px rgba(9,8,12,.75)}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum";text-shadow:0 1px 16px rgba(9,8,12,.85)}}
.c{{color:{DEST}}} .r{{position:absolute;left:72px;height:1px;width:130px;background:{MED};opacity:.55}}"""

def bloco(y, fs, fecho):
    return (f"<div class='m c' style='top:{y}px;font-size:{round(fs*.30)}px'>quinta, 19.11, na Bally Club</div>"
            f"<div class='t' style='top:{y+round(fs*.48)}px;font-size:{fs}px'>special bday<br>Cleber Davidson.</div>"
            f"<div class='r' style='top:{y+round(fs*2.62)}px'></div>"
            f"<div class='m' style='top:{y+round(fs*2.86)}px;font-size:{round(fs*.27)}px'>atração principal,</div>"
            f"<div class='t' style='top:{y+round(fs*3.22)}px;font-size:{round(fs*1.16)}px'>DJ Duarte</div>"
            f"<div class='t' style='top:{y+round(fs*4.62)}px;font-size:{round(fs*.44)}px;opacity:.86'>Oliver, Coiote, Moov,<br>Matheus Sanchez e Mexikanno.</div>"
            f"<div class='m c' style='top:{y+round(fs*5.86)}px;font-size:{round(fs*.29)}px'>{fecho}</div>")

PECAS = [  # saída, W, H, cabeça, x do rosto, topo, fim do Cleber, fim do fundo, y do texto, tamanho
 ('story_special-bday_cleber.png', 1080, 1920, 330, 770, 330, (1060, 1330), (1050, 1500), 1150, 86, 'ingressos no link.'),
 ('feed_special-bday_cleber.png', 1080, 1350, 250, 790, 120, (740, 960), (700, 1080), 690, 76, 'ingressos no link da bio.'),
]
with sync_playwright() as p:
    br = p.chromium.launch()
    for nome, W, H, cab, cx, topo, fimc, fimf, ty, fs, fecho in PECAS:
        pg = br.new_page(viewport={'width': W, 'height': H})
        topo_html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:{250 if H > 1500 else 72}px;width:160px'>"
                     f"<div class='m' style='left:auto;right:72px;top:{268 if H > 1500 else 90}px;font-size:25px'>quinta, por que não?</div>")
        pg.set_content(f"<style>{css(W, H)}</style>{topo_html}{bloco(ty, fs, fecho)}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
        pg.screenshot(path=P + '_t.png', omit_background=True); pg.close()
        bg = fundo(W, H, fimf).convert('RGBA'); sombra, fig = cleber(W, H, cab, cx, topo, fimc)
        bg.alpha_composite(sombra); bg.alpha_composite(fig); bg.alpha_composite(Image.open(P + '_t.png'))
        random.seed(7); n = Image.effect_noise((W, H), 20).convert('RGB'); out = Image.blend(bg.convert('RGB'), ImageChops.overlay(bg.convert('RGB'), n), .06)
        out.save(P + nome); os.remove(P + '_t.png'); print(nome)
    br.close()
