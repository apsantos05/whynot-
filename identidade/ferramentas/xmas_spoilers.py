"""XMAS PARTY, stories de spoiler (1080x1920) com a cortina de veludo.
  1 fechada e 2 entreaberta: só a logo e a data (suspense)   3 contagem: "faltam N dias."
Uso: python3 xmas_spoilers.py <pasta fontes> [dias...]"""
import os, sys, base64
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FD = sys.argv[1]; DIAS = [int(d) for d in sys.argv[2:]] or [23]
P = R + '/xmas-party/spoilers/'; F = P + 'fundos/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
PF = FD + '/fontsource-playfair-display-5.3.0/package/files/'; CZ = FD + '/fontsource-cinzel-5.3.0/package/files/'
CSS = f"""@font-face{{font-family:P;font-style:italic;src:url(data:font/woff2;base64,{b64(PF+'playfair-display-latin-400-italic.woff2')})}}
@font-face{{font-family:C;src:url(data:font/woff2;base64,{b64(CZ+'cinzel-latin-400-normal.woff2')})}}
*{{margin:0}} body{{width:1080px;height:1920px;background:transparent;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.ouro{{font-family:P;font-style:italic;line-height:1.02;background:linear-gradient(180deg,#fff1c8 0%,#e8c46e 45%,#b8862b 72%,#f3d98f 100%);
 -webkit-background-clip:text;color:transparent;filter:drop-shadow(0 3px 10px rgba(0,0,0,.85))}}
.cap{{font-family:C;color:#f3e2b6;letter-spacing:.34em;padding-left:.34em;text-shadow:0 2px 3px rgba(0,0,0,.95),0 0 2px rgba(0,0,0,.8)}}
.wn{{font-family:P;font-style:italic;color:#e9cf8e;text-shadow:0 2px 6px rgba(0,0,0,.9)}}"""
TOPO = "<div class='c wn' style='top:250px;font-size:46px'>why not?</div>"
def peca(nome, fundo, html, escurece):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=P + '_t.png', omit_background=True); br.close()
    bg = Image.open(F + fundo).convert('RGB').resize((1080, 1920), Image.LANCZOS)
    # escurece o pé da imagem (onde fica o texto) com degradê suave
    g = Image.linear_gradient('L').resize((1080, 1920)).point(lambda v: int(min(255, max(0, (v - escurece[0]) * escurece[1]))))
    bg = Image.composite(Image.new('RGB', bg.size, (8, 2, 3)), bg, g).convert('RGBA')
    bg.alpha_composite(Image.open(P + '_t.png')); bg.convert('RGB').save(P + nome, quality=95); os.remove(P + '_t.png'); print(nome)

peca('story_spoiler_1_cortina-fechada.png', 'cortina_fechada.png', TOPO +
     "<div class='c ouro' style='top:1625px;font-size:150px'>18.12</div>"
     "<div class='c cap' style='top:1810px;font-size:32px'>sexta-feira</div>", (175, 2.2))
peca('story_spoiler_2_cortina-entreaberta.png', 'cortina_entreaberta.png', TOPO +
     "<div class='c ouro' style='top:1400px;font-size:170px'>18.12</div>"
     "<div class='c cap' style='top:1615px;font-size:36px'>sexta-feira</div>", (150, 1.6))
for d in DIAS:
    peca(f'story_contagem_faltam-{d}.png', 'cortina_aberta.png', TOPO +
         f"<div class='c cap' style='top:1355px;font-size:34px'>faltam</div>"
         f"<div class='c ouro' style='top:1400px;font-size:190px'>{d} dias.</div>", (170, 1.9))
