"""Camadas da arte das PROMOTERS do afterzin pra montar no Photoshop (1080x1920):
fundo P&B (feixes de luz), cada DJ em cor natural numa camada própria já posicionada, sombra e textos.
Gera também uma prévia. A montagem no Photoshop é feita pelo ferramentas/ps_monta_promoter.jsx.
Uso: python3 afterzin_promoter_camadas.py <pasta fontes> <pasta fotos stock> <pasta saída>"""
import os, sys, base64
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
E1 = R + '/edicao-01/fotos-djs/'; F = R + '/afterzin-2011/fotos/'
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ededed', '#a9adb1'
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
def coluna(f):
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))

# nome, arquivo da camada, recorte, centro do rosto (fração da largura), altura da cabeça (fração da altura), x do rosto, topo da cabeça, altura da cabeça, espelha, brilho
DJS = [('Mexikanno', 'dj_mexikanno', E1 + 'mex.png', .38, .32, 112, 598, 190, False, .9),
       ('Marquez', 'dj_marquez', F + 'marquez.png', .50, .30, 318, 590, 190, False, .9),
       ('Possani', 'dj_possani', E1 + 'possani.png', .45, .268, 768, 590, 190, False, .9),
       ('Polão', 'dj_polao', F + 'polao.png', .38, .262, 972, 586, 190, False, .9),
       ('Kaio Alves', 'dj_kaio-alves', F + 'kaio2.png', .66, .222, 392, 842, 282, False, 1.02),
       ('Paganotti', 'dj_paganotti', F + 'paganotti.png', .72, .285, 676, 806, 330, True, 1.0)]
FIM = (1180, 1360)        # cada DJ some no preto entre essas alturas

def figura(arq, cx, hf, x, topo, cab, espelha, brilho):
    im = Image.open(arq).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    if espelha: im = ImageOps.mirror(im); cx = 1 - cx
    if 'marquez' in arq or 'kaio2' in arq: im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.0)))
    sc = cab / (hf * im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    rgb = ImageEnhance.Contrast(im.convert('RGB')).enhance(1.05); rgb = ImageEnhance.Brightness(rgb).enhance(brilho)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x0 = round(x - cx * im.width)
    lay = rgb.convert('RGBA'); pe = Image.linear_gradient('L').resize(im.size).point(lambda v: 255 if v < 175 else max(0, round(255 - (v - 175) * 3.2))); lay.putalpha(ImageChops.multiply(im.getchannel('A'), pe));   # some no próprio rodapé do recorte
    out.alpha_composite(lay, (max(0, x0), topo), (max(0, -x0), 0))
    y0, y1 = FIM; out.putalpha(ImageChops.multiply(out.getchannel('A'), coluna(lambda y: 1 - sm((y - y0) / (y1 - y0)))))
    return out

def fundo():
    im = Image.open(f'{ST}/AdobeStock_175742652.jpeg').convert('RGB')        # os feixes de luz da arte de line, em P&B
    alt = 1180; s = alt / im.height * 1.0; im = im.resize((round(im.width * s), alt), Image.LANCZOS)
    x = round(im.width * .5 - W / 2); g = ImageOps.grayscale(im.crop((x, 0, x + W, alt)))
    g = ImageOps.autocontrast(g, cutoff=.4).point(lambda v: round(255 * min(1, 1.05 * (v / 255) ** 1.25)))
    duo = Image.merge('RGB', [g.point(lambda v, b=b: round(b + (232 - b) * v / 255)) for b in BASE])
    bg = Image.new('RGB', (W, H), BASE); bg.paste(duo, (0, 300))
    m = coluna(lambda y: sm((y - 300) / 260) * (1 - sm((y - 1150) / 300)))
    bg = Image.composite(bg, Image.new('RGB', (W, H), BASE), m)
    v = Image.new('L', (W, H), 0); v.paste(255, (0, 0, W, H))                  # vinheta nas laterais
    lado = Image.linear_gradient('L').rotate(90, expand=True).resize((W, H)); lado = ImageChops.lighter(lado, ImageOps.mirror(lado)).point(lambda p: round(150 * sm((p - 150) / 105)))
    return Image.composite(Image.new('RGB', (W, H), BASE), bg, lado)

def sombra(camadas):
    a = Image.new('L', (W, H), 0)
    for c in camadas: a = ImageChops.lighter(a, c.getchannel('A'))
    s = Image.new('RGBA', (W, H), (0, 0, 0, 255)); s.putalpha(a.point(lambda v: round(v * .7)).filter(ImageFilter.GaussianBlur(26)))
    return s

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:440;color:{DEST};line-height:1;letter-spacing:-.012em;white-space:nowrap;font-variation-settings:"WONK" 0}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum"}}
.r{{position:absolute;left:72px;height:1px;width:130px;background:{MED};opacity:.55}}"""
TXT = {
 'txt_topo': f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:250px;width:160px'>"
             f"<div class='m' style='left:auto;right:72px;top:268px;font-size:25px'>line-up</div>",
 'txt_titulo': "<div class='t' style='left:64px;top:318px;font-size:156px;font-variation-settings:\"WONK\" 1'>afterzin.</div>"
               f"<div class='m' style='top:490px;font-size:30px;color:{DEST}'>sexta pra sábado, 21.11, a partir da 01h, na Bally Club.</div>",
 'txt_nomes': f"<div class='m' style='top:1374px;font-size:32px;color:{DEST}'>a line é pesada.</div>"
              "<div class='t' style='top:1420px;font-size:92px'>Kaio Alves, Paganotti,</div>"
              "<div class='t' style='top:1528px;font-size:48px;opacity:.8'>Mexikanno, Marquez, Polão e Possani.</div>",
 'txt_ingresso': "<div class='r' style='top:1612px'></div>"
                 f"<div class='m' style='top:1636px;font-size:31px;color:{DEST}'>link de ingresso aqui.</div>",
}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for nome, h in TXT.items():
        pg.set_content(f"<style>{CSS}</style>{h}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{OUT}/{nome}.png', omit_background=True)
    br.close()
bg = fundo(); bg.save(OUT + '/fundo_pb.png')
cams = {}
for nome, arq_out, arq, cx, hf, x, topo, cab, esp, bri in DJS:
    cams[arq_out] = figura(arq, cx, hf, x, topo, cab, esp, bri); cams[arq_out].save(f'{OUT}/{arq_out}.png')
sombra([cams['dj_kaio-alves'], cams['dj_paganotti']]).save(OUT + '/sombra_frente.png')
# prévia na mesma ordem das camadas do PSD
pv = bg.convert('RGBA')
for n in ['dj_mexikanno', 'dj_marquez', 'dj_possani', 'dj_polao', 'sombra_frente', 'dj_kaio-alves', 'dj_paganotti', 'txt_topo', 'txt_titulo', 'txt_nomes', 'txt_ingresso']:
    pv.alpha_composite(Image.open(f'{OUT}/{n}.png').convert('RGBA'))
pv.convert('RGB').save(OUT + '/_previa.jpg', quality=92); print('ok')
