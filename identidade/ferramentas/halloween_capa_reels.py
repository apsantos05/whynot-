"""Capa do reels 18/10 'no one leaves.' — vela + logo + COMING SOON, discreta.
Gera camadas PNG + manifest (para halloween_teaser_psd.js) + composição final."""
import os, json, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright
import base64

S = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(S, '..')
W, H = 1080, 1920
BG = (11, 7, 6)
DOC = '1810_capa-reels-no-one-leaves'
L = os.path.join(S, DOC); os.makedirs(L, exist_ok=True)
layers = []

def add(name, im, blend=None, opacity=1, text=None):
    p = os.path.join(L, f'{len(layers):02d}.png'); im.save(p)
    d = {'name': name, 'png': p, 'blend': blend, 'opacity': opacity}
    if text: d['text'] = text
    layers.append(d)

# 00 fundo
add('Fundo', Image.new('RGBA', (W, H), BG + (255,)))

# 01 foto vela, aquecida e com bordas esfumadas
ph = Image.open(SC + '/hwf/photo-1640085461451-e3dc47415dd1.png').convert('RGB')
k = 1.10; ph = ph.resize((round(ph.width * k), round(ph.height * k)), Image.LANCZOS)
r, g, b = ph.split()
ph = Image.merge('RGB', (r.point(lambda v: min(255, max(0, v - 14) * 1.12)), g.point(lambda v: max(0, v - 14) * 1.06), b.point(lambda v: max(0, v - 16) * 0.82)))
ox, oy = (W - ph.width) // 2, 190
m = Image.new('L', ph.size, 0)
ImageDraw.Draw(m).ellipse((150, 80, ph.width - 150, ph.height - 140), fill=255)
m = m.filter(ImageFilter.GaussianBlur(150))
foto = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl = ph.convert('RGBA'); fl.putalpha(m)
foto.alpha_composite(fl, (ox, oy))
add('FOTO · vela (Unsplash)', foto)

# 02 brilho brasa atrás da chama
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gm = Image.new('L', (W, H), 0)
ImageDraw.Draw(gm).ellipse((W/2 - 260, 330, W/2 + 260, 760), fill=150)
gm = gm.filter(ImageFilter.GaussianBlur(120)); gl.paste((122, 58, 22, 255), (0, 0), gm)
add('Brilho brasa (tela)', gl, blend='screen', opacity=0.55)

# 03 vinheta
vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-260, -120, W + 260, H + 120), fill=255)
vg = vg.filter(ImageFilter.GaussianBlur(260))
vin = Image.new('RGBA', (W, H), (255, 255, 255, 255)); dark = Image.new('RGBA', (W, H), (40, 26, 20, 255))
vin = Image.composite(vin, dark, vg)
add('Vinheta', vin, blend='multiply')

# 04/05 logo + COMING SOON (renderizados em Chromium com as fontes da identidade)
F = SC + '/hwb/fonts'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO_W, LOGO_Y, SOON_Y = 340, 1372, 1538
css = (f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F + '/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
       "html,body{margin:0;width:1080px;height:1920px;background:transparent}")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f"<style>{css}</style><img src='data:image/png;base64,{b64(SC + '/hwb/out/_logo_reto.png')}' "
                   f"style='position:absolute;left:{(W - LOGO_W)//2}px;top:{LOGO_Y}px;width:{LOGO_W}px'>")
    pg.wait_for_timeout(200); pg.screenshot(path=L + '/_logo.png', omit_background=True)
    pg.set_content(f"<style>{css}</style><div style=\"position:absolute;left:0;right:0;top:{SOON_Y}px;text-align:center;"
                   "font-family:SM;font-weight:700;font-size:24px;letter-spacing:.5em;text-indent:.5em;color:#c4a582\">COMING SOON</div>")
    pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
    pg.screenshot(path=L + '/_soon.png', omit_background=True); br.close()
add('Logo why not? halloween', Image.open(L + '/_logo.png').convert('RGBA'))
add('COMING SOON', Image.open(L + '/_soon.png').convert('RGBA'),
    text={'text': 'COMING SOON', 'font': 'SpaceMono-Bold', 'size': 24, 'color': '#c4a582', 'x': W / 2, 'y': SOON_Y + 24, 'ls': .5, 'anchor': 'middle'})

# 06 grão
random.seed(7); n = Image.effect_noise((W, H), 22).convert('L')
gr = Image.merge('RGBA', (n, n, n, Image.new('L', (W, H), 255)))
add('Grão (sobrepor · 18%)', gr, blend='overlay', opacity=0.18)

# composição (simula os modos de mesclagem usados)
def comp():
    base = Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        im = Image.open(d['png']).convert('RGBA'); a = im.split()[3].point(lambda v: v * d['opacity'])
        rgb = im.convert('RGB')
        if d['blend'] == 'multiply': rgb = ImageChops.multiply(base, rgb)
        elif d['blend'] == 'screen': rgb = ImageChops.screen(base, rgb)
        elif d['blend'] == 'overlay': rgb = ImageChops.overlay(base, rgb)
        base = Image.composite(rgb, base, a)
    return base
c = comp(); c.save(L + '/_composite.png'); c.save(os.path.join(S, DOC + '.png'))
json.dump({DOC: {'width': W, 'height': H, 'layers': layers}}, open(S + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
# prévia do recorte do grid (3:4 central) e do feed 4:5
c.crop((0, 240, W, 1680)).resize((360, 480)).save(S + '/_grid34.png')
c.resize((360, 640)).save(S + '/_full.png')
print('ok')
