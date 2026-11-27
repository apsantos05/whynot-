"""XMAS PARTY, stories de spoiler (1080x1920) com a cortina de veludo.
  1 fechada e 2 entreaberta: só a logo e a data (suspense)   3 contagem: "faltam N dias."  + feed de chamada. Topo: why not? | The House
Uso: python3 xmas_spoilers.py <pasta fontes> [dias...]"""
import os, sys, base64
from PIL import Image, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FD = sys.argv[1]; DIAS = [int(d) for d in sys.argv[2:]] or [23]
P = R + '/xmas-party/spoilers/'; F = P + 'fundos/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
PF = FD + '/fontsource-playfair-display-5.3.0/package/files/'; CZ = FD + '/fontsource-cinzel-5.3.0/package/files/'
CSS = f"""@font-face{{font-family:P;font-style:italic;src:url(data:font/woff2;base64,{b64(PF+'playfair-display-latin-400-italic.woff2')})}}
@font-face{{font-family:C;src:url(data:font/woff2;base64,{b64(CZ+'cinzel-latin-400-normal.woff2')})}}
*{{margin:0}} body{{width:1080px;background:transparent;position:relative}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.ouro{{font-family:P;font-style:italic;line-height:1.02;background:linear-gradient(180deg,#fff1c8 0%,#e8c46e 45%,#b8862b 72%,#f3d98f 100%);
 -webkit-background-clip:text;color:transparent;filter:drop-shadow(0 3px 10px rgba(0,0,0,.85))}}
.cap{{font-family:C;color:#f3e2b6;letter-spacing:.34em;padding-left:.34em;text-shadow:0 2px 3px rgba(0,0,0,.95),0 0 2px rgba(0,0,0,.8)}}
.wn{{font-family:P;font-style:italic;color:#e9cf8e;text-shadow:0 2px 6px rgba(0,0,0,.9)}}"""
PAR = R + '/assets/parceiros/xmas_par_logos.png'   # why not? | The House
topo = lambda top=230, w=560: f"<img src='data:image/png;base64,{b64(PAR)}' style='position:absolute;left:{(1080 - w) // 2}px;top:{top}px;width:{w}px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.8))'>"
TOPO = topo()
def peca(nome, fundo, html, escurece, H=1920, y0=0):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': H})
        pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=P + '_t.png', omit_background=True); br.close()
    src = Image.open(F + fundo).convert('RGB')
    if abs(src.width / src.height - 1080 / H) < .01: bg = src.resize((1080, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 40, 2))
    else: bg = src.resize((1080, 1920), Image.LANCZOS).crop((0, y0, 1080, y0 + H))
    # escurece o pé da imagem (onde fica o texto) com degradê suave
    g = Image.linear_gradient('L').resize((1080, H)).point(lambda v: int(min(255, max(0, (v - escurece[0]) * escurece[1]))))
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
         f"<div class='c cap' style='top:1355px;font-size:34px'>{'falta' if d == 1 else 'faltam'}</div>"
         f"<div class='c ouro' style='top:1400px;font-size:190px'>{d} {'dia' if d == 1 else 'dias'}.</div>", (170, 1.9))
# dia da festa
peca('story_e-hoje.png', 'cortina_aberta.png', TOPO +
     "<div class='c ouro' style='top:1390px;font-size:200px'>é hoje.</div>", (170, 1.9))
# feed 4:5 de chamada com a cortina fechada
peca('feed_chamada_cortina-fechada.png', 'cortina_fechada.png', topo(80, 520) +
     "<div class='c ouro' style='top:1130px;font-size:118px'>18.12</div>"
     "<div class='c cap' style='top:1268px;font-size:28px'>sexta-feira</div>", (190, 2.4), H=1350, y0=500)
# feed 4:5 surpresa: só a cortina com a luz estourando pela fresta. Logos nos cantos de cima (longe da fresta), data sozinha no chão
PAR_IMG = Image.open(PAR)
def canto(lado, top, h):
    """recorta do par a logo da esquerda (why not?) ou da direita (The House) e posiciona no canto"""
    a = PAR_IMG.split()[3]; cols = [x for x in range(PAR_IMG.width) if a.crop((x, 0, x + 1, PAR_IMG.height)).getbbox()]
    gaps = [i for i in range(1, len(cols)) if cols[i] - cols[i - 1] > 40]; cut = cols[gaps[0]] - 10
    parte = PAR_IMG.crop((0, 0, cut, PAR_IMG.height) if lado == 'e' else (cut, 0, PAR_IMG.width, PAR_IMG.height)); parte = parte.crop(parte.getbbox())
    tmp = P + f'_canto_{lado}.png'; parte.save(tmp); w = round(parte.width * h / parte.height)
    pos = f"left:72px" if lado == 'e' else f"right:72px"
    return f"<img src='data:image/png;base64,{b64(tmp)}' style='position:absolute;{pos};top:{top}px;height:{h}px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.85))'>"
def centro(lado, top, h):
    t = canto(lado, top, h); return t.replace("left:72px", "left:50%;transform:translateX(-50%)").replace("right:72px", "left:50%;transform:translateX(-50%)")
TOPO_APRESENTAM = ("<div style='position:absolute;left:290px;right:290px;top:30px;height:300px;background:radial-gradient(ellipse at 50% 50%,rgba(6,1,2,.85),rgba(6,1,2,0) 72%)'></div>" +
     centro('e', 84, 50) + "<div class='c' style='top:146px;font-family:P;font-style:italic;font-size:30px;color:#e9cf8e;text-shadow:0 2px 6px rgba(0,0,0,.9)'>e</div>" +
     centro('d', 188, 62) + "<div class='c cap' style='top:270px;font-size:22px'>apresentam</div>")
peca('feed_surpresa_luz-na-cortina.png', 'cortina_luz_feed.png', TOPO_APRESENTAM +
     "<div style='position:absolute;left:220px;right:220px;top:1120px;height:220px;background:radial-gradient(ellipse at 50% 45%,rgba(6,1,2,.7),rgba(6,1,2,0) 70%)'></div>"
     "<div class='c ouro' style='top:1135px;font-size:108px'>18.12</div>"
     "<div class='c cap' style='top:1262px;font-size:24px'>sexta-feira</div>", (215, 2.0), H=1350)
for f in ('_canto_e.png', '_canto_d.png'): os.remove(P + f)
