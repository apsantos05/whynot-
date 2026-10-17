import base64, os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); O='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=O+'/hwb/fonts'; LOGO=O+'/hwb/out/_logo_reto.png'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
css=f"""@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}
@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent}}
.t{{position:absolute;left:0;right:0;text-align:center;font-family:'Fr';font-style:italic;color:#efe4d0;text-shadow:0 0 26px rgba(196,165,130,.3),0 4px 30px rgba(0,0,0,.95)}}
.i{{position:absolute;left:0;right:0;text-align:center;font-family:'SM';font-weight:700;color:#c4a582;letter-spacing:.38em;text-indent:.38em;text-shadow:0 2px 18px rgba(0,0,0,.9)}}"""
P={'s1.png':'<div class="t" style="top:1500px;font-size:96px">ingressos na bio.</div>',
   's2.png':'<div class="t" style="top:1500px;font-size:88px">espero vocês no dia 2.</div>',
   'e_logo.png':f'<img src="data:image/png;base64,{b64(LOGO)}" style="position:absolute;left:215px;width:650px;top:560px">',
   'e_date.png':"<div class='t' style=\"top:860px;font-family:FrV;font-style:normal;font-weight:900;font-variation-settings:'opsz' 144;font-size:200px;line-height:1\">02.11</div>",
   'e_title.png':'<div class="t" style="top:1110px;font-size:110px">no one leaves.</div>',
   'e_cta.png':'<div style="position:absolute;left:50%;transform:translateX(-50%);top:1320px;border:2px solid rgba(196,165,130,.75);border-radius:999px;padding:20px 44px;font-family:SM;font-weight:700;font-size:34px;letter-spacing:.32em;color:#efe4d0;white-space:nowrap">INGRESSOS NA BIO</div>'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for n,body in P.items():
        pg.set_content(f'<style>{css}</style>{body}'); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(S,n), omit_background=True)
    b.close()
print('ok')
