"""Story 1080x1920 do afterzin PRAS PROMOTERS: os 6 DJs em foto colorida sobre luz de pista (azul, magenta, vermelho),
atrações principais na frente, nomes embaixo e espaço pro sticker de link de cada promoter. Só Fraunces.
(sem citar o show nem o artista)
Uso: python3 afterzin_promoter_fotos.py <pasta fontes> <pasta fotos stock>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
A = R + '/afterzin-2011'; OUT = A + '/minimal'; E1 = R + '/edicao-01/fotos-djs/'; F = A + '/fotos/'
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (6, 6, 10), '#f1eef4', '#b9b4c4'
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
def coluna(f):      # máscara vertical a partir de f(y) em 0..1
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))

# nome, recorte, centro do rosto (fração da largura), altura da cabeça (fração da altura), x do rosto, topo da cabeça, altura da cabeça em px, espelha
TRAS = [('Mexikanno', E1 + 'mex.png', .38, .32, 116, 540, 182, False), ('Marquez', F + 'marquez.png', .50, .30, 316, 540, 182, False),
        ('Possani', E1 + 'possani.png', .45, .268, 770, 540, 182, False), ('Polão', F + 'polao.png', .38, .262, 978, 536, 182, False)]
# Kaio à esquerda (corpo virado pra fora) e Paganotti espelhado, com a mão pra direita: cada um abre pra um lado
FRENTE = [('Kaio Alves', F + 'kaio2.png', .66, .222, 408, 800, 262, False), ('Paganotti', F + 'paganotti.png', .72, .285, 652, 778, 292, True)]
FIM_GRUPO = (1120, 1338)      # o grupo todo some no escuro entre essas duas alturas
LUZ_E, LUZ_D, LUZ_T = (255, 52, 118), (64, 132, 255), (214, 170, 255)      # contraluz: vermelho/magenta à esquerda, azul à direita, lilás por cima

def figura(arq, cx, hf, x, topo, cab, espelha, brilho, sat, borda):
    im = Image.open(arq).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    if espelha: im = ImageOps.mirror(im); cx = 1 - cx
    if 'marquez' in arq or 'kaio2' in arq: im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.1)))   # halo do fundo claro
    sc = cab / (hf * im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    rgb = ImageEnhance.Color(im.convert('RGB')).enhance(sat); rgb = ImageEnhance.Contrast(rgb).enhance(1.08); rgb = ImageEnhance.Brightness(rgb).enhance(brilho)
    rgb = Image.blend(rgb, ImageChops.soft_light(rgb, Image.new('RGB', rgb.size, (96, 70, 190))), .30)     # puxa as sombras pro azul da pista
    a = im.getchannel('A')
    # contraluz colorida nas bordas (a luz vem de trás, como no fundo)
    d = borda; pad = ImageOps.expand(a, d * 2, 0)
    def faixa(dx, dy):
        e = ImageChops.subtract(pad, ImageChops.offset(pad, dx, dy)).filter(ImageFilter.GaussianBlur(d * .42))
        return e.crop((d * 2, d * 2, d * 2 + a.width, d * 2 + a.height))
    for cor, (dx, dy), forca in [(LUZ_E, (d, 0), .62), (LUZ_D, (-d, 0), .62), (LUZ_T, (0, d), .34)]:
        luz = ImageChops.screen(rgb, Image.new('RGB', rgb.size, cor)); rgb = Image.composite(luz, rgb, faixa(dx, dy).point(lambda v, f=forca: round(min(255, v * 1.25) * f)))
    fim = Image.linear_gradient('L').resize(im.size).point(lambda v: 255 if v < 170 else max(0, round(255 - (v - 170) * 3.2)))
    im = rgb.convert('RGBA'); im.putalpha(ImageChops.multiply(a, fim))
    return im, (round(x - cx * im.width), topo)

def cola(dst, im, pos): dst.alpha_composite(im, (max(0, pos[0]), pos[1]), (max(0, -pos[0]), 0))

def fundo():
    im = Image.open(f'{ST}/AdobeStock_216002663.jpeg').convert('RGB')      # pista com luz azul, magenta e vermelha
    alt = 1560; s = alt / im.height; im = im.resize((round(im.width * s), alt), Image.LANCZOS)
    x = round(im.width * .535 - W / 2); luz = im.crop((x, 0, x + W, alt)).filter(ImageFilter.GaussianBlur(5))
    luz = ImageEnhance.Color(luz).enhance(1.18); luz = ImageEnhance.Contrast(luz).enhance(1.10); luz = ImageEnhance.Brightness(luz).enhance(.92)
    bg = Image.new('RGB', (W, H), BASE); bg.paste(luz, (0, 40))
    # escurece em cima (logo e título) e some embaixo (nomes e link)
    m = coluna(lambda y: sm((y - 50) / 230) * (1 - .84 * (1 - sm((y - 250) / 420))) if y < 700 else 1 - sm((y - 1010) / 330))
    bg = Image.composite(bg, Image.new('RGB', (W, H), BASE), m)
    grp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for nome, arq, cx, hf, x, topo, cab, esp in TRAS:
        im, pos = figura(arq, cx, hf, x, topo, cab, esp, .84, .86, 5); cola(grp, im, pos)
    for nome, arq, cx, hf, x, topo, cab, esp in FRENTE:
        im, pos = figura(arq, cx, hf, x, topo, cab, esp, .95 if nome == 'Paganotti' else 1.04, .96, 7)
        sombra = Image.new('RGBA', im.size, (5, 3, 12, 255)); sombra.putalpha(im.getchannel('A').point(lambda v: round(v * .66)))
        cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cola(cam, sombra, pos)
        grp = Image.alpha_composite(grp, cam.filter(ImageFilter.GaussianBlur(24)))        # sombra atrás de quem está na frente: dá profundidade
        cola(grp, im, pos)
    y0, y1 = FIM_GRUPO; grp.putalpha(ImageChops.multiply(grp.getchannel('A'), coluna(lambda y: 1 - sm((y - y0) / (y1 - y0)))))
    bg.paste(grp, (0, 0), grp)
    # névoa colorida subindo do chão, na frente do grupo: amarra as fotos com a luz do fundo
    nev = luz.resize((W, 300)).filter(ImageFilter.GaussianBlur(70)); cam = Image.new('RGB', (W, H), (0, 0, 0)); cam.paste(nev, (0, 1010))
    forca = coluna(lambda y: .34 * sm((y - 1010) / 130) * (1 - sm((y - 1180) / 150)))
    return Image.composite(ImageChops.screen(bg, cam), bg, forca)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:440;color:{DEST};line-height:1;letter-spacing:-.012em;white-space:nowrap;font-variation-settings:"WONK" 0;text-shadow:0 2px 30px rgba(6,6,10,.6)}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum";text-shadow:0 1px 16px rgba(6,6,10,.75)}}"""
html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:250px;width:160px'>"
        f"<div class='m' style='left:auto;right:72px;top:268px;font-size:25px;color:{DEST}'>line-up</div>"
        f"<div class='t' style='left:64px;top:322px;font-size:152px;font-variation-settings:\"WONK\" 1'>afterzin.</div>"
        f"<div class='m' style='top:490px;font-size:30px;color:{DEST}'>sexta pra sábado, 21.11, a partir da 01h, na Bally Club.</div>"
        f"<div class='m' style='top:1338px;font-size:32px;color:{DEST}'>a line é pesada.</div>"
        f"<div class='t' style='top:1384px;font-size:88px'>Kaio Alves, Paganotti,</div>"
        f"<div class='t' style='top:1488px;font-size:47px;opacity:.82'>Mexikanno, Marquez, Polão e Possani.</div>"
        f"<div class='m' style='top:1578px;font-size:31px;color:{DEST}'>link de ingresso aqui.</div>")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
    pg.screenshot(path=OUT + '/_t.png', omit_background=True); br.close()
t = Image.open(OUT + '/_t.png'); bg = fundo(); bg.paste(t, (0, 0), t)
random.seed(13); n = Image.effect_noise(bg.size, 20).convert('RGB'); bg = Image.blend(bg, ImageChops.overlay(bg, n), .07)
bg.save(OUT + '/s7_story_promoter_fotos.png'); os.remove(OUT + '/_t.png'); print('s7_story_promoter_fotos')
