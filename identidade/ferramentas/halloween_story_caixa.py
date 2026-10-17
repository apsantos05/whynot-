"""Story caixa de perguntas: 'qual vai ser a sua fantasia?' — máscara + espaço para a figurinha. 2160x3840 (@2x)."""
import os, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from playwright.sync_api import sync_playwright
S = os.path.dirname(os.path.abspath(__file__))
O = '/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F = O + '/hwb/fonts'; b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
FOOT = os.path.join(S, '..', 'patro', 'rodape_patrocinadores_2160.png')
W, H = 2160, 3840; DOC = '1710_story_caixa-qual-sua-fantasia'
D = os.path.join(S, DOC); os.makedirs(D, exist_ok=True); layers = []
def add(name, im, blend=None, opacity=1, text=None):
    p = os.path.join(D, f'{len(layers):02d}.png'); im.save(p); d = {'name': name, 'png': p, 'blend': blend, 'opacity': opacity}
    if text: d['text'] = text
    layers.append(d)
add('Fundo', Image.new('RGBA', (W, H), (11, 7, 6, 255)))
ph = Image.open(O + '/hwf/photo-1640869444601-e791c41bae6b.png').convert('RGB')
ph = ph.crop((1015 - 640, 160, 1015 + 640, 1060))
g = ImageOps.grayscale(ph).point(lambda v: max(0, v - 10) * 1.05)
ph = ImageOps.colorize(g, black=(9, 6, 5), mid=(122, 86, 58), white=(228, 214, 190), midpoint=118)
pw = 1700; ph = ph.resize((pw, round(ph.height * pw / ph.width)), Image.LANCZOS)
m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).ellipse((80, 60, ph.width - 80, ph.height - 60), fill=255); m = m.filter(ImageFilter.GaussianBlur(170))
fo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl = ph.convert('RGBA'); fl.putalpha(m); fo.alpha_composite(fl, ((W - pw) // 2, 560))
add('FOTO · máscara (Unsplash)', fo)
gm = Image.new('L', (W, H), 0); ImageDraw.Draw(gm).ellipse((W/2 - 700, 700, W/2 + 700, 1600), fill=120); gm = gm.filter(ImageFilter.GaussianBlur(260))
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gl.paste((122, 58, 22, 255), (0, 0), gm); add('Brilho brasa (tela)', gl, blend='screen', opacity=0.6)
vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-500, -300, W + 500, H + 300), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(420))
add('Vinheta', Image.composite(Image.new('RGBA', (W, H), (255, 255, 255, 255)), Image.new('RGBA', (W, H), (36, 24, 18, 255)), vg), blend='multiply')
CSS = (f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
       f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center}}")
T = dict(logo_y=280, q_y=1720, hint_y=2120, box_y=2240, info_y=2980, foot_y=3240)
items = {
 'logo': f"<img src='data:image/png;base64,{b64(O+'/hwb/out/_logo_reto.png')}' style='position:absolute;left:{(W-640)//2}px;top:{T['logo_y']}px;width:640px'>",
 'q': f"<div class=c style=\"top:{T['q_y']}px;font-family:Fr;font-style:italic;font-size:150px;line-height:1.12;color:#efe4d0;text-shadow:0 0 40px rgba(196,165,130,.25)\">qual vai ser<br>a sua fantasia?</div>",
 'hint': f"<div class=c style=\"top:{T['hint_y']}px;font-family:SM;font-weight:700;font-size:40px;letter-spacing:.34em;text-indent:.34em;color:#c4a582\">CONTA PRA GENTE ↓</div>",
 'box': f"<div style=\"position:absolute;left:{(W-1300)//2}px;top:{T['box_y']}px;width:1300px;height:620px;border:4px dashed rgba(196,165,130,.45);border-radius:56px\"></div>",
 'info': f"<div class=c style=\"top:{T['info_y']}px;font-family:SM;font-weight:700;font-size:44px;letter-spacing:.34em;text-indent:.34em;color:#efe4d0;opacity:.8\">02.11 · 17H · THE WEEK</div>",
}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
    for k, b in items.items():
        pg.set_content(f"<style>{CSS}</style>{b}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{D}/_{k}.png', omit_background=True)
    br.close()
im = lambda k: Image.open(f'{D}/_{k}.png').convert('RGBA')
add('Logo why not? halloween', im('logo'))
add('Pergunta · qual vai ser a sua fantasia?', im('q'))
add('Chamada · CONTA PRA GENTE', im('hint'), text={'text': 'CONTA PRA GENTE ↓', 'font': 'SpaceMono-Bold', 'size': 40, 'color': '#c4a582', 'x': W/2, 'y': T['hint_y']+40, 'ls': .34, 'anchor': 'middle'})
add('Guia da figurinha (apagar antes de postar se quiser)', im('box'))
add('Info · 02.11 · 17H · THE WEEK', im('info'), text={'text': '02.11 · 17H · THE WEEK', 'font': 'SpaceMono-Bold', 'size': 44, 'color': '#efe4d0', 'x': W/2, 'y': T['info_y']+44, 'ls': .34, 'anchor': 'middle'})
ft = Image.open(FOOT).convert('RGBA'); fl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl.alpha_composite(ft, ((W-ft.width)//2, T['foot_y'])); add('Patrocinadores (rodapé)', fl)
random.seed(11); n = Image.effect_noise((W, H), 22).convert('L')
add('Grão (sobrepor · 18%)', Image.merge('RGBA', (n, n, n, Image.new('L', (W, H), 255))), blend='overlay', opacity=0.18)
def comp(skip=()):
    base = Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        if d['name'] in skip: continue
        i = Image.open(d['png']).convert('RGBA'); a = i.split()[3].point(lambda v: v*d['opacity']); rgb = i.convert('RGB')
        if d['blend'] == 'multiply': rgb = ImageChops.multiply(base, rgb)
        elif d['blend'] == 'screen': rgb = ImageChops.screen(base, rgb)
        elif d['blend'] == 'overlay': rgb = ImageChops.overlay(base, rgb)
        base = Image.composite(rgb, base, a)
    return base
c = comp(); c.save(D+'/_composite.png'); c.resize((1080, 1920), Image.LANCZOS).save(f'{S}/{DOC}.png')
comp(skip=('Guia da figurinha (apagar antes de postar se quiser)',)).resize((1080, 1920), Image.LANCZOS).save(f'{S}/{DOC}_sem-guia.png')
c.resize((432, 768)).save(S+'/_prev.png')
json.dump({DOC: {'width': W, 'height': H, 'layers': layers}}, open(S+'/manifest.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
