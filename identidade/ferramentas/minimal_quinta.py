"""Linha MINIMALISTA da quinta, por que não? — foto de ambiente em duotone lavanda, muito preto, texto pequeno à esquerda.
Gera feed 4:5 (2x), story 1080x1920 e story em vídeo (7s) de cada peça.
Uso: python3 minimal_quinta.py <pasta fontes> <pasta fotos stock>   (as fotos do Adobe Stock ficam FORA do repositório)"""
import os, sys, base64, subprocess, random
from PIL import Image, ImageOps, ImageEnhance, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD, ST = sys.argv[1], sys.argv[2]
OUT = R + '/quintas-bally/minimal'; os.makedirs(OUT, exist_ok=True)
LOGO = R + '/assets/logo/lavanda/logo-why-not-lavanda.png'
BASE, DEST, MED = (8, 8, 10), '#ece6f4', '#b3a9c4'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

def fundo(foto, W, H, foco=(.5, .5), zoom=1.0, brilho=1.0, base_em=.42):
    """cobre o quadro, duotone preto→lavanda, escurece embaixo (texto) e um pouco em cima (logo)."""
    im = Image.open(f'{ST}/AdobeStock_{foto}.jpeg').convert('RGB')
    s = max(W / im.width, H / im.height) * zoom; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(foco[0] * im.width - W / 2)), im.width - W); y = min(max(0, round(foco[1] * im.height - H / 2)), im.height - H)
    g = ImageOps.autocontrast(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), cutoff=.5)
    g = g.point(lambda v: round(255 * min(1, brilho * (v / 255) ** 1.25)))
    duo = Image.merge('RGB', [g.point(lambda v, k=k, b=b: round(b + (k - b) * v / 255)) for k, b in zip((232, 224, 246), BASE)])
    m = Image.linear_gradient('L').resize((W, H)).point(lambda v: 0 if v < 255 * base_em else min(255, round((v - 255 * base_em) * 2.4)))
    duo = Image.composite(Image.new('RGB', (W, H), BASE), duo, m)
    t = ImageOps.flip(Image.linear_gradient('L')).resize((W, H)).point(lambda v: max(0, round((v - 150) * 1.5)))
    return Image.composite(Image.new('RGB', (W, H), BASE), duo, t)

def grao(im, seed=7, f=.13):
    random.seed(seed); n = Image.effect_noise(im.size, 24).convert('RGB'); return Image.blend(im, ImageChops.overlay(im, n), f)

CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:transparent;position:relative;overflow:hidden}}
.t{{position:absolute;font-family:Fr;font-style:italic;font-weight:420;color:{DEST};line-height:1.02;letter-spacing:-.01em}}
.m{{position:absolute;font-family:SM;font-weight:700;color:{MED};letter-spacing:.26em;text-transform:uppercase;white-space:nowrap}}
.r{{position:absolute;height:1px;background:{MED};opacity:.55}}"""
logo = lambda x, y, w: f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>"

def camadas(W, H, kicker, titulo, info, canto, base_y, fs):
    """3 camadas (logo+canto, título, linha+info) — separadas pra entrarem uma a uma no vídeo."""
    n = titulo.count('<br>') + 1; ty = base_y - n * fs * 1.02
    top = 250 if H == 1920 else 70
    return [logo(72, top, 160 if H == 1920 else 150) + f"<div class='m' style='right:72px;top:{top+26}px;font-size:{17 if H==1920 else 16}px'>{canto}</div>",
            f"<div class='m' style='left:72px;top:{ty-46:.0f}px;font-size:{21 if H==1920 else 19}px;color:{DEST}'>{kicker}</div>"
            f"<div class='t' style='left:68px;top:{ty:.0f}px;font-size:{fs}px'>{titulo}</div>",
            f"<div class='r' style='left:72px;top:{base_y+34}px;width:130px'></div>"
            f"<div class='m' style='left:72px;top:{base_y+62}px;font-size:{19 if H==1920 else 17}px'>{info}</div>"]

def render(pg, W, H, html, path, sf):
    pg.set_viewport_size({'width': W, 'height': H}); pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}</style>{html}")
    pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(200); pg.screenshot(path=path, omit_background=True)

PECAS = [  # nome, foto, foco feed, foco story, zoom story, brilho, kicker, título, info, canto
 ('toda-quinta', '175742652', (.5, .42), (.5, .45), 1.0, 1.0, 'bally club · 22h', 'quinta,<br>por que não?', 'open gin 22h às 23h · lista vip até 00h', 'toda quinta'),
 ('open-gin', '1885683718', (.5, .62), (.5, .62), 1.0, .85, 'toda quinta · bally club', 'open gin.', '22h às 23h · quem chega cedo, brinda', 'quinta, por que não?'),
 ('lista-vip', '354468011', (.55, .5), (.6, .5), 1.0, 1.25, 'toda quinta · bally club', 'lista VIP<br>até 00h.', 'nome na lista pelo grupo · link na bio', 'quinta, por que não?'),
]
with sync_playwright() as p:
    br = p.chromium.launch(); p2 = br.new_page(device_scale_factor=2); p1 = br.new_page(device_scale_factor=1)
    for nome, foto, ff, fs_, zs, bri, kicker, titulo, info, canto in PECAS:
        # FEED 4:5 @2x
        W, H = 1080, 1350; L = camadas(W, H, kicker, titulo, info, canto, 1180, 96)
        render(p2, W, H, ''.join(L), OUT + '/_t.png', 2); t = Image.open(OUT + '/_t.png')
        bg = fundo(foto, W * 2, H * 2, ff, 1.0, bri); bg.paste(t, (0, 0), t); grao(bg).save(f'{OUT}/feed_{nome}.png')
        # STORY 1080x1920 + vídeo
        W, H = 1080, 1920; L = camadas(W, H, kicker, titulo, info, canto, 1490, 108)
        for i, h in enumerate(L): render(p1, W, H, h, f'{OUT}/_l{i}.png', 1)
        big = fundo(foto, 1296, 2304, fs_, zs, bri, .40); big.save(OUT + '/_big.png')
        st = big.resize((1080, 1920), Image.LANCZOS)
        for i in range(3): l = Image.open(f'{OUT}/_l{i}.png'); st.paste(l, (0, 0), l)
        grao(st).save(f'{OUT}/story_{nome}.png')
        fa = lambda s: f"format=rgba,fade=t=in:st={s}:d=0.7:alpha=1"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', '7', '-r', '30', '-i', OUT + '/_big.png'] +
            sum([['-loop', '1', '-t', '7', '-r', '30', '-i', f'{OUT}/_l{i}.png'] for i in range(3)], []) + ['-filter_complex',
            "[0:v]zoompan=z='1+0.07*on/210':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,fade=t=in:st=0:d=1.0[b];"
            f"[1:v]{fa(0.5)}[a];[2:v]{fa(1.4)}[c];[3:v]{fa(2.6)}[d];"
            "[b][a]overlay[x];[x][c]overlay[y];[y][d]overlay,noise=alls=5:allf=t,fade=t=out:st=6.5:d=0.5,format=yuv420p[v]",
            '-map', '[v]', '-t', '7', '-c:v', 'libx264', '-crf', '18', '-maxrate', '10M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            f'{OUT}/story_{nome}.mp4'], check=True)
        print(nome)
    br.close()
for f in os.listdir(OUT):
    if f.startswith('_'): os.remove(OUT + '/' + f)
