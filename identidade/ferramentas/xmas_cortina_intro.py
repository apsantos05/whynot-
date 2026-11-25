"""Texto de abertura do vídeo da cortina: "why not? apresenta" (PNG transparente 1080x1920).
Uso: python3 xmas_cortina_intro.py <pasta fontes> <saida.png>"""
import sys, base64
from playwright.sync_api import sync_playwright
FD, OUT = sys.argv[1], sys.argv[2]
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
PF = FD + '/fontsource-playfair-display-5.3.0/package/files/'; CZ = FD + '/fontsource-cinzel-5.3.0/package/files/'
html = f"""<style>@font-face{{font-family:P;font-style:italic;src:url(data:font/woff2;base64,{b64(PF+'playfair-display-latin-400-italic.woff2')})}}
@font-face{{font-family:C;src:url(data:font/woff2;base64,{b64(CZ+'cinzel-latin-400-normal.woff2')})}}
*{{margin:0}} body{{width:1080px;height:1920px;background:transparent;position:relative}}
.w{{position:absolute;left:0;right:0;top:760px;text-align:center;font-family:P;font-style:italic;font-size:150px;line-height:1;
 background:linear-gradient(180deg,#fff1c8 0%,#e8c46e 45%,#b8862b 70%,#f3d98f 100%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(0 0 18px rgba(255,190,90,.45)) drop-shadow(0 4px 24px rgba(0,0,0,.8))}}
.a{{position:absolute;left:0;right:0;top:965px;text-align:center;font-family:C;font-size:50px;letter-spacing:.40em;padding-left:.40em;color:#f6e3b4;-webkit-font-smoothing:antialiased;
 text-shadow:0 2px 3px rgba(0,0,0,.95),0 0 2px rgba(0,0,0,.8)}}</style>
<div class=w>why not?</div><div class=a>apresenta</div>"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.set_content(html); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT, omit_background=True); br.close()
