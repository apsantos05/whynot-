"""Par de logos da XMAS PARTY: why not? (3D preservado, tons de creme/dourado pela luminância) + The House (original), sem fio no meio.
Gera assets/parceiros/xmas_par_logos.png (transparente, alta resolução)."""
import os
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wn = Image.open(R + '/assets/logo/lavanda/logo-why-not-lavanda.png').convert('RGBA'); wn = wn.crop(wn.getbbox())
th = Image.open(R + '/assets/parceiros/logo-the-house.png').convert('RGBA'); th = th.crop(th.getbbox())
# mapeia a luminância do original (face clara, extrusão em degraus mais escuros) para dourado escuro -> creme
L = wn.convert('L'); lo, hi = L.getextrema()
def tom(c0, c1):
    return lambda v: round(c0 + (c1 - c0) * max(0, min(1, (v - lo) / max(1, hi - lo))) ** 1.25)
ouro = Image.merge('RGB', [L.point(tom(a, b)) for a, b in zip((92, 62, 22), (250, 238, 205))])
ouro.putalpha(wn.split()[3]); wn = ouro
H = 300
wn = wn.resize((round(wn.width * H * .6 / wn.height), round(H * .6)), Image.LANCZOS)
th = th.resize((round(th.width * H / th.height), H), Image.LANCZOS)
gap = 110; W = wn.width + gap + th.width
out = Image.new('RGBA', (W, H + 40), (0, 0, 0, 0))
out.alpha_composite(wn, (0, (H + 40 - wn.height) // 2 + 22))
out.alpha_composite(th, (wn.width + gap, 20))
out.save(R + '/assets/parceiros/xmas_par_logos.png'); print(out.size)
