"""Amostra da linha MINIMALISTA com foto: 1 feed 4:5, 1 story e 1 story em vídeo (7s).
Foto grande em P&B, muito preto, texto pequeno alinhado à esquerda. Uso: python3 minimal_amostra.py <pasta fontes>"""
import os, sys, base64, subprocess, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]; OUT = R + '/perfil/amostra-minimal'; os.makedirs(OUT, exist_ok=True)
FOTO, CX, HF = R + '/edicao-01/fotos-djs/coiote.png', .47, .23     # recorte, centro do rosto, altura da cabeça
LOGO = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
BASE, DEST, MED = '#08080a', '#ece6f4', '#a79db8'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

def foto_layer(W, H, head_h, face_x, top):
    im = Image.open(FOTO).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    sc = head_h / (HF * im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    a = im.getchannel('A'); g = ImageOps.autocontrast(ImageOps.grayscale(im.convert('RGB')), cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.15)
    rgb = Image.merge('RGB', [g.point(lambda v, k=k: round(8 + (k - 8) * v / 255)) for k in (226, 220, 236)])  # leve tom lavanda
    lay = Image.new('RGB', (W, H), BASE); lay.paste(rgb, (round(face_x * W - CX * im.width), top), a)
    fade = Image.linear_gradient('L').resize((W, H)).point(lambda v: 0 if v < 120 else min(255, round((v - 120) * 2.6)))
    lay = Image.composite(Image.new('RGB', (W, H), BASE), lay, fade)                 # some pro preto embaixo
    side = Image.linear_gradient('L').rotate(90, expand=True).resize((W, H)).point(lambda v: max(0, 150 - round(v * 1.6)))
    return Image.composite(Image.new('RGB', (W, H), BASE), lay, side)                # e um pouco à esquerda

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1.02;letter-spacing:-.01em}}
.m{{position:absolute;font-family:SM;font-weight:700;color:{MED};letter-spacing:.26em;text-transform:uppercase;white-space:nowrap}}
.r{{position:absolute;height:1px;background:{MED};opacity:.5}}"""

def shot(pg, W, H, html, path):
    pg.set_viewport_size({'width': W, 'height': H}); pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
    pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250); pg.screenshot(path=path, omit_background=True)

def grain(im, seed=7):
    random.seed(seed); n = Image.effect_noise(im.size, 22).convert('RGB'); return Image.blend(im, ImageChops.overlay(im, n), .12)

logo = lambda x, y, w: f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>"
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=2)
    # ---------- FEED 4:5 ----------
    W, H = 1080, 1350
    shot(pg, W, H, logo(72, 70, 150) + f"""<div class='m' style='right:72px;top:92px;font-size:15px'>toda quinta</div>
<div class='m' style='left:72px;top:956px;font-size:19px;color:{DEST}'>bally club · 22h</div>
<div class='t' style='left:68px;top:1000px;font-size:92px'>quinta,<br>por que não?</div>
<div class='r' style='left:72px;top:1218px;width:120px'></div>
<div class='m' style='left:72px;top:1246px;font-size:17px'>open gin 22h às 23h · lista vip até 00h</div>""", OUT + '/_txt.png')
    bg = foto_layer(W * 2, H * 2, 330 * 2, .66, 150 * 2)
    bg.paste(Image.open(OUT + '/_txt.png'), (0, 0), Image.open(OUT + '/_txt.png')); grain(bg).save(OUT + '/amostra_feed_minimal.png')
    # ---------- STORY (camadas separadas pro vídeo) ----------
    W, H = 1080, 1920
    L = [logo(72, 250, 170) + f"<div class='m' style='right:72px;top:280px;font-size:16px'>toda quinta</div>",
         f"<div class='m' style='left:72px;top:1206px;font-size:21px;color:{DEST}'>bally club · 22h</div><div class='t' style='left:68px;top:1256px;font-size:104px'>quinta,<br>por que não?</div>",
         f"<div class='r' style='left:72px;top:1500px;width:130px'></div><div class='m' style='left:72px;top:1530px;font-size:19px'>open gin 22h às 23h · lista vip até 00h</div>"]
    pg.close(); pg = br.new_page(device_scale_factor=1)
    for i, h in enumerate(L): shot(pg, W, H, h, f'{OUT}/_l{i}.png')
    br.close()
sbg = foto_layer(1080, 1920, 430, .64, 330); sbg.save(OUT + '/_sbg.png')
st = sbg.copy()
for i in range(3): l = Image.open(f'{OUT}/_l{i}.png'); st.paste(l, (0, 0), l)
grain(st).save(OUT + '/amostra_story_minimal.png')
# ---------- STORY EM VÍDEO: foto aproxima devagar, textos entram um a um ----------
fa = lambda st: f"format=rgba,fade=t=in:st={st}:d=0.7:alpha=1"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', '7', '-r', '30', '-i', OUT + '/_sbg.png'] +
    sum([['-loop', '1', '-t', '7', '-r', '30', '-i', f'{OUT}/_l{i}.png'] for i in range(3)], []) + ['-filter_complex',
    "[0:v]scale=1296:2304,zoompan=z='1+0.06*on/210':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,fade=t=in:st=0:d=1.2[b];"
    f"[1:v]{fa(0.6)}[a];[2:v]{fa(1.6)}[c];[3:v]{fa(2.8)}[d];"
    "[b][a]overlay[x];[x][c]overlay[y];[y][d]overlay,noise=alls=5:allf=t,fade=t=out:st=6.5:d=0.5,format=yuv420p[v]",
    '-map', '[v]', '-t', '7', '-c:v', 'libx264', '-crf', '18', '-maxrate', '10M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    OUT + '/amostra_story_minimal.mp4'], check=True)
for f in os.listdir(OUT):
    if f.startswith('_'): os.remove(OUT + '/' + f)
print(os.listdir(OUT))
