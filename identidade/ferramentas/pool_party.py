"""Pool party why not? na casa alugada: story 1080x1920 e feed 1080x1350 com a foto da piscina.
Open cooler, mulher free, homem R$ 50. Tipografia da casa (Fraunces). Data opcional.
Uso: python3 pool_party.py <pasta fontes fraunces> ["sábado, 05.12, a partir das 16h"]"""
import os, sys, base64, random
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FD = sys.argv[1]; DATA = sys.argv[2] if len(sys.argv) > 2 else ''
P = R + '/pool-party/'; FOTO = P + 'foto_casa_piscina.jpg'; LOGO = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
sm = lambda t: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, t)))
AQUA, CREME, MED = '#8fe3ff', '#f4efe6', '#c9d6dc'
def coluna(W, H, f):
    c = Image.new('L', (1, H)); c.putdata([round(255 * min(1, max(0, f(y)))) for y in range(H)]); return c.resize((W, H))
def fundo(W, H, foco_x, esc):
    im = Image.open(FOTO).convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(foco_x * im.width - W / 2)), im.width - W); y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H)).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.12)).enhance(1.06)
    return Image.composite(Image.new('RGB', (W, H), (4, 10, 16)), im, coluna(W, H, esc))
def css(W, H):
    return f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;left:68px;font-family:Fr;font-style:italic;font-weight:440;color:{CREME};line-height:.96;letter-spacing:-.016em;white-space:nowrap;font-variation-settings:"WONK" 0;text-shadow:0 2px 30px rgba(0,0,0,.65)}}
.a{{color:{AQUA}}}
.m{{position:absolute;left:72px;font-family:FrR;font-weight:400;color:{MED};white-space:nowrap;font-variation-settings:"opsz" 14,"WONK" 0;letter-spacing:.012em;font-feature-settings:"lnum";text-shadow:0 1px 16px rgba(0,0,0,.9)}}
.c{{color:{CREME}}} .r{{position:absolute;left:72px;height:2px;width:130px;background:{AQUA}}}"""
def topo(top, w):
    return (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:72px;top:{top}px;width:{w}px'>"
            f"<div class='m' style='left:auto;right:72px;top:{top + 18}px;font-size:25px'>pool party, por que não?</div>")
def precos(y, fs, gap):
    return (f"<div class='m' style='top:{y}px;font-size:{round(fs*.36)}px'>mulher</div>"
            f"<div class='t' style='top:{y+round(fs*.5)}px;font-size:{fs}px'><span class='a'>free.</span></div>"
            f"<div class='m' style='left:560px;top:{y}px;font-size:{round(fs*.36)}px'>homem</div>"
            f"<div class='t' style='left:556px;top:{y+round(fs*.5)}px;font-size:{fs}px'>R$ 50.</div>")
dl = lambda top, fs: f"<div class='m c' style='top:{top}px;font-size:{fs}px'>{DATA}</div>" if DATA else ''
STORY = (topo(210, 150) +
  "<div class='t' style='top:300px;font-size:150px'>pool <span class='a'>party.</span></div>" +
  "<div class='m c' style='top:1240px;font-size:31px'>na casa, com piscina</div>"
  "<div class='t' style='top:1286px;font-size:120px'>open cooler.</div>"
  "<div class='r' style='top:1440px'></div>" + precos(1470, 104, 0) + dl(1655, 30))
FEED = (topo(64, 140) +
  "<div class='t' style='top:150px;font-size:168px'>pool <span class='a'>party.</span></div>" +
  "<div class='m c' style='top:850px;font-size:28px'>na casa, com piscina</div>"
  "<div class='t' style='top:890px;font-size:100px'>open cooler.</div>"
  "<div class='r' style='top:1018px'></div>" + precos(1044, 88, 0) + dl(1230, 27))
PECAS = [('story_pool-party.png', 1080, 1920, STORY, .563, lambda y: .82 * (1 - sm((y - 330) / 300)) + .74 * sm((y - 1120) / 380)),
         ('feed_pool-party.png', 1080, 1350, FEED, .563, lambda y: .72 * (1 - sm((y - 40) / 360)) + .72 * sm((y - 760) / 300))]
with sync_playwright() as p:
    br = p.chromium.launch()
    for nome, W, H, html, fx, esc in PECAS:
        pg = br.new_page(viewport={'width': W, 'height': H}); pg.set_content(f"<style>{css(W, H)}</style>{html}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300); pg.screenshot(path=P + '_t.png', omit_background=True); pg.close()
        bg = fundo(W, H, fx, esc).convert('RGBA'); bg.alpha_composite(Image.open(P + '_t.png'))
        random.seed(7); n = Image.effect_noise((W, H), 20).convert('RGB'); out = Image.blend(bg.convert('RGB'), ImageChops.overlay(bg.convert('RGB'), n), .06)
        out.save(P + nome); os.remove(P + '_t.png'); print(nome)
    br.close()
