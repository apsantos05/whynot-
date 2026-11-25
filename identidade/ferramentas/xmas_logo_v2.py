"""XMAS PARTY, rodada 2 de logos (sem gorro). Quatro direções em vetor (texto em curvas):
F bola de discoteca como enfeite de Natal | G árvore tipográfica | H X de bengala doce | I laço de presente em traço.
Uso: python3 xmas_logo_v2.py <pasta fontes> <pasta saída>"""
import os, sys, math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from playwright.sync_api import sync_playwright
FS, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
def F(d, f):
    for c in (f'{FS}/{d}/package/files/{f}',):
        if os.path.exists(c): return TTFont(c)
    raise SystemExit(f)
CINZEL = F('fontsource-cinzel-5.3.0', 'cinzel-latin-700-normal.woff2'); CINZEL9 = F('fontsource-cinzel-5.3.0', 'cinzel-latin-900-normal.woff2')
PLAYI = F('fontsource-playfair-display-5.3.0', 'playfair-display-latin-700-italic.woff2')
SCRIPT = F('fontsource-pinyon-script-5.3.0', 'pinyon-script-latin-400-normal.woff2')
ABRIL = F('fontsource-abril-fatface', 'abril-fatface-latin-400-normal.woff2')
ANTON = F('fontsource-anton', 'anton-latin-400-normal.woff2')
ITAL = F('fontsource-italiana', 'italiana-latin-400-normal.woff2')
BODONI = F('fontsource-bodoni-moda-5.3.0', 'bodoni-moda-latin-900-normal.woff2')

def largura(font, s, size, track=0):
    cmap = font.getBestCmap(); h = font['hmtx']; k = size / font['head'].unitsPerEm
    return sum(h[cmap[ord(c)]][0] for c in s if ord(c) in cmap) * k + track * (len(s) - 1)
def texto(font, s, size, x, y, track=0, anchor='start'):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); k = size / font['head'].unitsPerEm; h = font['hmtx']
    w = largura(font, s, size, track); cx = x - (w if anchor == 'end' else w / 2 if anchor == 'middle' else 0); pen = SVGPathPen(gs)
    for c in s:
        n = cmap.get(ord(c))
        if not n: continue
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, cx, y))); cx += h[n][0] * k + track
    return pen.getCommands()
def estrela(cx, cy, r, fino=.16):
    p = []
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4; rr = r if i % 2 == 0 else r * fino; p.append(f'{cx + rr*math.cos(a):.1f},{cy - rr*math.sin(a):.1f}')
    return 'M' + ' L'.join(p) + ' Z'
DEFS = """<linearGradient id="ouro" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#fff3c4"/><stop offset=".22" stop-color="#e9c46a"/><stop offset=".48" stop-color="#b8862b"/>
<stop offset=".62" stop-color="#f6dc8e"/><stop offset=".82" stop-color="#a8741f"/><stop offset="1" stop-color="#e8c873"/></linearGradient>
<pattern id="bengala" width="120" height="120" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="120" height="120" fill="#fbf6ee"/><rect width="60" height="120" fill="#d0142c"/></pattern>"""
VERM, BRANCO = '#d0142c', '#fbf6ee'
def svg(w, h, corpo): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{DEFS}</defs>{corpo}</svg>'
L = {}

# ---- F: bola de discoteca-enfeite + wordmark ----
W, H = 2600, 1400; cx, cy, r = 560, 780, 390
random.seed(11); fac = []
for i in range(14):                      # faixas de latitude
    la0, la1 = -math.pi/2 + math.pi*i/14, -math.pi/2 + math.pi*(i+1)/14
    n = max(4, round(28 * math.cos((la0+la1)/2)))
    for j in range(n):
        lo0, lo1 = -math.pi/2 + math.pi*j/n, -math.pi/2 + math.pi*(j+1)/n
        q = [(math.cos(la)*math.sin(lo), math.sin(la), math.cos(la)*math.cos(lo)) for la, lo in ((la0,lo0),(la0,lo1),(la1,lo1),(la1,lo0))]
        nz = math.cos((la0+la1)/2)*math.cos((lo0+lo1)/2); nx = math.cos((la0+la1)/2)*math.sin((lo0+lo1)/2); ny = math.sin((la0+la1)/2)
        luz = max(0, -.45*nx - .55*ny + .7*nz)       # luz vindo de cima-esquerda
        v = .25 + .75 * luz * (.7 + .3*random.random())
        if random.random() < .06: v = 1.25
        col = (round(min(255, 70 + 190*v)), round(min(255, 42 + 160*v)), round(min(255, 10 + 110*v*v)))
        pts = ' '.join(f'{cx + r*.985*x:.1f},{cy + r*.985*y:.1f}' for x, y, z in q)
        fac.append(f'<polygon points="{pts}" fill="rgb{col}" stroke="#3a2306" stroke-width="2.2"/>')
bola = (f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="#2a1804"/>' + ''.join(fac) +
        f'<path d="{estrela(cx-150, cy-170, 70, .1)}" fill="#fff"/><path d="{estrela(cx+120, cy-60, 34, .1)}" fill="#fff" opacity=".85"/>'
        f'<rect x="{cx-80}" y="{cy-r-60}" width="160" height="80" rx="12" fill="url(#ouro)"/>'
        + ''.join(f'<rect x="{cx-80}" y="{cy-r-50+k*16}" width="160" height="4" fill="#8a5d16" opacity=".6"/>' for k in range(4)) +
        f'<path d="M{cx},{cy-r-60} C{cx-50},{cy-r-150} {cx+50},{cy-r-150} {cx},{cy-r-60}" fill="none" stroke="url(#ouro)" stroke-width="14"/>')
tx = 1080
L['F_disco'] = svg(W, H, bola +
    f'<path d="{texto(PLAYI, "why not?", 96, tx+8, 520)}" fill="{BRANCO}"/>'
    f'<path d="{texto(ABRIL, "XMAS", 470, tx, 900, track=4)}" fill="url(#ouro)"/>'
    f'<path d="{texto(CINZEL, "PARTY", 150, tx+10, 1100, track=88)}" fill="{BRANCO}"/>'
    f'<path d="{texto(CINZEL, "SEXTA, 18.12", 54, tx+12, 1230, track=20)}" fill="url(#ouro)"/>')

# ---- G: árvore tipográfica ----
W, H = 2200, 2050; C = W/2
def caber(font, s, alvo, track_rel=0):
    s0 = 100; w = largura(font, s, s0, track_rel*s0); return s0 * alvo / w
sx = caber(CINZEL9, 'XMAS', 820, .04); sp = caber(CINZEL, 'PARTY', 1300, .22)
ylinha = 1520
L['G_arvore'] = svg(W, H,
    f'<path d="M{C},360 L{C-920},{ylinha} M{C},360 L{C+920},{ylinha}" stroke="url(#ouro)" stroke-width="5" fill="none"/>'
    f'<path d="M{C-960},{ylinha} L{C+960},{ylinha}" stroke="url(#ouro)" stroke-width="5"/>'
    f'<path d="{estrela(C, 300, 150, .14)}" fill="url(#ouro)"/>'
    f'<path d="{texto(PLAYI, "why not?", 104, C, 690, anchor="middle")}" fill="{BRANCO}"/>'
    f'<path d="{texto(CINZEL9, "XMAS", sx, C, 1050, track=.04*sx, anchor="middle")}" fill="url(#ouro)"/>'
    f'<path d="{texto(CINZEL, "PARTY", sp, C, 1410, track=.22*sp, anchor="middle")}" fill="{BRANCO}"/>'
    + ''.join(f'<circle cx="{C+dx}" cy="{yy}" r="16" fill="{VERM}" stroke="{BRANCO}" stroke-width="5"/>' for dx, yy in ((-250, 760), (230, 790), (-520, 1150), (500, 1130))) +
    f'<rect x="{C-110}" y="{ylinha+5}" width="220" height="110" fill="url(#ouro)"/>'
    f'<path d="{texto(CINZEL, "18.12", 64, C, ylinha+84, track=10, anchor="middle")}" fill="#5a0410"/>'
    f'<path d="{texto(CINZEL, "SEXTA-FEIRA", 50, C, ylinha+250, track=30, anchor="middle")}" fill="{BRANCO}"/>')

# ---- H: X de bengala doce ----
W, H = 2600, 1720
wX = largura(ANTON, 'X', 860); x0 = 180
L['H_bengala'] = svg(W, H,
    f'<path d="{texto(PLAYI, "why not?", 96, x0+10, 300)}" fill="{BRANCO}"/>'
    f'<path d="{texto(ANTON, "X", 860, x0, 1180)}" fill="url(#bengala)" stroke="{BRANCO}" stroke-width="6"/>'
    f'<path d="{texto(ANTON, "MAS", 860, x0+wX+24, 1180, track=24)}" fill="url(#ouro)"/>'
    f'<g transform="translate({x0+wX+600},1330) rotate(-7)"><path d="{texto(SCRIPT, "party", 400, 0, 0, anchor="middle")}" fill="{BRANCO}" stroke="#5a0410" stroke-width="10" paint-order="stroke"/></g>'
    f'<path d="{texto(CINZEL, "SEXTA, 18.12", 58, W-180, 300, track=20, anchor="end")}" fill="url(#ouro)"/>')

# ---- I: laço de presente em traço fino + Italiana ----
W, H = 2600, 1560; C = W/2
laco = (f'<g fill="none" stroke="url(#ouro)" stroke-width="9" stroke-linecap="round">'
        f'<path d="M{C},430 C{C-120},250 {C-360},220 {C-330},360 C{C-310},450 {C-120},450 {C},430"/>'
        f'<path d="M{C},430 C{C+120},250 {C+360},220 {C+330},360 C{C+310},450 {C+120},450 {C},430"/>'
        f'<path d="M{C-14},440 C{C-90},520 {C-150},580 {C-240},600"/><path d="M{C+14},440 C{C+90},520 {C+150},580 {C+240},600"/>'
        f'<path d="M140,640 L{C-430},640 M{C+430},640 L{W-140},640" stroke-width="5"/></g>'
        f'<ellipse cx="{C}" cy="432" rx="30" ry="24" fill="url(#ouro)"/>')
L['I_laco'] = svg(W, H, laco +
    f'<path d="{texto(PLAYI, "why not?", 84, C, 670, anchor="middle")}" fill="{BRANCO}"/>'
    f'<path d="{texto(ITAL, "XMAS", 520, C, 1150, track=60, anchor="middle")}" fill="url(#ouro)"/>'
    f'<g transform="translate({C+600},1370) rotate(-6)"><path d="{texto(SCRIPT, "party", 300, 0, 0, anchor="middle")}" fill="{VERM}" stroke="{BRANCO}" stroke-width="7" paint-order="stroke"/></g>'
    f'<path d="{texto(CINZEL, "SEXTA, 18.12", 54, C-560, 1330, track=22, anchor="middle")}" fill="{BRANCO}"/>')

with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page()
    for k, s in L.items():
        open(f'{OUT}/xmas_logo_{k}.svg', 'w').write(s)
        w, h = (int(v) for v in s.split('width="')[1].split('"')[0:3:2])
        w = int(s.split('width="')[1].split('"')[0]); h = int(s.split('height="')[1].split('"')[0])
        pg.set_viewport_size({'width': w, 'height': h})
        pg.set_content(f"<body style='margin:0'>{s}</body>"); pg.screenshot(path=f'{OUT}/xmas_logo_{k}_transparente.png', omit_background=True)
        pg.set_content(f"<body style='margin:0;background:radial-gradient(circle at 50% 45%,#8a0a1c,#3a030b)'>{s}</body>"); pg.screenshot(path=f'{OUT}/xmas_logo_{k}_previa.jpg', type='jpeg', quality=92)
        print(k)
    br.close()
