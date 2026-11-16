"""Banner do site da Bally COM FOTOS dos DJs (padrão da Bally) — afterzin why not? — 1024x600 + @2x.
Uso: python3 afterzin_site_fotos.py <pasta fontes>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageDraw
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
A = R + '/afterzin-2011'; OUT = A + '/minimal'; E1 = R + '/edicao-01/fotos-djs/'; F = A + '/fotos/'
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ececec', '#a9adb1'
W, H = 1024, 600
# nome, hora, recorte, centro do rosto (fração da largura), altura da cabeça (fração da altura), destaque
DJS = [('Mexikanno', '01h', E1 + 'mex.png', .38, .32, False), ('Marquez', '02h', F + 'marquez.png', .50, .30, False),
       ('Paganotti', '03h', F + 'paganotti.png', .72, .285, True), ('Kaio Alves', '05h', F + 'kaio.png', .51, .45, True),
       ('Polão', '04h', F + 'polao.png', .38, .262, False), ('Possani', '06h', E1 + 'possani.png', .45, .268, False)]
XS = [512 + (k - 2.5) * 158 for k in range(6)]
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

def fundo(sf):
    w, h = W * sf, H * sf
    bg = Image.new('RGB', (w, h), BASE)
    glow = Image.new('L', (w, h), 0); ImageDraw.Draw(glow).ellipse((w * .12, h * .02, w * .88, h * .86), fill=70)
    from PIL import ImageFilter
    glow = glow.filter(ImageFilter.GaussianBlur(90 * sf)); bg = Image.composite(Image.new('RGB', (w, h), (44, 46, 50)), bg, glow)
    ordem = [i for i, d in enumerate(DJS) if not d[5]] + [i for i, d in enumerate(DJS) if d[5]]
    for i in ordem:
        nome, hora, arq, cx, hf, dest = DJS[i]
        im = Image.open(arq).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
        if 'marquez' in arq:   # fundo claro deixou um halo no cabelo: aperta a máscara
            from PIL import ImageFilter as _F
            im.putalpha(im.getchannel('A').filter(_F.MinFilter(7)).filter(_F.GaussianBlur(1.2)))
        head = (112 if dest else 88) * sf; sc = head / (hf * im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        a = im.getchannel('A')
        fim = Image.linear_gradient('L').resize(im.size).point(lambda v: 255 if v < 150 else max(0, round(255 - (v - 150) * 2.6)))   # some cada foto no próprio rodapé
        a = ImageChops.multiply(a, fim); g = ImageOps.autocontrast(ImageOps.grayscale(im.convert('RGB')), cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.12)
        if not dest: g = g.point(lambda v: round(v * .86))
        rgb = Image.merge('RGB', [g.point(lambda v, b=b: round(b + (236 - b) * v / 255)) for b in BASE])
        bg.paste(rgb, (round(XS[i] * sf - cx * im.width), (138 if dest else 162) * sf), a)
    m = Image.linear_gradient('L').resize((w, h)).point(lambda v: round(255 * (lambda t: t * t * (3 - 2 * t))(min(1, max(0, (v / 255 - .47) / .24)))))
    return Image.composite(Image.new('RGB', (w, h), BASE), bg, m)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1;letter-spacing:-.01em;white-space:nowrap;font-variation-settings:"WONK" 0}}
.m{{position:absolute;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.01em}}
.c{{transform:translateX(-50%);text-align:center}}"""
html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:44px;top:36px;width:108px'>"
        f"<div class='t' style='right:44px;top:24px;font-size:56px;font-variation-settings:\"WONK\" 1'>afterzin.</div>"
        f"<div class='m' style='right:44px;top:88px;font-size:15px;color:{DEST}'>sexta pra sábado, 21.11, a partir da 01h, na Bally Club</div>")
for (nome, hora, _, _, _, dest), x in zip(DJS, XS):
    html += (f"<div class='t c' style='left:{x:.0f}px;top:{438 if dest else 445}px;font-size:{31 if dest else 24}px;{'' if dest else 'opacity:.82'}'>{nome}</div>"
             f"<div class='m c' style='left:{x:.0f}px;top:486px;font-size:15px;color:{DEST if dest else MED}'>{hora}</div>")
html += f"<div class='m c' style='left:512px;top:548px;font-size:14px'>ingressos aqui no site ou na portaria.</div>"
with sync_playwright() as p:
    br = p.chromium.launch()
    for sf, nome in [(1, 'site_afterzin_fotos_1024x600'), (2, 'site_afterzin_fotos_1024x600@2x')]:
        pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=sf)
        pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
        pg.screenshot(path=OUT + '/_t.png', omit_background=True); pg.close()
        t = Image.open(OUT + '/_t.png'); bg = fundo(sf); bg.paste(t, (0, 0), t)
        random.seed(13); n = Image.effect_noise(bg.size, 22).convert('RGB'); bg = Image.blend(bg, ImageChops.overlay(bg, n), .11)
        bg.save(f'{OUT}/{nome}.png'); print(nome, bg.size)
        if sf == 1: bg.save(f'{OUT}/{nome}.jpg', quality=94)
    br.close()
os.remove(OUT + '/_t.png')
