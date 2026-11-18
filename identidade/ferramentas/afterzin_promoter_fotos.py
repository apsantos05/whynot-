"""Story 1080x1920 do afterzin PRAS PROMOTERS: os 6 DJs em foto colorida, atrações principais na frente,
nomes embaixo e espaço pro sticker de link de cada promoter. Só Fraunces. (sem citar o show nem o artista)
Uso: python3 afterzin_promoter_fotos.py <pasta fontes> <pasta fotos stock>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
A = R + '/afterzin-2011'; OUT = A + '/minimal'; E1 = R + '/edicao-01/fotos-djs/'; F = A + '/fotos/'
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ececec', '#a9adb1'
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))

# nome, recorte, centro do rosto (fração da largura), altura da cabeça (fração da altura), x do rosto, topo da cabeça, altura da cabeça em px, espelha
TRAS = [('Mexikanno', E1 + 'mex.png', .38, .32, 128, 572, 178, False), ('Marquez', F + 'marquez.png', .50, .30, 338, 560, 180, False),
        ('Polão', F + 'polao.png', .38, .262, 792, 560, 184, False), ('Possani', E1 + 'possani.png', .45, .268, 978, 574, 176, False)]
FRENTE = [('Kaio Alves', F + 'kaio.png', .51, .45, 672, 770, 236, False), ('Paganotti', F + 'paganotti.png', .72, .285, 432, 778, 250, False)]
FIM_GRUPO = (1120, 1330)      # o grupo todo some no preto entre essas duas alturas

def figura(arq, cx, hf, x, topo, cab, espelha, brilho, sat):
    im = Image.open(arq).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    if espelha: im = ImageOps.mirror(im); cx = 1 - cx
    if 'marquez' in arq: im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.2)))   # halo do fundo claro
    sc = cab / (hf * im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    rgb = ImageEnhance.Color(im.convert('RGB')).enhance(sat); rgb = ImageEnhance.Contrast(rgb).enhance(1.06); rgb = ImageEnhance.Brightness(rgb).enhance(brilho)
    a = im.getchannel('A'); fim = Image.linear_gradient('L').resize(im.size).point(lambda v: 255 if v < 165 else max(0, round(255 - (v - 165) * 3.2)))
    im = rgb.convert('RGBA'); im.putalpha(ImageChops.multiply(a, fim))
    return im, (round(x - cx * im.width), topo)

def fundo():
    im = Image.open(f'{ST}/AdobeStock_175742652.jpeg').convert('RGB')      # os mesmos feixes de luz da arte de line
    s = max(W / im.width, 1250 / im.height) * 1.15; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, 0, x + W, 1250))), cutoff=.5).point(lambda v: round(255 * .62 * (v / 255) ** 1.35))
    duo = Image.merge('RGB', [g.point(lambda v, b=b: round(b + (236 - b) * v / 255)) for b in BASE]).filter(ImageFilter.GaussianBlur(3))
    bg = Image.new('RGB', (W, H), BASE); bg.paste(duo, (0, 150))
    borda = Image.new('L', (W, H), 255)      # some em cima (logo) e embaixo (texto)
    borda.paste(Image.linear_gradient('L').resize((W, 330)), (0, 150)); borda.paste(0, (0, 0, W, 150))
    borda.paste(ImageOps.flip(Image.linear_gradient('L')).resize((W, 420)), (0, 980)); borda.paste(0, (0, 1400, W, H))
    bg = Image.composite(bg, Image.new('RGB', (W, H), BASE), borda)
    grp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for nome, arq, cx, hf, x, topo, cab, esp in TRAS:
        im, pos = figura(arq, cx, hf, x, topo, cab, esp, .80, .82); grp.alpha_composite(im, (max(0, pos[0]), pos[1]), (max(0, -pos[0]), 0))
    for nome, arq, cx, hf, x, topo, cab, esp in FRENTE:
        im, pos = figura(arq, cx, hf, x, topo, cab, esp, .97 if nome == 'Paganotti' else 1.06, .92)
        sombra = Image.new('RGBA', im.size, (4, 4, 5, 255)); sombra.putalpha(im.getchannel('A').point(lambda v: round(v * .62)))
        cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.alpha_composite(sombra, (max(0, pos[0]), pos[1]), (max(0, -pos[0]), 0))
        grp = Image.alpha_composite(grp, cam.filter(ImageFilter.GaussianBlur(22)))        # sombra atrás de quem está na frente: dá profundidade
        grp.alpha_composite(im, (max(0, pos[0]), pos[1]), (max(0, -pos[0]), 0))
    y0, y1 = FIM_GRUPO; col = Image.new('L', (1, H)); col.putdata([round(255 * (1 - sm((y - y0) / (y1 - y0)))) for y in range(H)])
    grp.putalpha(ImageChops.multiply(grp.getchannel('A'), col.resize((W, H)))); bg.paste(grp, (0, 0), grp)
    return bg

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1;letter-spacing:-.012em;white-space:nowrap;font-variation-settings:"WONK" 0}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum"}}
.r{{position:absolute;left:72px;height:1px;width:130px;background:{MED};opacity:.55}}"""
html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:250px;width:160px'>"
        f"<div class='m' style='left:auto;right:72px;top:268px;font-size:25px'>line-up</div>"
        f"<div class='t' style='left:64px;top:326px;font-size:150px;font-variation-settings:\"WONK\" 1'>afterzin.</div>"
        f"<div class='m' style='top:494px;font-size:30px;color:{DEST}'>sexta pra sábado, 21.11, a partir da 01h, na Bally Club.</div>"
        f"<div class='t' style='top:1322px;font-size:88px'>Paganotti, Kaio Alves,</div>"
        f"<div class='t' style='top:1428px;font-size:47px;opacity:.8'>Mexikanno, Marquez, Polão e Possani.</div>"
        f"<div class='r' style='top:1512px'></div>"
        f"<div class='m' style='top:1538px;font-size:28px'>ingressos comigo, no link.</div>")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
    pg.screenshot(path=OUT + '/_t.png', omit_background=True); br.close()
t = Image.open(OUT + '/_t.png'); bg = fundo(); bg.paste(t, (0, 0), t)
random.seed(13); n = Image.effect_noise(bg.size, 22).convert('RGB'); bg = Image.blend(bg, ImageChops.overlay(bg, n), .08)
bg.save(OUT + '/s7_story_promoter_fotos.png'); os.remove(OUT + '/_t.png'); print('s7_story_promoter_fotos')
