import base64, os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); F=S+'/../hwb/fonts'; LOGO=S+'/../hwb/out/_logo_reto.png'
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
css=f"""@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent}}
.t{{position:absolute;left:0;right:0;text-align:center;font-family:'Fr';font-style:italic;color:#efe4d0;text-shadow:0 0 26px rgba(196,165,130,.3),0 4px 30px rgba(0,0,0,.9)}}
.i{{position:absolute;left:0;right:0;text-align:center;font-family:'SM';font-weight:700;color:#c4a582;letter-spacing:.38em;text-indent:.38em;text-shadow:0 2px 18px rgba(0,0,0,.9)}}"""
P={'t1.png':'<div class="t" style="top:1440px;font-size:112px">ele já chegou.</div>',
   't2.png':'<div class="t" style="top:1440px;font-size:92px">e está esperando<br>por você.</div>',
   't3.png':'<div class="i" style="top:1500px;font-size:44px">SEXTA-FEIRA · 21:00</div><div class="t" style="top:1570px;font-size:76px">tudo será revelado.</div>',
   'e_logo.png':f'<img src="data:image/png;base64,{b64(LOGO)}" style="position:absolute;left:190px;width:700px;top:660px">',
   'e_title.png':'<div class="t" style="top:1020px;font-size:128px">no one leaves.</div>',
   'e_date.png':'<div class="i" style="top:1230px;font-size:40px">SEXTA-FEIRA · 21:00</div>'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for n,body in P.items():
        pg.set_content(f'<style>{css}</style>{body}'); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(S,n), omit_background=True)
    b.close()
print('ok')
