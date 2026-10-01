"""Gera as versões tratadas (duotone why not?) das fotos HQ: hq/<dj>.png -> lineup/z_<dj>.png
Recorta no contorno, converte para tons gelo, suaviza a base e as bordas cortadas pela foto."""
import numpy as np, sys, os
from PIL import Image, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(D), "lineup")
LO = np.array([6, 10, 12], np.float32); HI = np.array([232, 244, 248], np.float32)
MAXH = 1400

def grade(name, contrast=1.2, gamma=0.92, bottom=0.18, lift=0.03, keep=1.0):
    im = Image.open(os.path.join(D, name + ".png")).convert("RGBA")
    a = np.array(im)[..., 3]
    ys, xs = np.where(a > 16)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    y1 = y0 + int((y1 - y0) * keep)
    im = im.crop((x0, y0, x1, y1))
    if im.height > MAXH: im = im.resize((int(im.width * MAXH / im.height), MAXH), Image.LANCZOS)
    arr = np.array(im).astype(np.float32); al = arr[..., 3] / 255
    rgb = arr[..., :3] / 255
    g = 0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
    sub = g[al > 0.5]; lo, hi = np.percentile(sub, 0.8), np.percentile(sub, 99.6)
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    g = np.clip((g - 0.5) * contrast + 0.5 + lift, 0, 1) ** gamma
    out = LO + g[..., None] * (HI - LO)
    h, w = al.shape
    # base esfumada
    yv = np.linspace(0, 1, h)[:, None]
    fade = np.clip((1 - yv) / bottom, 0, 1) ** 1.3
    # bordas laterais cortadas pela foto original: esfuma
    edge = np.ones((h, w), np.float32)
    touch_l = (np.array(Image.open(os.path.join(D, name + ".png")).convert("RGBA"))[..., 3][:, 0] > 16).mean() > 0.05
    touch_r = (np.array(Image.open(os.path.join(D, name + ".png")).convert("RGBA"))[..., 3][:, -1] > 16).mean() > 0.05
    xv = np.linspace(0, 1, w)[None, :]
    if touch_l: edge *= np.clip(xv / 0.10, 0, 1)
    if touch_r: edge *= np.clip((1 - xv) / 0.10, 0, 1)
    A = np.clip(al * fade * edge, 0, 1)
    res = np.dstack([out, A[..., None] * 255]).astype(np.uint8)
    o = Image.fromarray(res, "RGBA").filter(ImageFilter.UnsharpMask(1.2, 50, 3))
    o.save(os.path.join(OUT, "z_" + name + ".png"))
    print(name, o.size, "aspect", round(o.width / o.height, 4), "L/R cut", touch_l, touch_r)
    return o.width / o.height

if __name__ == "__main__":
    import json
    asp = {}
    KEEP = {"coiote": 0.74, "maka": 1.0, "maycon": 0.72, "mex": 0.68, "possani": 0.74}
    for n, k in KEEP.items():
        asp[n] = round(grade(n, keep=k), 4)
    json.dump(asp, open(os.path.join(OUT, "asp_hq.json"), "w"))
