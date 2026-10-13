"""Gera o logo why not? Halloween (osso/brasa) como SVG vetorial: abóbora acesa no lugar do "o".
Uso: python3 logo_halloween.py <Fraunces variável .ttf/.woff2> <pasta de saída>"""
import sys, re
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb

FONT, OUT = sys.argv[1], sys.argv[2]
TEXT = "why not?"

vf = TTFont(FONT)
inst = instantiateVariableFont(vf, {"wght": 900, "opsz": 144, "SOFT": 0, "WONK": 0})
inst.flavor = None
inst.save(OUT + "/Fraunces-900-144.ttf")
font = TTFont(OUT + "/Fraunces-900-144.ttf")
upem = font["head"].unitsPerEm
gs = font.getGlyphSet()

blob = hb.Blob.from_file_path(OUT + "/Fraunces-900-144.ttf")
hbf = hb.Font(hb.Face(blob))
buf = hb.Buffer(); buf.add_str(TEXT); buf.guess_segment_properties()
hb.shape(hbf, buf, {"kern": True, "liga": True})
order = font.getGlyphOrder()

def contours(gname):
    rp = DecomposingRecordingPen(gs); gs[gname].draw(rp)
    out, cur = [], []
    for op, args in rp.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            out.append(cur); cur = []
    return out

def to_d(ops, dx):
    p = SVGPathPen(None)
    for op, args in ops:
        getattr(p, op)(*[(x + dx, y) for x, y in args])
    return p.getCommands()

def bounds(ops):
    b = BoundsPen(None)
    for op, args in ops:
        getattr(b, op)(*args)
    return b.bounds

x = 0; parts = []; dot = None; BBL = []
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    g = order[info.codepoint]
    cs = contours(g)
    if g == "o":
        # a abóbora entra no lugar do "o"
        ob = bounds([op for c in cs for op in c])
        dot = (ob[0] + x, ob[1], ob[2] - ob[0], ob[3] - ob[1])
        x += pos.x_advance
        continue
    for c in cs:
        parts.append(to_d(c, x + pos.x_offset))
        bb = bounds(c)
        if bb:
            BBL.append((bb[0] + x, bb[1], bb[2] + x, bb[3]))
    x += pos.x_advance
adv = x
BB = (min(b[0] for b in BBL), min(b[1] for b in BBL), max(b[2] for b in BBL), max(b[3] for b in BBL))

# limites gerais
allb = [1e9, 1e9, -1e9, -1e9]
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    pass
d_text = " ".join(parts)
minx, miny, maxx, maxy = BB

# ---- desenho ----
FACE = "#efe4d0"   # osso
RAMP = ["#e6c9a3", "#e0b07e", "#d8975f", "#cc7f47", "#bb6a37", "#a4572c",
        "#8a4724", "#6f391d", "#552c17", "#3e2012", "#2a160c", "#1a0e08"]
step = upem / 80.0
N = len(RAMP)

ox0, oy0, ow, oh = dot
R = ow * 1.1 / 2.08          # largura da abóbora ≈ largura do "o" (um pouco maior)
cx = ox0 + ow / 2
cy = oy0 - ow * 0.02 + 0.9 * R  # assenta na linha de base

def pumpkin_sil(fill):
    # silhueta: três gomos + cabo (coordenadas em unidades de fonte, y para cima → invertido depois)
    return (f'<ellipse cx="{cx - R*0.42:.1f}" cy="{cy:.1f}" rx="{R*0.62:.1f}" ry="{R*0.84:.1f}" fill="{fill}"/>'
            f'<ellipse cx="{cx + R*0.42:.1f}" cy="{cy:.1f}" rx="{R*0.62:.1f}" ry="{R*0.84:.1f}" fill="{fill}"/>'
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{R*0.6:.1f}" ry="{R*0.9:.1f}" fill="{fill}"/>'
            f'<path d="M{cx - R*0.12:.1f} {cy + R*0.8:.1f} L{cx - R*0.06:.1f} {cy + R*1.22:.1f} L{cx + R*0.2:.1f} {cy + R*1.3:.1f} L{cx + R*0.14:.1f} {cy + R*0.8:.1f} Z" fill="{fill}"/>')

def pumpkin_face():
    r = R
    lobes = (f'<ellipse cx="{cx - r*0.42:.1f}" cy="{cy:.1f}" rx="{r*0.62:.1f}" ry="{r*0.84:.1f}" fill="url(#gomo)"/>'
             f'<ellipse cx="{cx + r*0.42:.1f}" cy="{cy:.1f}" rx="{r*0.62:.1f}" ry="{r*0.84:.1f}" fill="url(#gomo)"/>'
             f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r*0.6:.1f}" ry="{r*0.9:.1f}" fill="url(#gomoc)"/>')
    stem = (f'<path d="M{cx - r*0.12:.1f} {cy + r*0.8:.1f} L{cx - r*0.06:.1f} {cy + r*1.22:.1f} '
            f'L{cx + r*0.2:.1f} {cy + r*1.3:.1f} L{cx + r*0.14:.1f} {cy + r*0.8:.1f} Z" fill="#6b5a2e"/>')
    # olhos triangulares e boca serrilhada (y para cima)
    eyes = (f'<path d="M{cx - r*0.46:.1f} {cy + r*0.12:.1f} L{cx - r*0.12:.1f} {cy + r*0.12:.1f} L{cx - r*0.29:.1f} {cy + r*0.44:.1f} Z" fill="url(#luz)"/>'
            f'<path d="M{cx + r*0.12:.1f} {cy + r*0.12:.1f} L{cx + r*0.46:.1f} {cy + r*0.12:.1f} L{cx + r*0.29:.1f} {cy + r*0.44:.1f} Z" fill="url(#luz)"/>')
    m = [(-0.5, -0.12), (-0.34, -0.22), (-0.24, -0.12), (-0.08, -0.24), (0.08, -0.12),
         (0.24, -0.24), (0.34, -0.12), (0.5, -0.12), (0.36, -0.42), (0.18, -0.34),
         (0.06, -0.48), (-0.08, -0.36), (-0.22, -0.48), (-0.36, -0.36)]
    mouth = '<path d="M' + " L".join(f"{cx + a*r:.1f} {cy + b*r:.1f}" for a, b in m) + ' Z" fill="url(#luz)"/>'
    seams = (f'<path d="M{cx - r*0.2:.1f} {cy + r*0.84:.1f} Q{cx - r*0.34:.1f} {cy:.1f} {cx - r*0.2:.1f} {cy - r*0.84:.1f}" '
             f'fill="none" stroke="#5a1d06" stroke-width="{r*0.05:.1f}" opacity=".55"/>'
             f'<path d="M{cx + r*0.2:.1f} {cy + r*0.84:.1f} Q{cx + r*0.34:.1f} {cy:.1f} {cx + r*0.2:.1f} {cy - r*0.84:.1f}" '
             f'fill="none" stroke="#5a1d06" stroke-width="{r*0.05:.1f}" opacity=".55"/>')
    return lobes + seams + stem + eyes + mouth

defs = f'''<defs>
<radialGradient id="gomo" cx=".45" cy=".4" r=".75"><stop offset="0" stop-color="#e2873a"/><stop offset=".65" stop-color="#b8541e"/><stop offset="1" stop-color="#6e2a0c"/></radialGradient>
<radialGradient id="gomoc" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#ec9446"/><stop offset=".65" stop-color="#c05c22"/><stop offset="1" stop-color="#7a300e"/></radialGradient>
<linearGradient id="luz" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff0c2"/><stop offset=".55" stop-color="#ffc45a"/><stop offset="1" stop-color="#f08a2c"/></linearGradient>
<radialGradient id="aura" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff9a3c" stop-opacity=".32"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
</defs>'''

layers = []
for k in range(N, 0, -1):
    dx, dy = -k * step, -k * step  # esquerda e para baixo (y da fonte sobe)
    layers.append(f'<g transform="translate({dx:.1f} {dy:.1f})" fill="{RAMP[k-1]}"><path d="{d_text}"/>{pumpkin_sil(RAMP[k-1])}</g>')
aura = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R*2.0:.1f}" fill="url(#aura)"/>'
front = f'<path d="{d_text}" fill="{FACE}"/>' + aura + pumpkin_face()
body = "".join(layers) + front

# caixa total (unidades da fonte), com extrusão e abóbora
ext = N * step
bx0 = min(minx, cx - R*1.05) - ext - 10
bx1 = max(maxx, cx + R*1.05) + 10
by0 = min(miny, cy - R) - ext - 10
by1 = max(maxy, cy + R*1.35) + 10
W, H = bx1 - bx0, by1 - by0

def svg(width_px, canvas=None, bg=False):
    if canvas is None:
        s = width_px / W
        cw, ch = width_px, H * s
        tx, ty = -bx0 * s, by1 * s
    else:
        cw, ch = canvas
        s = width_px / W
        tx = (cw - W * s) / 2 - bx0 * s
        ty = (ch - H * s) / 2 + by1 * s
    g = f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f} {-s:.5f})">{body}</g>'
    back = ''
    if bg:
        back = ('<defs><radialGradient id="bg" cx=".5" cy=".5" r=".62"><stop offset="0" stop-color="#2b140a"/>'
                '<stop offset=".45" stop-color="#140b07"/><stop offset="1" stop-color="#0b0706"/></radialGradient></defs>'
                f'<rect width="{cw}" height="{ch}" fill="#0b0706"/><rect width="{cw}" height="{ch}" fill="url(#bg)"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw:.0f}" height="{ch:.0f}" viewBox="0 0 {cw:.0f} {ch:.0f}" '
            f'role="img" aria-label="why not? — logo Halloween">{back}{defs}{g}</svg>')

open(OUT + "/logo-why-not-halloween.svg", "w").write(svg(1600))
open(OUT + "/logo-why-not-halloween-fundo.svg", "w").write(svg(880, (1080, 1080), bg=True))
print("ok", W, H, dot)
