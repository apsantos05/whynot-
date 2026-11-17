"""Capa de Reels do afterzin a partir de um quadro do vídeo: logo no canto, data no canto direito, frase grande embaixo.
1080x1920; logo, data e frase cabem juntos no corte 4:5 da grade se o corte for puxado pro topo. Uso: python3 afterzin_capa_reels.py <pasta fontes> <quadro.png>"""
import os, sys, base64, random
import cv2, numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, QUADRO = sys.argv[1], sys.argv[2]
OUT = R + '/afterzin-2011/capa-reels'; os.makedirs(OUT, exist_ok=True)
LOGO = R + '/assets/logo/grafite/logo-why-not-grafite.png'
BASE, DEST, MED = (8, 9, 10), '#ececec', '#a9adb1'
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

# 1) limpa a logo pequena que já vem queimada no canto do vídeo
im = cv2.imread(QUADRO); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
mask = np.zeros(g.shape, np.uint8); mask[46:100, 24:150] = (g[46:100, 24:150] > 105).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8)); im = cv2.inpaint(im, mask, 6, cv2.INPAINT_TELEA)
foto = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))

def fundo(pb):
    f = foto
    if pb:
        gg = ImageEnhance.Contrast(ImageOps.autocontrast(ImageOps.grayscale(f), cutoff=.4)).enhance(1.08)
        f = Image.merge('RGB', [gg.point(lambda v, b=b: round(b + (236 - b) * v / 255)) for b in BASE])
    m = Image.linear_gradient('L').resize((W, H)).point(lambda v: round(255 * (lambda t: t * t * (3 - 2 * t))(min(1, max(0, (v / 255 - .46) / .30)))))
    f = Image.composite(Image.new('RGB', (W, H), BASE), f, m.point(lambda v: round(v * .93)))
    t = ImageOps.flip(Image.linear_gradient('L')).resize((W, H)).point(lambda v: max(0, round((v - 165) * 1.5)))
    return Image.composite(Image.new('RGB', (W, H), BASE), f, t)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}"""
html = (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:62px;top:92px;width:204px'>"
        f"<div style='position:absolute;right:62px;top:92px;font-family:FrR;font-weight:500;font-size:56px;color:{DEST};letter-spacing:.01em;font-feature-settings:\"lnum\";font-variation-settings:\"WONK\" 0;text-shadow:0 2px 18px rgba(0,0,0,.55)'>21.11</div>"
        f"<div style='position:absolute;left:60px;top:1062px;font-family:Fr;font-style:italic;font-weight:440;font-size:172px;line-height:.98;letter-spacing:-.015em;color:{DEST};text-shadow:0 4px 30px rgba(0,0,0,.5)'>aqui é<br>why not?</div>")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
    pg.screenshot(path=OUT + '/_t.png', omit_background=True); br.close()
t = Image.open(OUT + '/_t.png')
for pb, nome in [(True, 'capa-reels_afterzin_pb'), (False, 'capa-reels_afterzin_cor')]:
    bg = fundo(pb); bg.paste(t, (0, 0), t)
    random.seed(13); n = Image.effect_noise(bg.size, 22).convert('RGB'); bg = Image.blend(bg, ImageChops.overlay(bg, n), .10)
    bg.save(f'{OUT}/{nome}.jpg', quality=94); print(nome)
os.remove(OUT + '/_t.png')
