import base64, os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); SC='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=SC+'/hwb/fonts'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode(); LOGO=SC+'/hwb/out/_logo_reto.png'
A='#c4a582'; O='#efe4d0'; BR='#7a3a16'
def lbl(x,y,t,s=15,c=O,ls=.22,anchor='middle',rot=0):
    tr=f" transform='rotate({rot} {x} {y})'" if rot else ''
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' dominant-baseline='middle' font-family='SM' font-weight='700' font-size='{s}' letter-spacing='{ls}em' fill='{c}'{tr}>{t}</text>"
def num(x,y,t,s=30): return f"<text x='{x}' y='{y}' text-anchor='middle' dominant-baseline='central' font-family='FrV' font-weight='900' font-size='{s}' fill='{O}'>{t}</text>"
def bistro(x,y): return f"<circle cx='{x}' cy='{y}' r='17' fill='#2e160a' stroke='{A}' stroke-width='3'/><circle cx='{x}' cy='{y}' r='5' fill='{A}'/>"
svg=[]
svg.append(f"<defs><pattern id='h' width='14' height='14' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='14' stroke='rgba(196,165,130,.16)' stroke-width='4'/></pattern>"
           f"<radialGradient id='glow' cx='50%' cy='50%' r='50%'><stop offset='0' stop-color='{BR}' stop-opacity='.55'/><stop offset='1' stop-color='{BR}' stop-opacity='0'/></radialGradient></defs>")
# avenida
svg.append(f"<rect x='30' y='170' width='750' height='133' fill='#1c1714'/>")
svg.append(f"<line x1='30' y1='236' x2='780' y2='236' stroke='rgba(239,228,208,.35)' stroke-width='4' stroke-dasharray='34 26'/>")
svg.append(lbl(405,205,'AVENIDA JK',17,'rgba(239,228,208,.7)',.4))
# calçada + entrada pela avenida
svg.append(f"<rect x='30' y='303' width='750' height='127' fill='#120c09'/>")
svg.append(f"<rect x='381' y='303' width='84' height='127' fill='rgba(196,165,130,.18)' stroke='{A}' stroke-width='3'/>")
svg.append(lbl(423,366,'ENTRADA',13,O,.25,rot=-90))
# área externa 1
svg.append(f"<rect x='30' y='430' width='750' height='182' fill='#17100b' stroke='{A}' stroke-width='3'/>")
svg.append(lbl(405,521,'ÁREA EXTERNA',17,'rgba(196,165,130,.9)',.35))
# pista (meio)
svg.append(f"<rect x='207' y='612' width='306' height='393' fill='#1f120a'/>")
svg.append(f"<ellipse cx='360' cy='808' rx='200' ry='220' fill='url(#glow)'/>")
for x,y in [(290,690),(430,690),(360,800),(290,910),(430,910)]: svg.append(bistro(x,y))
svg.append(lbl(360,752,'PISTA',22,O,.45))
svg.append(lbl(360,968,'BISTRÔS',12,A,.3))
# lounges 1-5
h=(1003-617)/5
for i in range(5):
    y=617+i*h; svg.append(f"<rect x='57' y='{y}' width='150' height='{h}' fill='rgba(196,165,130,.13)' stroke='{A}' stroke-width='3'/>")
    svg.append(num(132,y+h/2-6,str(i+1),34)); svg.append(lbl(132,y+h/2+22,'LOUNGE',10,A,.25))
# cozinha e banheiros
svg.append(f"<rect x='513' y='612' width='267' height='368' fill='url(#h)' stroke='rgba(196,165,130,.55)' stroke-width='3'/>")
svg.append(lbl(646,796,'COZINHA',15,'rgba(239,228,208,.75)',.3))
svg.append(f"<rect x='518' y='993' width='262' height='92' fill='#1a120d' stroke='{A}' stroke-width='3'/>")
svg.append(lbl(649,1039,'BANHEIROS',15,O,.3))
# área externa 2
svg.append(f"<path d='M30 1005 L513 1005 L513 1092 L780 1092 L780 1715 L30 1715 Z' fill='#17100b' stroke='{A}' stroke-width='3'/>")
svg.append(lbl(405,1250,'ÁREA EXTERNA',17,'rgba(196,165,130,.9)',.35))
# lounge 6
svg.append(f"<circle cx='110' cy='1075' r='54' fill='rgba(196,165,130,.13)' stroke='{A}' stroke-width='3'/>"); svg.append(num(110,1069,'6',34)); svg.append(lbl(110,1100,'LOUNGE',9,A,.2))
# palco
svg.append(f"<ellipse cx='373' cy='1468' rx='300' ry='220' fill='url(#glow)'/>")
svg.append(f"<rect x='220' y='1352' width='307' height='233' rx='10' fill='rgba(196,165,130,.2)' stroke='{O}' stroke-width='5'/>")
svg.append(f"<text x='373' y='1462' text-anchor='middle' dominant-baseline='central' font-family='Fr' font-style='italic' font-size='58' fill='{O}'>palco</text>")
svg.append(lbl(373,1520,'6 DJS',13,A,.35))
# entrada (lado oposto)
svg.append(f"<line x1='30' y1='1715' x2='780' y2='1715' stroke='{O}' stroke-width='6'/>")
svg.append(f"<rect x='75' y='1732' width='150' height='40' rx='20' fill='{O}'/>"); svg.append(lbl(150,1753,'ENTRADA',13,'#0b0706',.25))
SVG="<svg xmlns='http://www.w3.org/2000/svg' viewBox='20 160 770 1630' width='{w}' height='{h}'>"+''.join(svg)+"</svg>"
CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 "html,body{margin:0;background:#0b0706}.c{position:absolute;left:0;right:0;text-align:center}")
def page(W,H,map_w,map_y,logo_y,logo_w,title_y,title_s,info_y,info_s):
    mh=round(map_w*1630/770)
    return (f"<div style='position:relative;width:{W}px;height:{H}px;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#1d0f08 0%,#0b0706 70%)'>"
      f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-logo_w)//2}px;top:{logo_y}px;width:{logo_w}px'>"
      f"<div class=c style=\"top:{title_y}px;font-family:Fr;font-style:italic;font-size:{title_s}px;color:{O}\">o mapa da noite.</div>"
      f"<div style='position:absolute;left:{(W-map_w)//2}px;top:{map_y}px'>{SVG.format(w=map_w,h=mh)}</div>"
      f"<div class=c style=\"top:{info_y}px;font-family:SM;font-weight:700;font-size:{info_s}px;letter-spacing:.32em;text-indent:.32em;color:{A}\">02.11 · 17H · THE WEEK · JK RIO PRETO</div></div>")
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,W,H,args in [('2110_story_mapa-the-week',1080,1920,(640,350,130,300,215,62,1745,22)),('2110_feed_mapa-the-week',1080,1350,(480,250,60,240,140,48,1290,18))]:
        pg=b.new_page(viewport={'width':W,'height':H},device_scale_factor=2)
        pg.set_content(f"<style>{CSS}</style>"+page(W,H,*args)); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{S}/{name}.png')
    b.close()
print('ok')
