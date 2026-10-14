"""Feed 'sem fantasia, não entra.' — máscara + logo + fantasia obrigatória · 6 DJs · COMING SOON.
Camadas PNG + manifest (halloween_teaser_psd.js) + composição. Documento 2160x2700 (feed 4:5 @2x)."""
import os, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__)); SC = os.path.join(S, '..')
W, H = 2160, 2700
DOC = '2210_feed_sem-fantasia-nao-entra'
L = os.path.join(S, DOC); os.makedirs(L, exist_ok=True)
layers = []
def add(name, im, blend=None, opacity=1, text=None):
    p = os.path.join(L, f'{len(layers):02d}.png'); im.save(p)
    d = {'name': name, 'png': p, 'blend': blend, 'opacity': opacity}
    if text: d['text'] = text
    layers.append(d)

add('Fundo', Image.new('RGBA', (W, H), (11, 7, 6, 255)))

# foto da máscara: recorte 4:5 em volta da máscara, tom osso/âmbar
ph = Image.open(SC + '/hwf/photo-1640869444601-e791c41bae6b.png').convert('RGB')
cw = round(1160 * 4 / 5); cx = 1015
ph = ph.crop((cx - cw // 2, 0, cx + cw // 2, 1160)).resize((W, H), Image.LANCZOS)
g = ImageOps.grayscale(ph)
g = g.point(lambda v: max(0, v - 10) * 1.05)
ph = ImageOps.colorize(g, black=(9, 6, 5), mid=(122, 86, 58), white=(228, 214, 190), midpoint=118)
K = 0.74  # máscara menor, mais respiro no escuro
sw, sh = round(W * K), round(H * K); ph = ph.resize((sw, sh), Image.LANCZOS)
m = Image.new('L', (sw, sh), 0); ImageDraw.Draw(m).ellipse((90, 90, sw - 90, sh - 90), fill=255); m = m.filter(ImageFilter.GaussianBlur(160))
foto = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl = ph.convert('RGBA'); fl.putalpha(m)
foto.alpha_composite(fl, ((W - sw) // 2, 330))
add('FOTO · máscara (Unsplash)', foto)

# brilho brasa atrás da máscara
gm = Image.new('L', (W, H), 0); ImageDraw.Draw(gm).ellipse((W/2 - 700, 650, W/2 + 600, 1500), fill=120)
gm = gm.filter(ImageFilter.GaussianBlur(260)); gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gl.paste((122, 58, 22, 255), (0, 0), gm)
add('Brilho brasa (tela)', gl, blend='screen', opacity=0.6)

# escurecer base p/ leitura
gr = Image.linear_gradient('L').resize((W, H)); gr = gr.point(lambda v: 0 if v < 120 else min(255, (v - 120) * 2.2))
esc = Image.new('RGBA', (W, H), (11, 7, 6, 255)); esc.putalpha(gr)
add('Escurecer base (leitura do texto)', esc)

vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-500, -300, W + 500, H + 300), fill=255)
vg = vg.filter(ImageFilter.GaussianBlur(380))
add('Vinheta', Image.composite(Image.new('RGBA', (W, H), (255, 255, 255, 255)), Image.new('RGBA', (W, H), (36, 24, 18, 255)), vg), blend='multiply')

# textos/logo via Chromium com as fontes da identidade
F = SC + '/hwb/fonts'; b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
css = (f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F + '/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F + '/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
       "html,body{margin:0;width:2160px;height:2700px;background:transparent}"
       ".c{position:absolute;left:0;right:0;text-align:center}")
LOGO_W, LOGO_Y = 620, 170
T1_Y, T2_Y, TS = 1820, 2040, 230
INFO_Y, SOON_Y = 2370, 2470
items = {
    'logo': f"<img src='data:image/png;base64,{b64(SC + '/hwb/out/_logo_reto.png')}' style='position:absolute;left:{(W-LOGO_W)//2}px;top:{LOGO_Y}px;width:{LOGO_W}px'>",
    't1': f"<div class=c style=\"top:{T1_Y}px;font-family:Fr;font-style:italic;font-size:{TS}px;color:#efe4d0;line-height:1;text-shadow:0 0 40px rgba(196,165,130,.25)\">sem fantasia,</div>",
    't2': f"<div class=c style=\"top:{T2_Y}px;font-family:Fr;font-style:italic;font-size:{TS}px;color:#efe4d0;line-height:1;text-shadow:0 0 40px rgba(196,165,130,.25)\">não entra.</div>",
    'info': f"<div class=c style=\"top:{INFO_Y}px;font-family:SM;font-weight:700;font-size:46px;letter-spacing:.32em;text-indent:.32em;color:#c4a582\">FANTASIA OBRIGATÓRIA · 6 DJS</div>",
    'soon': f"<div class=c style=\"top:{SOON_Y}px;font-family:SM;font-weight:700;font-size:34px;letter-spacing:.5em;text-indent:.5em;color:#efe4d0;opacity:.7\">COMING SOON</div>",
}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for k, body in items.items():
        pg.set_content(f"<style>{css}</style>{body}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{L}/_{k}.png', omit_background=True)
    br.close()
im = lambda k: Image.open(f'{L}/_{k}.png').convert('RGBA')
add('Logo why not? halloween', im('logo'))
add('Título · sem fantasia,', im('t1'), text={'text': 'sem fantasia,', 'font': 'Fraunces-Italic', 'size': TS, 'color': '#efe4d0', 'x': W/2, 'y': T1_Y + TS*0.8, 'ls': 0, 'anchor': 'middle'})
add('Título · não entra.', im('t2'), text={'text': 'não entra.', 'font': 'Fraunces-Italic', 'size': TS, 'color': '#efe4d0', 'x': W/2, 'y': T2_Y + TS*0.8, 'ls': 0, 'anchor': 'middle'})
add('Info · FANTASIA OBRIGATÓRIA · 6 DJS', im('info'), text={'text': 'FANTASIA OBRIGATÓRIA · 6 DJS', 'font': 'SpaceMono-Bold', 'size': 46, 'color': '#c4a582', 'x': W/2, 'y': INFO_Y + 46, 'ls': .32, 'anchor': 'middle'})
add('COMING SOON', im('soon'), opacity=1, text={'text': 'COMING SOON', 'font': 'SpaceMono-Bold', 'size': 34, 'color': '#efe4d0', 'x': W/2, 'y': SOON_Y + 34, 'ls': .5, 'anchor': 'middle'})

random.seed(3); n = Image.effect_noise((W, H), 22).convert('L')
add('Grão (sobrepor · 18%)', Image.merge('RGBA', (n, n, n, Image.new('L', (W, H), 255))), blend='overlay', opacity=0.18)

def comp():
    base = Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        i = Image.open(d['png']).convert('RGBA'); a = i.split()[3].point(lambda v: v * d['opacity']); rgb = i.convert('RGB')
        if d['blend'] == 'multiply': rgb = ImageChops.multiply(base, rgb)
        elif d['blend'] == 'screen': rgb = ImageChops.screen(base, rgb)
        elif d['blend'] == 'overlay': rgb = ImageChops.overlay(base, rgb)
        base = Image.composite(rgb, base, a)
    return base
c = comp(); c.save(L + '/_composite.png'); c.save(f'{S}/{DOC}_2x.png'); c.resize((1080, 1350), Image.LANCZOS).save(f'{S}/{DOC}.png')
c.resize((432, 540)).save(S + '/_feed_prev.png')
json.dump({DOC: {'width': W, 'height': H, 'layers': layers}}, open(S + '/manifest_feed.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
