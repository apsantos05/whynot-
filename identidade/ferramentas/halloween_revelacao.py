"""Revelação 16/10: porta + 02.11 · 17h · The Week JK + rodapé patrocinadores. Feed 4:5 e story 9:16 (@2x).
Gera camadas + manifest para halloween_teaser_psd.js."""
import os, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__))
O = '/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
FOOT = os.path.join(S, '..', 'patro', 'rodape_patrocinadores_2160.png')
F = O + '/hwb/fonts'; b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
CSS = (f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F + '/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F + '/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F + '/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
       "html,body{margin:0;background:transparent}.c{position:absolute;left:0;right:0;text-align:center}")
LOGO = O + '/hwb/out/_logo_reto.png'
PH = O + '/hwf/photo-1577926373616-dc964aae15bd.png'

def build(doc, W, H, L):
    D = os.path.join(S, doc); os.makedirs(D, exist_ok=True); layers = []
    def add(name, im, blend=None, opacity=1, text=None):
        p = os.path.join(D, f'{len(layers):02d}.png'); im.save(p)
        d = {'name': name, 'png': p, 'blend': blend, 'opacity': opacity}
        if text: d['text'] = text
        layers.append(d)
    add('Fundo', Image.new('RGBA', (W, H), (11, 7, 6, 255)))
    ph = Image.open(PH).convert('RGB'); r, g, b = ph.split()
    ph = Image.merge('RGB', (r.point(lambda v: min(255, max(0, v - 6) * 1.04)), g.point(lambda v: max(0, v - 8) * 0.98), b.point(lambda v: max(0, v - 10) * 0.82)))
    pw = L['ph_w']; ph = ph.resize((pw, round(ph.height * pw / ph.width)), Image.LANCZOS)
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).ellipse((120, 60, ph.width - 120, ph.height - 60), fill=255); m = m.filter(ImageFilter.GaussianBlur(200))
    fo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl = ph.convert('RGBA'); fl.putalpha(m); fo.alpha_composite(fl, ((W - pw) // 2, L['ph_y']))
    add('FOTO · porta (Unsplash)', fo)
    gm = Image.new('L', (W, H), 0); cy = L['ph_y'] + int(ph.height * 0.45)
    ImageDraw.Draw(gm).ellipse((W/2 - 520, cy - 520, W/2 + 520, cy + 420), fill=130); gm = gm.filter(ImageFilter.GaussianBlur(240))
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gl.paste((122, 58, 22, 255), (0, 0), gm)
    add('Brilho brasa (tela)', gl, blend='screen', opacity=0.55)
    gr = Image.linear_gradient('L').resize((W, H)); y0 = L['dark_from'] / H * 255
    gr = gr.point(lambda v: 0 if v < y0 else min(255, (v - y0) * 3.2))
    es = Image.new('RGBA', (W, H), (11, 7, 6, 255)); es.putalpha(gr); add('Escurecer base (leitura do texto)', es)
    tp = Image.linear_gradient('L').resize((W, H)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v: max(0, (v - 200) * 4))
    et = Image.new('RGBA', (W, H), (11, 7, 6, 255)); et.putalpha(tp); add('Escurecer topo (logo)', et)
    vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-500, -300, W + 500, H + 300), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(380))
    add('Vinheta', Image.composite(Image.new('RGBA', (W, H), (255, 255, 255, 255)), Image.new('RGBA', (W, H), (36, 24, 18, 255)), vg), blend='multiply')
    items = {
        'logo': f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W - L['logo_w'])//2}px;top:{L['logo_y']}px;width:{L['logo_w']}px'>",
        'nol': f"<div class=c style=\"top:{L['nol_y']}px;font-family:Fr;font-style:italic;font-size:{L['nol_s']}px;color:#efe4d0;opacity:.9\">no one leaves.</div>",
        'date': f"<div class=c style=\"top:{L['date_y']}px;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:{L['date_s']}px;line-height:1;color:#efe4d0;letter-spacing:-.01em;text-shadow:0 0 60px rgba(196,165,130,.25)\">02.11</div>",
        'sub': f"<div class=c style=\"top:{L['sub_y']}px;font-family:Fr;font-style:italic;font-size:{L['sub_s']}px;color:#efe4d0\">a porta abre às 17h.</div>",
        'info': f"<div class=c style=\"top:{L['info_y']}px;font-family:SM;font-weight:700;font-size:{L['info_s']}px;letter-spacing:.34em;text-indent:.34em;color:#c4a582\">SEGUNDA · THE WEEK · JK RIO PRETO</div>",
    }
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
        for k, body in items.items():
            pg.set_content(f"<style>{CSS}html,body{{width:{W}px;height:{H}px}}</style>{body}")
            pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
            pg.screenshot(path=f'{D}/_{k}.png', omit_background=True)
        br.close()
    im = lambda k: Image.open(f'{D}/_{k}.png').convert('RGBA')
    add('Logo why not? halloween', im('logo'))
    add('Slogan · no one leaves.', im('nol'), text={'text': 'no one leaves.', 'font': 'Fraunces-Italic', 'size': L['nol_s'], 'color': '#efe4d0', 'x': W/2, 'y': L['nol_y'] + L['nol_s']*0.8, 'ls': 0, 'anchor': 'middle'})
    add('Data · 02.11', im('date'), text={'text': '02.11', 'font': 'Fraunces-Black', 'size': L['date_s'], 'color': '#efe4d0', 'x': W/2, 'y': L['date_y'] + L['date_s']*0.78, 'ls': -.01, 'anchor': 'middle'})
    add('Frase · a porta abre às 17h.', im('sub'), text={'text': 'a porta abre às 17h.', 'font': 'Fraunces-Italic', 'size': L['sub_s'], 'color': '#efe4d0', 'x': W/2, 'y': L['sub_y'] + L['sub_s']*0.8, 'ls': 0, 'anchor': 'middle'})
    add('Info · SEGUNDA · THE WEEK · JK RIO PRETO', im('info'), text={'text': 'SEGUNDA · THE WEEK · JK RIO PRETO', 'font': 'SpaceMono-Bold', 'size': L['info_s'], 'color': '#c4a582', 'x': W/2, 'y': L['info_y'] + L['info_s'], 'ls': .34, 'anchor': 'middle'})
    ft = Image.open(FOOT).convert('RGBA'); fl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fl.alpha_composite(ft, ((W - ft.width) // 2, L['foot_y']))
    add('Patrocinadores (rodapé)', fl)
    random.seed(4); n = Image.effect_noise((W, H), 22).convert('L')
    add('Grão (sobrepor · 18%)', Image.merge('RGBA', (n, n, n, Image.new('L', (W, H), 255))), blend='overlay', opacity=0.18)
    base = Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        i = Image.open(d['png']).convert('RGBA'); a = i.split()[3].point(lambda v: v * d['opacity']); rgb = i.convert('RGB')
        if d['blend'] == 'multiply': rgb = ImageChops.multiply(base, rgb)
        elif d['blend'] == 'screen': rgb = ImageChops.screen(base, rgb)
        elif d['blend'] == 'overlay': rgb = ImageChops.overlay(base, rgb)
        base = Image.composite(rgb, base, a)
    base.save(D + '/_composite.png'); base.resize((W // 2, H // 2), Image.LANCZOS).save(f'{S}/{doc}.png')
    base.resize((W // 5, H // 5)).save(f'{S}/_prev_{doc}.png')
    return {doc: {'width': W, 'height': H, 'layers': layers}}

man = {}
man.update(build('1610_feed_revelacao-02-11', 2160, 2700, dict(ph_w=1560, ph_y=40, dark_from=1450, logo_w=560, logo_y=140, nol_y=315, nol_s=66,
       date_y=1640, date_s=360, sub_y=2030, sub_s=112, info_y=2215, info_s=44, foot_y=2470)))
man.update(build('1610_story_revelacao-02-11', 2160, 3840, dict(ph_w=1900, ph_y=330, dark_from=2200, logo_w=640, logo_y=300, nol_y=500, nol_s=76,
       date_y=2280, date_s=420, sub_y=2740, sub_s=128, info_y=2950, info_s=50, foot_y=3230)))
json.dump(man, open(S + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
