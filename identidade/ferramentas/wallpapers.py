import base64, os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__))
O='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=O+'/hwb/fonts/fs/package/files/'; SM=O+'/hwb/fonts/sm/package/files/'
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
W,H=1290,2796
fonts=f"""@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'fraunces-latin-full-normal.woff2')}) format('woff2')}}
@font-face{{font-family:'FrI';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(SM+'space-mono-latin-700-normal.woff2')}) format('woff2')}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}"""
ramp=['#b3cfd6','#9bbdc6','#85abb5','#7199a4','#5f8792','#4f7580','#41646e','#35535c','#2a434b','#20343a','#17262b','#0f191d']
step=4.2
shadow=','.join(f'{-(k+1)*step:.1f}px {(k+1)*step:.1f}px 0 {c}' for k,c in enumerate(ramp))
grain=f"""<svg width="{W}" height="{H}" style="position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""
trad=f"""<body style="background:#060a0c">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 38% at 50% 56%,#12302e 0%,#0a1315 55%,#060a0c 100%)"></div>
<div style="position:absolute;left:0;right:0;top:1290px;text-align:center;transform:rotate(-8deg)">
 <span style="font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144,'SOFT' 0,'WONK' 0;font-size:250px;letter-spacing:-.02em;color:#e4f2f6;text-shadow:{shadow}">why not?</span></div>
<div style="position:absolute;left:0;right:0;top:1760px;text-align:center;font-family:FrI;font-style:italic;font-size:64px;color:#9dbcc4">uma vez por mês. nunca igual.</div>
<div style="position:absolute;left:0;right:0;top:2330px;text-align:center;font-family:SM;font-weight:700;font-size:30px;letter-spacing:.5em;text-indent:.5em;color:#2f4e56">@WHYNOT.SJRP</div>
{grain}</body>"""
hall=f"""<body style="background:#0b0706">
<img src="data:image/jpeg;base64,{b64(S+'/vela.jpg')}" style="position:absolute;left:{(W-1120)//2}px;top:330px;width:1120px;
 -webkit-mask-image:radial-gradient(ellipse 42% 46% at 50% 47%,#000 55%,transparent 100%)">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 32% 15% at 50% 30%,rgba(122,58,22,.38),transparent 70%);mix-blend-mode:screen"></div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 85% 70% at 50% 50%,transparent 55%,rgba(5,3,2,.85) 100%)"></div>
<img src="data:image/png;base64,{b64(O+'/hwb/out/_logo_reto.png')}" style="position:absolute;left:{(W-760)//2}px;top:1930px;width:760px">
<div style="position:absolute;left:0;right:0;top:2170px;text-align:center;font-family:FrI;font-style:italic;font-size:84px;color:#efe4d0;text-shadow:0 0 30px rgba(196,165,130,.3)">no one leaves.</div>
<div style="position:absolute;left:0;right:0;top:2310px;text-align:center;font-family:SM;font-weight:700;font-size:30px;letter-spacing:.5em;text-indent:.5em;color:#c4a582">31 · 10</div>
{grain}</body>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    for name,html in [('wallpaper-whynot-tradicional.png',trad),('wallpaper-whynot-halloween.png',hall)]:
        pg.set_content(f'<style>{fonts}</style>{html}'); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(S,name)); print('ok',name)
    b.close()
