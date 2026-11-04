"""Wordmark why not? genérico: qualquer texto em Fraunces Black 900 com a extrusão 3D em 12 degraus.
Uso: python3 wordmark.py <fraunces variável .woff2/.ttf> <texto> <cor face> <rampa topo> <rampa fundo> <saida.png> [largura px]
"""
import sys, os, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb
from playwright.sync_api import sync_playwright

FONT, TEXT, FACE, RA, RB, OUT = sys.argv[1:7]
WPX = int(sys.argv[7]) if len(sys.argv) > 7 else 3200
N = 12

tmp = tempfile.mkdtemp()
ttf = tmp + '/f.ttf'
vf = TTFont(FONT)
inst = instantiateVariableFont(vf, {"wght": 900, "opsz": 144, "SOFT": 0, "WONK": 0}); inst.flavor = None; inst.save(ttf)
font = TTFont(ttf); gs = font.getGlyphSet(); upem = font['head'].unitsPerEm; order = font.getGlyphOrder()
buf = hb.Buffer(); buf.add_str(TEXT); buf.guess_segment_properties()
hb.shape(hb.Font(hb.Face(hb.Blob.from_file_path(ttf))), buf, {"kern": True, "liga": True})

x = 0; parts = []; bb = [1e9, 1e9, -1e9, -1e9]
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    g = order[info.codepoint]
    from fontTools.pens.transformPen import TransformPen
    sp = SVGPathPen(gs); gs[g].draw(TransformPen(sp, (1, 0, 0, 1, x + pos.x_offset, 0)))
    parts.append(sp.getCommands())
    bp = BoundsPen(gs); gs[g].draw(TransformPen(bp, (1, 0, 0, 1, x + pos.x_offset, 0)))
    if bp.bounds:
        b = bp.bounds; bb = [min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3])]
    x += pos.x_advance
d = ' '.join(parts)

def hx(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
a, b = hx(RA), hx(RB)
ramp = ['#%02x%02x%02x' % tuple(round(a[j] + (b[j] - a[j]) * (k / (N - 1)) ** .85) for j in range(3)) for k in range(N)]
step = upem / 80.0; ext = N * step
x0, y0, x1, y1 = bb[0] - ext - 10, bb[1] - ext - 10, bb[2] + 10, bb[3] + 10
W, H = x1 - x0, y1 - y0; s = WPX / W; HPX = round(H * s)
layers = ''.join(f'<g transform="translate({-k*step:.1f} {-k*step:.1f})" fill="{ramp[k-1]}"><path d="{d}"/></g>' for k in range(N, 0, -1))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WPX}" height="{HPX}" viewBox="0 0 {WPX} {HPX}">'
       f'<g transform="translate({-x0*s:.2f} {y1*s:.2f}) scale({s:.5f} {-s:.5f})">{layers}<path d="{d}" fill="{FACE}"/></g></svg>')
open(OUT.replace('.png', '.svg'), 'w').write(svg)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': WPX, 'height': HPX})
    pg.set_content(f"<style>*{{margin:0}}body{{background:transparent}}</style>{svg}")
    pg.screenshot(path=OUT, omit_background=True, clip={'x': 0, 'y': 0, 'width': WPX, 'height': HPX}); br.close()
print(OUT, WPX, HPX)
