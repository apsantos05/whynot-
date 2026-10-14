"""Renderiza os textos/logo do reels como PNG transparente 1080x1920 (Playwright)."""
import base64, sys, os
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(S, '..', 'hwb', 'fonts')
LOGO = os.path.join(S, '..', 'hwb', 'out', '_logo_reto.png')
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

css = f"""
@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}}
.t{{position:absolute;left:0;right:0;text-align:center;font-family:'Fr';font-style:italic;font-weight:400;color:#efe4d0;
    text-shadow:0 0 28px rgba(196,165,130,.35),0 4px 30px rgba(0,0,0,.85)}}
.i{{position:absolute;left:0;right:0;text-align:center;font-family:'SM';font-weight:700;color:#c4a582;letter-spacing:.42em;text-indent:.42em}}
"""
pages = {
    'tx_quem.png': '<div class="t" style="top:1380px;font-size:132px">quem entra…</div>',
    'tx_fica.png': '<div class="t" style="top:1380px;font-size:150px">…fica.</div>',
    'end_logo.png': f'<img src="data:image/png;base64,{b64(LOGO)}" style="position:absolute;left:190px;width:700px;top:640px">',
    'end_title.png': '<div class="t" style="top:1010px;font-size:132px">no one leaves.</div>',
    'end_soon.png': '<div class="i" style="top:1220px;font-size:32px">COMING SOON</div>',
}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for name, body in pages.items():
        pg.set_content(f'<html><head><style>{css}</style></head><body>{body}</body></html>')
        pg.evaluate('document.fonts.ready.then(()=>0)')
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(S, name), omit_background=True)
        print('ok', name)
    b.close()
