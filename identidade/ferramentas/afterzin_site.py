"""Banner do site da Bally — afterzin why not? — 1024x600 (medida fixa do site) + @2x. Linha minimalista grafite.
Uso: python3 afterzin_site.py <pasta fontes> <pasta fotos stock>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
OUT = R + '/afterzin-2011/minimal'
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ececec', '#a9adb1'
W, H = 1024, 600
LINE = [('01:00', 'Mexikanno'), ('02:00', 'Marquez'), ('03:00', 'Paganotti'), ('04:00', 'Polão'), ('05:00', 'Kaio Alves'), ('06:00', 'Possani')]
DESTAQUE = {'Paganotti', 'Kaio Alves'}
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

def fundo(sf):
    w, h = W * sf, H * sf
    im = Image.open(f'{ST}/AdobeStock_175742652.jpeg').convert('RGB')
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * .30)
    g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, y, x + w, y + h))), cutoff=.5).point(lambda v: round(255 * (v / 255) ** 1.35))
    duo = Image.merge('RGB', [g.point(lambda v, b=b: round(b + (236 - b) * v / 255)) for b in BASE])
    # escurece as laterais (texto) e a base; o meio fica com os feixes de luz
    hz = Image.linear_gradient('L').rotate(90, expand=True).resize((w, h))
    lat = hz.point(lambda v: min(255, round(abs(v - 127.5) * 2.3 + 40)))
    duo = Image.composite(Image.new('RGB', (w, h), BASE), duo, lat.point(lambda v: round(v * .86)))
    base = Image.linear_gradient('L').resize((w, h)).point(lambda v: 0 if v < 150 else round((v - 150) * 2.2))
    return Image.composite(Image.new('RGB', (w, h), BASE), duo, base)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1;letter-spacing:-.01em;white-space:nowrap;font-variation-settings:"WONK" 0}}
.m{{position:absolute;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.01em}}
.h{{position:absolute;font-family:FrR;font-weight:500;white-space:nowrap;font-feature-settings:"tnum","lnum";letter-spacing:.02em}}"""

html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:56px;top:48px;width:118px'>"
        f"<div class='m' style='left:56px;top:262px;font-size:19px;color:{DEST}'>sexta pra sábado, 21.11, a partir da 01h</div>"
        f"<div class='t' style='left:52px;top:296px;font-size:116px;font-variation-settings:\"WONK\" 1'>afterzin.</div>"
        f"<div class='t' style='left:56px;top:432px;font-size:30px;color:{MED}'>o show acaba. a noite continua.</div>"
        f"<div class='m' style='left:56px;top:520px;font-size:17px'>na Bally Club. ingressos aqui no site ou na portaria.</div>")
x0, yy = 664, 96
html += f"<div class='m' style='left:{x0}px;top:{yy-40}px;font-size:16px;color:{DEST}'>line-up e horários</div>"
for hora, nome in LINE:
    d = nome in DESTAQUE; f = 46 if d else 33; p_ = 70 if d else 54
    html += (f"<div class='h' style='left:{x0}px;top:{yy+round(f*.34)}px;font-size:15px;color:{DEST if d else MED}'>{hora}</div>"
             f"<div class='t' style='left:{x0+70}px;top:{yy}px;font-size:{f}px;{'' if d else 'opacity:.78'}'>{nome}</div>")
    yy += p_
with sync_playwright() as p:
    br = p.chromium.launch()
    for sf, nome in [(1, 'site_afterzin_1024x600'), (2, 'site_afterzin_1024x600@2x')]:
        pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=sf)
        pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
        pg.screenshot(path=OUT + '/_t.png', omit_background=True); pg.close()
        t = Image.open(OUT + '/_t.png'); bg = fundo(sf); bg.paste(t, (0, 0), t)
        random.seed(13); n = Image.effect_noise(bg.size, 22).convert('RGB'); bg = Image.blend(bg, ImageChops.overlay(bg, n), .12)
        bg.save(f'{OUT}/{nome}.png'); print(nome, bg.size)
        if sf == 1: bg.save(f'{OUT}/{nome}.jpg', quality=94)
    br.close()
os.remove(OUT + '/_t.png')
