"""Capas dos destaques do Instagram (1080x1920, ícone de linha no centro — o corte circular pega o miolo).
Uso: python3 perfil_destaques.py"""
import os
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = R + '/perfil/destaques'; os.makedirs(OUT, exist_ok=True)
BASE, DEST = '#09080c', '#ece6f4'
ICONS = {
 'quintas':  "<rect x='3.5' y='5' width='17' height='15' rx='2'/><path d='M3.5 10h17M8 3v4M16 3v4'/>",
 'ingressos': "<path d='M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4z'/><path d='M14.5 6.5v11' stroke-dasharray='1.6 2'/>",
 'lista-vip': "<path d='M12 3.6l2.6 5.3 5.8.85-4.2 4.1 1 5.8L12 16.9l-5.2 2.75 1-5.8-4.2-4.1 5.8-.85z'/>",
 'fotos':    "<path d='M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z'/><circle cx='12' cy='13.5' r='3.4'/>",
 'line-up':  "<path d='M4 14v-2a8 8 0 0 1 16 0v2'/><path d='M4 14h2.6v5.2H5a1 1 0 0 1-1-1zM20 14h-2.6v5.2H19a1 1 0 0 0 1-1z'/>",
 'onde':     "<path d='M12 21s-6.5-6.1-6.5-11a6.5 6.5 0 0 1 13 0c0 4.9-6.5 11-6.5 11z'/><circle cx='12' cy='10' r='2.3'/>",
 'afterzin': "<path d='M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z'/>",
}
def html(svg):
    return (f"<style>*{{margin:0}}body{{width:1080px;height:1920px;background:{BASE};position:relative;overflow:hidden}}"
            f".g{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#2a2238 0,#15111d 330px,{BASE} 760px)}}"
            f"svg{{position:absolute;left:50%;top:50%;width:520px;height:520px;transform:translate(-50%,-50%)}}</style>"
            f"<div class='g'></div><svg viewBox='0 0 24 24' fill='none' stroke='{DEST}' stroke-width='1.05' stroke-linecap='round' stroke-linejoin='round'>{svg}</svg>")
with sync_playwright() as p:
    br = p.chromium.launch()
    for n, svg in ICONS.items():
        pg = br.new_page(viewport={'width': 1080, 'height': 1920}); pg.set_content(html(svg))
        pg.screenshot(path=f'{OUT}/destaque_{n}.png'); pg.close(); print(n)
    br.close()
# prévia: como ficam no perfil (círculos)
names = list(ICONS); S = 220; W = 60 + len(names) * (S + 40); sheet = Image.new('RGB', (W, S + 120), '#000000')
for i, n in enumerate(names):
    im = Image.open(f'{OUT}/destaque_{n}.png').convert('RGB'); c = im.crop((0, 420, 1080, 1500)).resize((S, S), Image.LANCZOS)
    m = Image.new('L', (S * 4, S * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255); m = m.resize((S, S), Image.LANCZOS)
    x = 50 + i * (S + 40); sheet.paste(c, (x, 40), m); ImageDraw.Draw(sheet).ellipse((x - 4, 36, x + S + 4, 44 + S), outline='#3a3348', width=2)
sheet.save(OUT + '/_previa-no-perfil.png')
