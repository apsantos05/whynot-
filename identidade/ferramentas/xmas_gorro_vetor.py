"""Gorro de Papai Noel desenhado em vetor (sem imagem de terceiros), vestido no X do logo XMAS PARTY.
Lê xmas_logo_C_base.svg e grava xmas_logo_D_gorro.svg + prévias.
Uso: python3 xmas_gorro_vetor.py <pasta logo> <rot_graus> <sufixo>"""
import sys, math, random, re
from playwright.sync_api import sync_playwright
P, ROT, SUF = sys.argv[1], float(sys.argv[2]), sys.argv[3]
base = open(f'{P}/xmas_logo_C_base.svg').read()

def felpa(cx, cy, rx, ry, n, amp, seed):
    """contorno fofo: elipse/retângulo arredondado com bolinhas no contorno"""
    random.seed(seed); pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        # superelipse (cara de faixa com cantos redondos)
        c, s = math.cos(t), math.sin(t)
        x = cx + rx * math.copysign(abs(c) ** .45, c); y = cy + ry * math.copysign(abs(s) ** .45, s)
        pts.append((x, y))
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        k = amp * (.6 + .8 * random.random())
        # bolinha para fora: controle deslocado na normal externa
        nx, ny = dy / L, -dx / L
        d += f' Q{mx + nx * k:.1f},{my + ny * k:.1f} {b[0]:.1f},{b[1]:.1f}'
    return d + ' Z'

def bola(cx, cy, r, n, amp, seed):
    random.seed(seed); pts = [(cx + r * math.cos(2*math.pi*i/n), cy + r * math.sin(2*math.pi*i/n)) for i in range(n)]
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]; mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
        dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy); k = amp*(.6+.8*random.random())
        d += f' Q{mx + dy/L*k:.1f},{my - dx/L*k:.1f} {b[0]:.1f},{b[1]:.1f}'
    return d + ' Z'

# X ocupa x 169–701, topo y=420. Aba centrada no topo do X.
CX, CY = 437, 418
corpo = ('M182,400 C196,262 300,150 452,118 C590,90 720,140 808,262 '
         'C826,288 842,318 850,348 '          # ponta caindo à direita
         'C812,322 772,302 738,300 C700,298 690,340 694,400 Z')
dobra = 'M738,300 C770,262 800,262 832,300 C812,286 786,280 760,296 Z'   # sombra da dobra
brilho = 'M250,360 C268,262 340,190 440,158 C350,210 300,290 286,372 Z'
HAT = f'''
<defs>
 <linearGradient id="gv" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#f0383f"/><stop offset=".45" stop-color="#c8102a"/><stop offset="1" stop-color="#6e0614"/></linearGradient>
 <radialGradient id="gf" cx=".42" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f7efe2"/><stop offset="1" stop-color="#d9cbb3"/></radialGradient>
 <filter id="sb" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
 <filter id="fz"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>
  <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .48  0 0 0 0 .38  0 0 0 -1.1 .62"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>
<g id="gorro" transform="rotate({ROT} {CX} {CY})">
 <ellipse cx="{CX+10}" cy="{CY+58}" rx="300" ry="34" fill="#000" opacity=".45" filter="url(#sb)"/>
 <path d="{corpo}" fill="url(#gv)" stroke="#5a0410" stroke-width="3"/>
 <path d="{brilho}" fill="#ff6b6b" opacity=".28"/>
 <path d="{dobra}" fill="#4a030c" opacity=".55"/>
 <path d="{bola(862, 360, 62, 22, 14, 7)}" fill="url(#gf)"/>
 <path d="{bola(862, 360, 62, 22, 14, 7)}" filter="url(#fz)" fill="#fff"/>
 <path d="{felpa(CX, CY, 292, 62, 46, 15, 3)}" fill="url(#gf)"/>
 <path d="{felpa(CX, CY, 292, 62, 46, 15, 3)}" filter="url(#fz)" fill="#fff"/>
</g>'''
svg = base.replace('</svg>', HAT + '</svg>')
open(f'{P}/xmas_logo_D_gorro{SUF}.svg', 'w').write(svg)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 2400, 'height': 1620})
    pg.set_content(f"<body style='margin:0;background:transparent'>{svg}</body>"); pg.screenshot(path=f'{P}/xmas_logo_D_gorro{SUF}_transparente.png', omit_background=True)
    pg.set_content(f"<body style='margin:0;background:radial-gradient(circle at 50% 45%,#8a0a1c,#3a030b)'>{svg}</body>"); pg.screenshot(path=f'{P}/xmas_logo_D_gorro{SUF}_previa.jpg', type='jpeg', quality=92)
    br.close()
print('ok')
