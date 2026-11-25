"""Stories para os dias parados e para a quinta 26.11, com espaço para os stickers do Instagram.
  - s_enquete: "quinta, quem vem?" (sticker de enquete)
  - s_caixinha: "pede a sua música pra quinta" (caixinha de perguntas)
  - s_e-hoje_baruc: "é hoje." da ressaca das provas (sticker de link)
Fundos gerados no ElevenLabs (sem pessoas, sem marcas) em <pasta fundos>.
Uso: python3 stories_interativos.py <pasta fontes> <pasta fundos>"""
import os, sys, base64, random
from PIL import Image, ImageOps, ImageChops, ImageEnhance
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, BG = sys.argv[1], sys.argv[2]
OUT = R + '/quintas-bally/semanas/2026-11-26/'
W, H = 1080, 1920
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
def coluna(f):
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))

def fundo(arq, pb, escuro, base=(8, 8, 10)):
    im = Image.open(arq).convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); x = (im.width - W) // 2; im = im.crop((x, 0, x + W, H))
    if pb:   # desce o globo pra não brigar com o logo e o topo; o que sobra em cima vira preto
        c = Image.new('RGB', (W, H), base); c.paste(im, (0, 330)); im = Image.composite(c, Image.new('RGB', (W, H), base), coluna(lambda y: sm((y - 330) / 120)))
    if pb: im = ImageOps.grayscale(im).convert('RGB')
    return Image.composite(Image.new('RGB', (W, H), base), im, coluna(escuro))

def css(dest, med, acento):
    return f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:440;color:{dest};line-height:.98;letter-spacing:-.014em;white-space:nowrap;font-variation-settings:"WONK" 0;text-shadow:0 2px 30px rgba(0,0,0,.6)}}
.a{{color:{acento}}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{med};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum";text-shadow:0 1px 16px rgba(0,0,0,.8)}}
.c{{color:{dest}}} .r{{position:absolute;left:72px;height:2px;width:130px;background:{acento}}}"""

def topo(logo, canto):
    return (f"<img src='data:image/png;base64,{b64(logo)}' style='position:absolute;left:72px;top:250px;width:160px'>"
            f"<div class='m' style='left:auto;right:72px;top:268px;font-size:25px'>{canto}</div>")

LG = R + '/assets/logo/grafite/logo-why-not-grafite.png'; LL = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
LB = OUT + 'logo_baruc.png'
PECAS = [
 ('story_enquete_quem-vem.png', 'pb_2.png', True, lambda y: .15 + .80 * sm((y - 900) / 360),
  ('#efe9f7', '#b6acc8', '#c9b8ec'), topo(LL, 'quinta, por que não?') +
  "<div class='m c' style='top:1150px;font-size:31px'>quinta, 26.11, na Bally Club</div>"
  "<div class='t' style='top:1196px;font-size:150px'>quem <span class='a'>vem?</span></div>"
  "<div class='m' style='top:1372px;font-size:30px'>responde aqui embaixo, a gente quer saber.</div>"),
 ('story_caixinha_pede-a-musica.png', 'pb_2.png', True, lambda y: .15 + .80 * sm((y - 900) / 360),
  ('#efe9f7', '#b6acc8', '#c9b8ec'), topo(LL, 'quinta, por que não?') +
  "<div class='m c' style='top:1100px;font-size:31px'>a pista é sua também.</div>"
  "<div class='t' style='top:1146px;font-size:132px'>pede a sua<br><span class='a'>música.</span></div>"
  "<div class='m' style='top:1440px;font-size:30px'>os DJs da quinta vão ler.</div>"),
 ('story_e-hoje_baruc.png', 'vermelho_2.png', False, lambda y: .10 + .82 * sm((y - 820) / 420),
  ('#f5eeee', '#d9b9bd', '#e3262e'), topo(LG, 'quinta, por que não?') +
  f"<img src='data:image/png;base64,{b64(LB)}' style='position:absolute;left:72px;top:820px;width:200px;filter:drop-shadow(0 12px 40px rgba(0,0,0,.6))'>"
  "<div class='m c' style='top:1062px;font-size:31px'>ressaca das provas, com a Baruc</div>"
  "<div class='t' style='top:1108px;font-size:190px'>é <span class='a'>hoje.</span></div>"
  "<div class='m' style='top:1328px;font-size:30px'>a partir das 22h, na Bally Club.</div>"
  "<div class='m c' style='top:1372px;font-size:30px'>ingressos e lista vip no link.</div>"),
]
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for nome, bgarq, pb, esc, cores, html in PECAS:
        pg.set_content(f"<style>{css(*cores)}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=OUT + '_t.png', omit_background=True)
        bg = fundo(f'{BG}/{bgarq}', pb, esc).convert('RGBA'); bg.alpha_composite(Image.open(OUT + '_t.png'))
        random.seed(3); n = Image.effect_noise((W, H), 20).convert('RGB'); out = Image.blend(bg.convert('RGB'), ImageChops.overlay(bg.convert('RGB'), n), .06)
        out.save(OUT + nome); os.remove(OUT + '_t.png'); print(nome)
    br.close()
