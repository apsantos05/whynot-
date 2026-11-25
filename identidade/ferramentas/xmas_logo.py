"""Logo do why not? XMAS PARTY (18.12) em vetor: texto convertido em curvas (fontTools) e montado em SVG,
pronto para abrir no Illustrator. Gera duas direções e prévias PNG sobre vermelho e sobre branco.
Uso: python3 xmas_logo.py <pasta fontsource> <pasta saída>"""
import os, sys, math, base64
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FS, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
F = lambda pkg, f: TTFont(f'{FS}/{pkg}/package/files/{f}')
BODONI = F('fontsource-bodoni-moda-5.3.0', 'bodoni-moda-latin-900-normal.woff2')
BODONI_I = F('fontsource-bodoni-moda-5.3.0', 'bodoni-moda-latin-700-italic.woff2')
SCRIPT = F('fontsource-pinyon-script-5.3.0', 'pinyon-script-latin-400-normal.woff2')
CINZEL = F('fontsource-cinzel-5.3.0', 'cinzel-latin-700-normal.woff2')
CINZEL9 = F('fontsource-cinzel-5.3.0', 'cinzel-latin-900-normal.woff2')
PLAYI = F('fontsource-playfair-display-5.3.0', 'playfair-display-latin-700-italic.woff2')

def texto(font, s, size, x, y, track=0, anchor='start'):
    """Devolve (path d, largura) do texto em curvas, baseline em y."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm; k = size / upm
    hmtx = font['hmtx']; names = [cmap.get(ord(c)) for c in s]
    largura = sum(hmtx[n][0] for n in names if n) * k + track * (len(s) - 1)
    x0 = x - (largura if anchor == 'end' else largura / 2 if anchor == 'middle' else 0)
    pen = SVGPathPen(gs); cx = x0
    for n in names:
        if not n: continue
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, cx, y))); cx += hmtx[n][0] * k + track
    return pen.getCommands(), largura

def estrela(cx, cy, r, fino=.16):
    pts = []
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4; rr = r if i % 2 == 0 else r * fino
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy - rr * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + ' Z'

OURO = """<linearGradient id="ouro" x1="0" y1="0" x2="0.35" y2="1">
 <stop offset="0" stop-color="#fff3c4"/><stop offset=".22" stop-color="#e9c46a"/><stop offset=".48" stop-color="#b8862b"/>
 <stop offset=".62" stop-color="#f6dc8e"/><stop offset=".82" stop-color="#a8741f"/><stop offset="1" stop-color="#e8c873"/></linearGradient>"""
VERM, BRANCO = '#d0142c', '#fbf6ee'

def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{OURO}</defs>{corpo}</svg>'

# ---- Direção A: editorial de luxo (Bodoni + script) ----
W, H = 2400, 1620
xmas, wx = texto(BODONI, 'XMAS', 640, W / 2, 900, track=-6, anchor='middle')
party, _ = texto(SCRIPT, 'party', 470, 0, 0)
why, _ = texto(PLAYI, 'why not?', 96, W / 2 - wx / 2 + 8, 300)
# variante com gorro: why not? sai da esquerda (o gorro senta no X) e a data alinha com o X
whyC, _ = texto(PLAYI, 'why not?', 96, W / 2 + 40, 330, anchor='middle')
dataC, _ = texto(CINZEL, 'SEXTA, 18.12', 62, W / 2 - wx / 2 + 12, 1490, track=22)
data, _ = texto(CINZEL, 'SEXTA, 18.12', 62, W / 2 - 300, 1500, track=22, anchor='middle')
A = (f'<g id="xmas"><path d="{xmas}" fill="url(#ouro)"/></g>'
     f'<g id="party" transform="translate({W/2 + 40},{1150}) rotate(-7)"><path d="{party}" fill="{VERM}" stroke="{BRANCO}" stroke-width="9" paint-order="stroke"/></g>'
     f'<g id="why-not"><path d="{why}" fill="{BRANCO}"/></g>'
     f'<g id="estrelas"><path d="{estrela(W/2 + wx/2 - 20, 330, 78)}" fill="url(#ouro)"/><path d="{estrela(W/2 + wx/2 + 60, 430, 34)}" fill="url(#ouro)"/></g>'
     f'<g id="data"><path d="{data}" fill="{BRANCO}"/></g>')
open(f'{OUT}/xmas_logo_A.svg', 'w').write(svg(W, H, A))

# ---- Direção B: selo festivo (Cinzel em círculo) ----
W2 = H2 = 2000; C = W2 / 2
anel = (f'<circle cx="{C}" cy="{C}" r="900" fill="none" stroke="url(#ouro)" stroke-width="16"/>'
        f'<circle cx="{C}" cy="{C}" r="860" fill="none" stroke="url(#ouro)" stroke-width="5"/>')
x2, _ = texto(CINZEL9, 'XMAS', 470, C, 1080, track=30, anchor='middle')
p2, _ = texto(CINZEL, 'PARTY', 210, C, 1330, track=70, anchor='middle')
w2, _ = texto(PLAYI, 'why not?', 120, C, 610, anchor='middle')
d2, _ = texto(CINZEL, '18.12', 96, C, 1560, track=26, anchor='middle')
B = (anel + f'<path d="{w2}" fill="{BRANCO}"/><path d="{x2}" fill="url(#ouro)"/><path d="{p2}" fill="{VERM}" stroke="{BRANCO}" stroke-width="6" paint-order="stroke"/>'
     f'<path d="{d2}" fill="{BRANCO}"/><path d="M{C-330},{1420} L{C+330},{1420}" stroke="url(#ouro)" stroke-width="5"/>'
     f'<path d="{estrela(C - 600, 1265, 46)}" fill="url(#ouro)"/><path d="{estrela(C + 600, 1265, 46)}" fill="url(#ouro)"/><path d="{estrela(C, 300, 90)}" fill="url(#ouro)"/>')
open(f'{OUT}/xmas_logo_B.svg', 'w').write(svg(W2, H2, B))
C_ = A.replace(f'<path d="{why}"', f'<path d="{whyC}"').replace(f'<path d="{data}"', f'<path d="{dataC}"')
open(f'{OUT}/xmas_logo_C_base.svg', 'w').write(svg(W, H, C_))
print('ok')
