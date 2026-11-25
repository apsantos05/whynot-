"""Gorro chapado (sem efeito 3D), no estilo da tipografia do logo: silhueta limpa, pequeno e inclinado no X.
Uso: python3 xmas_gorro_flat.py <pasta logo> <variante: ouro|verm> <saida_prefixo>"""
import sys
from playwright.sync_api import sync_playwright
P, VAR, OUT = sys.argv[1:4]
base = open(f'{P}/xmas_logo_C_base.svg').read()
# gorro desenhado num quadro local (0,0 = centro da aba), depois posicionado no braço direito do X
corpo = 'M-150,-8 C-140,-120 -70,-205 30,-228 C120,-248 200,-205 238,-120 C252,-88 258,-52 256,-20 C236,-62 205,-96 168,-100 C120,-104 128,-50 150,-8 Z'
aba = 'M-178,-30 Q-180,-52 -158,-54 L158,-54 Q180,-52 178,-30 L178,18 Q180,40 158,42 L-158,42 Q-180,40 -178,18 Z'
if VAR == 'ouro':
    fc, fa, fp, extra = 'url(#ouro)', '#fbf6ee', '#fbf6ee', ''
    fc = '#d0142c'; fa = 'url(#ouro)'; fp = 'url(#ouro)'
else:
    fc, fa, fp, extra = '#d0142c', '#fbf6ee', '#fbf6ee', ''
HAT = (f'<g id="gorro" transform="translate(560,392) rotate(14) scale(.78)">'
       f'<path d="{corpo}" fill="{fc}"/>'
       f'<path d="M150,-8 C128,-50 120,-104 168,-100 C140,-80 140,-40 150,-8 Z" fill="#000" opacity=".22"/>'
       f'<path d="{aba}" fill="{fa}"/>'
       f'<circle cx="262" cy="-8" r="44" fill="{fp}"/></g>')
svg = base.replace('</svg>', HAT + '</svg>')
open(f'{P}/{OUT}.svg', 'w').write(svg)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 2400, 'height': 1620})
    pg.set_content(f"<body style='margin:0'>{svg}</body>"); pg.screenshot(path=f'{P}/{OUT}_transparente.png', omit_background=True)
    pg.set_content(f"<body style='margin:0;background:radial-gradient(circle at 50% 45%,#8a0a1c,#3a030b)'>{svg}</body>"); pg.screenshot(path=f'{P}/{OUT}_previa.jpg', type='jpeg', quality=92)
    br.close()
