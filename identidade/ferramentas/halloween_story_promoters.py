"""Story recrutamento de promoters: olho observando + 25 promoters. 2160x3840 (@2x)."""
import os, sys, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S); import eye as EYE
O = '/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F = O + '/hwb/fonts'; b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
FOOT = os.path.join(S, '..', 'patro', 'rodape_patrocinadores_2160.png')
W, H = 2160, 3840; DOC = '1610_story_promoters-25-vagas'
D = os.path.join(S, DOC); os.makedirs(D, exist_ok=True); layers = []
def add(name, im, blend=None, opacity=1, text=None):
    p = os.path.join(D, f'{len(layers):02d}.png'); im.save(p); d = {'name': name, 'png': p, 'blend': blend, 'opacity': opacity}
    if text: d['text'] = text
    layers.append(d)
add('Fundo', Image.new('RGBA', (W, H), (11, 7, 6, 255)))
EY = 1250
gm = Image.new('L', (W, H), 0); ImageDraw.Draw(gm).ellipse((W/2-900, EY-560, W/2+900, EY+560), fill=150); gm = gm.filter(ImageFilter.GaussianBlur(300))
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gl.paste((122, 58, 22, 255), (0, 0), gm); add('Brilho brasa (tela)', gl, blend='screen', opacity=0.7)
ey = EYE.eye(W=1900, H=620, r_iris=190).filter(ImageFilter.GaussianBlur(3))
fm = Image.new('L', ey.size, 0); ImageDraw.Draw(fm).ellipse((60, 120, ey.width-60, ey.height-120), fill=255); fm = fm.filter(ImageFilter.GaussianBlur(95))
ey.putalpha(ImageChops.multiply(ey.split()[3], fm))
el = Image.new('RGBA', (W, H), (0, 0, 0, 0)); el.alpha_composite(ey, ((W-1900)//2, EY-310)); add('Olho observando', el, opacity=0.8)
vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-500, -300, W+500, H+300), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(420))
add('Vinheta', Image.composite(Image.new('RGBA', (W, H), (255, 255, 255, 255)), Image.new('RGBA', (W, H), (36, 24, 18, 255)), vg), blend='multiply')
CSS = (f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
       f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center}}")
T = dict(logo_y=300, h1_y=1720, n_y=2000, p_y=2440, info_y=2700, cta_y=2900, foot_y=3230)
items = {
 'logo': f"<img src='data:image/png;base64,{b64(O+'/hwb/out/_logo_reto.png')}' style='position:absolute;left:{(W-640)//2}px;top:{T['logo_y']}px;width:640px'>",
 'h1': f"<div class=c style=\"top:{T['h1_y']}px;font-family:Fr;font-style:italic;font-size:128px;color:#efe4d0;text-shadow:0 0 40px rgba(196,165,130,.25)\">estamos de olho em você.</div>",
 'n': f"<div class=c style=\"top:{T['n_y']}px;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:440px;line-height:1;color:#efe4d0\">25</div>",
 'p': f"<div class=c style=\"top:{T['p_y']}px;font-family:Fr;font-style:italic;font-size:150px;color:#efe4d0\">promoters.</div>",
 'info': f"<div class=c style=\"top:{T['info_y']}px;font-family:SM;font-weight:700;font-size:48px;letter-spacing:.34em;text-indent:.34em;color:#c4a582\">HALLOWEEN · 02.11 · THE WEEK</div>",
 'cta': f"<div style=\"position:absolute;left:50%;transform:translateX(-50%);top:{T['cta_y']}px;border:3px solid rgba(196,165,130,.7);border-radius:999px;padding:34px 70px;font-family:SM;font-weight:700;font-size:44px;letter-spacing:.3em;color:#efe4d0;white-space:nowrap\">RESPONDA ESTE STORY</div>",
}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for k, b in items.items():
        pg.set_content(f"<style>{CSS}</style>{b}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{D}/_{k}.png', omit_background=True)
    br.close()
im = lambda k: Image.open(f'{D}/_{k}.png').convert('RGBA')
add('Logo why not? halloween', im('logo'))
add('Frase · estamos de olho em você.', im('h1'), text={'text': 'estamos de olho em você.', 'font': 'Fraunces-Italic', 'size': 128, 'color': '#efe4d0', 'x': W/2, 'y': T['h1_y']+102, 'ls': 0, 'anchor': 'middle'})
add('Número · 25', im('n'), text={'text': '25', 'font': 'Fraunces-Black', 'size': 440, 'color': '#efe4d0', 'x': W/2, 'y': T['n_y']+343, 'ls': 0, 'anchor': 'middle'})
add('Frase · promoters.', im('p'), text={'text': 'promoters.', 'font': 'Fraunces-Italic', 'size': 150, 'color': '#efe4d0', 'x': W/2, 'y': T['p_y']+120, 'ls': 0, 'anchor': 'middle'})
add('Info · HALLOWEEN · 02.11 · THE WEEK', im('info'), text={'text': 'HALLOWEEN · 02.11 · THE WEEK', 'font': 'SpaceMono-Bold', 'size': 48, 'color': '#c4a582', 'x': W/2, 'y': T['info_y']+48, 'ls': .34, 'anchor': 'middle'})
add('Botão · RESPONDA ESTE STORY', im('cta'))
ft = Image.open(FOOT).convert('RGBA'); fl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl.alpha_composite(ft, ((W-ft.width)//2, T['foot_y'])); add('Patrocinadores (rodapé)', fl)
random.seed(9); n = Image.effect_noise((W, H), 22).convert('L')
add('Grão (sobrepor · 18%)', Image.merge('RGBA', (n, n, n, Image.new('L', (W, H), 255))), blend='overlay', opacity=0.18)
base = Image.open(layers[0]['png']).convert('RGB')
for d in layers[1:]:
    i = Image.open(d['png']).convert('RGBA'); a = i.split()[3].point(lambda v: v*d['opacity']); rgb = i.convert('RGB')
    if d['blend'] == 'multiply': rgb = ImageChops.multiply(base, rgb)
    elif d['blend'] == 'screen': rgb = ImageChops.screen(base, rgb)
    elif d['blend'] == 'overlay': rgb = ImageChops.overlay(base, rgb)
    base = Image.composite(rgb, base, a)
base.save(D+'/_composite.png'); base.resize((1080, 1920), Image.LANCZOS).save(f'{S}/{DOC}.png'); base.resize((432, 768)).save(S+'/_prev.png')
json.dump({DOC: {'width': W, 'height': H, 'layers': layers}}, open(S+'/manifest.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
