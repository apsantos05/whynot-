import base64, os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); O='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=O+'/hwb/fonts'; LOGO=O+'/hwb/out/_logo_reto.png'; CAIO=S+'/logo_caio.png'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
css=f"""@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent}}
.i{{position:absolute;left:0;right:0;text-align:center;font-family:'SM';font-weight:700;color:#c4a582;letter-spacing:.42em;text-indent:.42em;text-shadow:0 2px 18px rgba(0,0,0,.9)}}"""
P={'i_logo.png':f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(1080-640)//2}px;top:780px;width:640px;filter:drop-shadow(0 6px 30px rgba(0,0,0,.85))'>"
               "<div class='i' style='top:1000px;font-size:28px'>APRESENTA</div>",
   'c_logo.png':f"<div class='i' style='top:700px;font-size:26px'>LINE-UP · DJ 01/06</div><img src='data:image/png;base64,{b64(CAIO)}' style='position:absolute;left:{(1080-780)//2}px;top:790px;width:780px;filter:drop-shadow(0 0 40px rgba(196,165,130,.35)) drop-shadow(0 6px 30px rgba(0,0,0,.9))'>",
   'l_tag.png':f"<img src='data:image/png;base64,{b64(CAIO)}' style='position:absolute;left:{(1080-300)//2}px;top:1500px;width:300px;opacity:.95;filter:drop-shadow(0 4px 20px rgba(0,0,0,.95))'><div class='i' style='top:1640px;font-size:22px'>DJ 01/06 · 02.11</div>"}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for n,body in P.items():
        pg.set_content(f'<style>{css}</style>{body}'); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(S,n), omit_background=True)
    b.close()
print('ok')
