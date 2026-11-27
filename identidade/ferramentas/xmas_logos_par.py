"""Par de logos da XMAS PARTY: why not? (tingido de creme dourado) | fio dourado | The House (original).
Gera assets/parceiros/xmas_par_logos.png (transparente, alta resolução)."""
import os
from PIL import Image, ImageDraw
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wn = Image.open(R + '/assets/logo/lavanda/logo-why-not-lavanda.png').convert('RGBA'); wn = wn.crop(wn.getbbox())
th = Image.open(R + '/assets/parceiros/logo-the-house.png').convert('RGBA'); th = th.crop(th.getbbox())
creme = Image.new('RGBA', wn.size, (243, 226, 182, 255)); creme.putalpha(wn.split()[3]); wn = creme
H = 300
wn = wn.resize((round(wn.width * H * .58 / wn.height), round(H * .58)), Image.LANCZOS)
th = th.resize((round(th.width * H / th.height), H), Image.LANCZOS)
gap = 90; W = wn.width + gap * 2 + 6 + th.width
out = Image.new('RGBA', (W, H + 40), (0, 0, 0, 0))
out.alpha_composite(wn, (0, (H + 40 - wn.height) // 2 + 22))
ImageDraw.Draw(out).rectangle((wn.width + gap, 90, wn.width + gap + 5, H - 40), fill=(214, 178, 106, 230))
out.alpha_composite(th, (wn.width + gap * 2 + 6, 20))
out.save(R + '/assets/parceiros/xmas_par_logos.png'); print(out.size)
