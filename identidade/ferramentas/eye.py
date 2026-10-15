"""Olho brilhante procedural (âmbar) para fundo das artes Halloween."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
def eye(W=1400, H=460, r_iris=150):
    cx, cy = W/2, H/2
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    # amêndoa: interseção de dois círculos
    R = (W*0.46)**2/(2*H*0.36) + H*0.36/2
    up = (xx-cx)**2 + (yy-(cy+R-H*0.36))**2 < R**2
    dn = (xx-cx)**2 + (yy-(cy-R+H*0.36))**2 < R**2
    alm = Image.fromarray(((up & dn)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))
    d = np.sqrt((xx-cx)**2 + (yy-cy)**2)
    # esclera escura e quente, mais clara perto da íris
    scl = np.clip(1 - d/(W*0.5), 0, 1)
    rgb = np.zeros((H, W, 3))
    rgb[..., 0] = 11 + 16*scl; rgb[..., 1] = 7 + 9*scl; rgb[..., 2] = 6 + 4*scl
    # íris com fibras radiais
    ang = np.arctan2(yy-cy, xx-cx)
    rng = np.random.default_rng(5); nz = np.array(Image.fromarray((rng.random((H//4, W//4))*255).astype(np.uint8)).resize((W, H), Image.BICUBIC))/255
    fib = 0.62 + 0.22*np.sin(ang*61 + nz*5) + 0.16*np.sin(ang*17 + d*0.05)
    t = np.clip(d/r_iris, 0, 1)
    core = np.stack([255 - 40*t, 190 - 120*t, 90 - 70*t], -1) * fib[..., None]
    m_ir = (d < r_iris)[..., None]
    rgb = np.where(m_ir, core, rgb)
    ring = np.exp(-((d - r_iris)/6)**2)[..., None]   # aro escuro
    rgb = rgb*(1 - 0.85*ring)
    # pupila levemente vertical
    pd = np.sqrt(((xx-cx)/0.62)**2 + (yy-cy)**2)
    pm = np.clip((pd - 58)/4, 0, 1)[..., None]
    rgb = rgb*pm + np.array([6, 4, 3])*(1-pm)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA')
    # sombra das pálpebras
    lid = Image.new('L', (W, H), 0); ImageDraw.Draw(lid).ellipse((cx-W*0.62, cy-r_iris*0.55-H*1.3, cx+W*0.62, cy-r_iris*0.55), fill=245); ImageDraw.Draw(lid).rectangle((0, H*0.80, W, H), fill=120)
    lid = lid.filter(ImageFilter.GaussianBlur(28))
    im = Image.composite(Image.new('RGBA', (W, H), (8, 5, 4, 255)), im, lid)
    # brilho
    hl = Image.new('L', (W, H), 0); ImageDraw.Draw(hl).ellipse((cx+34, cy-40, cx+58, cy-16), fill=210); hl = hl.filter(ImageFilter.GaussianBlur(4))
    im = Image.composite(Image.new('RGBA', (W, H), (255, 236, 205, 255)), im, hl)
    im.putalpha(alm)
    # halo âmbar
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(gm).ellipse((cx-r_iris*1.6, cy-r_iris*1.6, cx+r_iris*1.6, cy+r_iris*1.6), fill=170); gm = gm.filter(ImageFilter.GaussianBlur(90))
    glow.paste((196, 110, 40, 255), (0, 0), gm)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.alpha_composite(glow); out.alpha_composite(im)
    return out
if __name__ == '__main__':
    e = eye(); bg = Image.new('RGBA', e.size, (11, 7, 6, 255)); bg.alpha_composite(e); bg.convert('RGB').resize((700, 280)).save('_eye.png')
