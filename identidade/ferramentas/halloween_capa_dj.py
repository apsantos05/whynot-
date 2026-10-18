"""Capa do reels DJ 01/06 · Caio Tofole — foto + logo why not? + logo do DJ. 1080x1920 (texto dentro do recorte 3:4 do grid)."""
import os, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); O='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=O+'/hwb/fonts'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode(); LOGO=O+'/hwb/out/_logo_reto.png'; CAIO=S+'/logo_caio.png'
W,H=1080,1920; DOC='1810_capa-reels-dj01-caio-tofole'; D=os.path.join(S,DOC); os.makedirs(D,exist_ok=True); layers=[]
def add(name,im,blend=None,opacity=1,text=None):
    p=os.path.join(D,f'{len(layers):02d}.png'); im.save(p); d={'name':name,'png':p,'blend':blend,'opacity':opacity}
    if text: d['text']=text
    layers.append(d)
add('Fundo',Image.new('RGBA',(W,H),(11,7,6,255)))
ph=Image.open(S+'/foto_caio.png').convert('RGB'); k=1990/ph.height; ph=ph.resize((round(ph.width*k),1990),Image.LANCZOS)
# grade: fundo bege vira brasa escura, preto continua preto
r,g,b=ph.split()
r=r.point(lambda v:int(255*((v/255)**1.7)*0.72)); g=g.point(lambda v:int(255*((v/255)**1.85)*0.5)); b=b.point(lambda v:int(255*((v/255)**2.0)*0.36))
ph=Image.merge('RGB',(r,g,b))
x0=round(800*k)-W//2-30; base=Image.new('RGBA',(W,H),(0,0,0,0)); base.paste(ph,(-x0,250)); fm=Image.new('L',(W,H),0); ImageDraw.Draw(fm).rectangle((0,0,W,H),fill=255)
for yy in range(0,620): fm.paste(int(255*max(0,min(1,(yy-250)/370))**1.4),(0,yy,W,yy+1))
base.putalpha(ImageChops.multiply(base.split()[3],fm)); add('FOTO · Caio Tofole (tratada)',base)
gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).ellipse((W/2-500,420,W/2+480,1150),fill=120); gm=gm.filter(ImageFilter.GaussianBlur(200))
gl=Image.new('RGBA',(W,H),(0,0,0,0)); gl.paste((196,120,60,255),(0,0),gm); add('Luz âmbar (tela)',gl,blend='screen',opacity=.35)
gr=Image.linear_gradient('L').resize((W,H)); y0=1000/H*255; gr=gr.point(lambda v:0 if v<y0 else min(235,(v-y0)*2.4))
es=Image.new('RGBA',(W,H),(11,7,6,255)); es.putalpha(gr); add('Escurecer base (leitura)',es)
tp=Image.linear_gradient('L').resize((W,H)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v:max(0,(v-195)*4))
et=Image.new('RGBA',(W,H),(11,7,6,255)); et.putalpha(tp); add('Escurecer topo (logo)',et)
vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-260,-120,W+260,H+120),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(240))
add('Vinheta',Image.composite(Image.new('RGBA',(W,H),(255,255,255,255)),Image.new('RGBA',(W,H),(30,20,14,255)),vg),blend='multiply')
CSS=(f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center;text-shadow:0 3px 22px rgba(0,0,0,.95)}}")
Y=dict(logo=262,ap=378,lu=1190,caio=1240,info=1572)
items={'logo':f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-360)//2}px;top:{Y['logo']}px;width:360px;filter:drop-shadow(0 4px 20px rgba(0,0,0,.8))'>",
 'ap':f"<div class=c style=\"top:{Y['ap']}px;font-family:SM;font-weight:700;font-size:22px;letter-spacing:.42em;text-indent:.42em;color:#c4a582\">APRESENTA</div>",
 'lu':f"<div class=c style=\"top:{Y['lu']}px;font-family:SM;font-weight:700;font-size:26px;letter-spacing:.42em;text-indent:.42em;color:#c4a582\">LINE-UP · DJ 01/06</div>",
 'caio':f"<img src='data:image/png;base64,{b64(CAIO)}' style='position:absolute;left:{(W-800)//2}px;top:{Y['caio']}px;width:800px;filter:drop-shadow(0 0 36px rgba(196,165,130,.3)) drop-shadow(0 6px 26px rgba(0,0,0,.9))'>",
 'info':f"<div class=c style=\"top:{Y['info']}px;font-family:Fr;font-style:italic;font-size:46px;color:#efe4d0\">02.11 · The Week</div>"}
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':W,'height':H})
    for kk,body in items.items():
        pg.set_content(f"<style>{CSS}</style>{body}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{D}/_{kk}.png',omit_background=True)
    br.close()
im=lambda kk: Image.open(f'{D}/_{kk}.png').convert('RGBA')
T=lambda t,f,s,c,y,ls=0:{'text':t,'font':f,'size':s,'color':c,'x':W/2,'y':y,'ls':ls,'anchor':'middle'}
add('Logo why not? halloween',im('logo'))
add('APRESENTA',im('ap'),text=T('APRESENTA','SpaceMono-Bold',22,'#c4a582',Y['ap']+22,.42))
add('LINE-UP · DJ 01/06',im('lu'),text=T('LINE-UP · DJ 01/06','SpaceMono-Bold',26,'#c4a582',Y['lu']+26,.42))
add('Logo Caio Tofole',im('caio'))
add('Info · 02.11 · The Week',im('info'),text=T('02.11 · The Week','Fraunces-Italic',46,'#efe4d0',Y['info']+38))
random.seed(8); n=Image.effect_noise((W,H),22).convert('L')
add('Grão (sobrepor · 18%)',Image.merge('RGBA',(n,n,n,Image.new('L',(W,H),255))),blend='overlay',opacity=.18)
c=Image.open(layers[0]['png']).convert('RGB')
for d in layers[1:]:
    i=Image.open(d['png']).convert('RGBA'); a=i.split()[3].point(lambda v:v*d['opacity']); rgb=i.convert('RGB')
    if d['blend']=='multiply': rgb=ImageChops.multiply(c,rgb)
    elif d['blend']=='screen': rgb=ImageChops.screen(c,rgb)
    elif d['blend']=='overlay': rgb=ImageChops.overlay(c,rgb)
    c=Image.composite(rgb,c,a)
c.save(D+'/_composite.png'); c.save(f'{S}/{DOC}.png')
pv=Image.new('RGB',(360+20+360,640),(40,40,40)); pv.paste(c.resize((360,640)),(0,0)); pv.paste(c.crop((0,240,W,1680)).resize((360,480)),(380,80)); pv.save(S+'/_capa_prev3.png')
json.dump({DOC:{'width':W,'height':H,'layers':layers}},open(S+'/manifest_capa.json','w'),indent=1,ensure_ascii=False)
print('ok')
