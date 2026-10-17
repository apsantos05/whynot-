"""Story kit promoters: palhaço do balão + 02.11 + espaço p/ sticker de link + rodapé patrocinadores. 1080x1920 (frame do reels)."""
import os, json, random, base64, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); O='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
SP='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
F=O+'/hwb/fonts'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode(); LOGO=O+'/hwb/out/_logo_reto.png'
W,H=1080,1920; DOC='1710_story_promoters-link-ingresso'; D=os.path.join(S,DOC); os.makedirs(D,exist_ok=True); layers=[]
def add(name,im,blend=None,opacity=1,text=None,hidden=False):
    p=os.path.join(D,f'{len(layers):02d}.png'); im.save(p); d={'name':name,'png':p,'blend':blend,'opacity':opacity}
    if text: d['text']=text
    if hidden: d['hidden']=True
    layers.append(d)
add('Fundo',Image.new('RGBA',(W,H),(11,7,6,255)))
fr=Image.open(S+'/fr_11.png').convert('RGB'); fr=fr.resize((W+60,round(fr.height*(W+60)/fr.width)),Image.LANCZOS)
r,g,b=fr.split(); fr=Image.merge('RGB',(r.point(lambda v:min(255,v*1.04)),g,b.point(lambda v:v*0.88)))
ph=Image.new('RGBA',(W,H),(0,0,0,0)); ph.paste(fr,(-30,-40)); add('FOTO · palhaço do balão (frame do reels)',ph)
gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).ellipse((W/2-420,330,W/2+420,900),fill=110); gm=gm.filter(ImageFilter.GaussianBlur(170))
gl=Image.new('RGBA',(W,H),(0,0,0,0)); gl.paste((122,58,22,255),(0,0),gm); add('Brilho brasa (tela)',gl,blend='screen',opacity=.5)
gr=Image.linear_gradient('L').resize((W,H)); y0=880/H*255; gr=gr.point(lambda v:0 if v<y0 else min(250,(v-y0)*2.6))
es=Image.new('RGBA',(W,H),(11,7,6,255)); es.putalpha(gr); add('Escurecer base (leitura do texto)',es)
tp=Image.linear_gradient('L').resize((W,H)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v:max(0,(v-215)*5))
et=Image.new('RGBA',(W,H),(11,7,6,255)); et.putalpha(tp); add('Escurecer topo (logo)',et)
vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-300,-200,W+300,H+200),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(240))
add('Vinheta',Image.composite(Image.new('RGBA',(W,H),(255,255,255,255)),Image.new('RGBA',(W,H),(36,24,18,255)),vg),blend='multiply')
CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center}}"
 ".sh{text-shadow:0 3px 24px rgba(0,0,0,.95)}")
Y=dict(logo=150,nol=262,t=1010,date=1088,info=1330,fan=1384,cta=1470,box=1520,foot=1690)
items={
 'logo':f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-400)//2}px;top:{Y['logo']}px;width:400px;filter:drop-shadow(0 4px 20px rgba(0,0,0,.8))'>",
 'nol':f"<div class='c sh' style=\"top:{Y['nol']}px;font-family:Fr;font-style:italic;font-size:44px;color:#efe4d0;opacity:.9\">no one leaves.</div>",
 't':f"<div class='c sh' style=\"top:{Y['t']}px;font-family:Fr;font-style:italic;font-size:62px;color:#efe4d0\">ele está esperando você.</div>",
 'date':f"<div class='c' style=\"top:{Y['date']}px;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:230px;line-height:1;color:#efe4d0;text-shadow:0 0 50px rgba(196,165,130,.3),0 6px 30px rgba(0,0,0,.9)\">02.11</div>",
 'info':f"<div class='c sh' style=\"top:{Y['info']}px;font-family:SM;font-weight:700;font-size:26px;letter-spacing:.3em;text-indent:.3em;color:#c4a582\">SEGUNDA · 17H · THE WEEK · JK RIO PRETO</div>",
 'fan':f"<div class='c sh' style=\"top:{Y['fan']}px;font-family:Fr;font-style:italic;font-size:40px;color:#efe4d0\">vem fantasiado · concurso de fantasias com prêmios</div>",
 'cta':f"<div class='c sh' style=\"top:{Y['cta']}px;font-family:SM;font-weight:700;font-size:28px;letter-spacing:.34em;text-indent:.34em;color:#efe4d0\">GARANTA SEU INGRESSO ↓</div>",
 'box':f"<div style=\"position:absolute;left:{(W-620)//2}px;top:{Y['box']}px;width:620px;height:130px;box-sizing:border-box;border:3px dashed rgba(196,165,130,.8);border-radius:28px;display:flex;align-items:center;justify-content:center;font-family:SM;font-weight:700;font-size:24px;letter-spacing:.3em;text-indent:.3em;color:rgba(196,165,130,.85)\">COLE O LINK AQUI</div>",
}
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':W,'height':H})
    for k,body in items.items():
        pg.set_content(f"<style>{CSS}</style>{body}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{D}/_{k}.png',omit_background=True)
    br.close()
im=lambda k: Image.open(f'{D}/_{k}.png').convert('RGBA')
T=lambda t,f,s,c,y,ls=0:{'text':t,'font':f,'size':s,'color':c,'x':W/2,'y':y,'ls':ls,'anchor':'middle'}
add('Logo why not? halloween',im('logo'))
add('Slogan · no one leaves.',im('nol'),text=T('no one leaves.','Fraunces-Italic',44,'#efe4d0',Y['nol']+36))
add('Frase · ele está esperando você.',im('t'),text=T('ele está esperando você.','Fraunces-Italic',62,'#efe4d0',Y['t']+50))
add('Data · 02.11',im('date'),text=T('02.11','Fraunces-Black',230,'#efe4d0',Y['date']+180))
add('Info · SEGUNDA · 17H · THE WEEK · JK RIO PRETO',im('info'),text=T('SEGUNDA · 17H · THE WEEK · JK RIO PRETO','SpaceMono-Bold',26,'#c4a582',Y['info']+26,.3))
add('Fantasia · vem fantasiado',im('fan'),text=T('vem fantasiado · concurso de fantasias com prêmios','Fraunces-Italic',40,'#efe4d0',Y['fan']+32))
add('CTA · GARANTA SEU INGRESSO',im('cta'),text=T('GARANTA SEU INGRESSO ↓','SpaceMono-Bold',28,'#efe4d0',Y['cta']+28,.34))
add('GUIA · espaço do sticker de link (ocultar)',im('box'))
ft=Image.open(SP+'/patro/rodape_patrocinadores_1080.png').convert('RGBA'); fl=Image.new('RGBA',(W,H),(0,0,0,0)); fl.alpha_composite(ft,(0,Y['foot']))
add('Patrocinadores (rodapé)',fl)
random.seed(5); n=Image.effect_noise((W,H),22).convert('L')
add('Grão (sobrepor · 18%)',Image.merge('RGBA',(n,n,n,Image.new('L',(W,H),255))),blend='overlay',opacity=.18)
def comp(skip=None):
    base=Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        if skip and d['name'].startswith(skip): continue
        i=Image.open(d['png']).convert('RGBA'); a=i.split()[3].point(lambda v:v*d['opacity']); rgb=i.convert('RGB')
        if d['blend']=='multiply': rgb=ImageChops.multiply(base,rgb)
        elif d['blend']=='screen': rgb=ImageChops.screen(base,rgb)
        elif d['blend']=='overlay': rgb=ImageChops.overlay(base,rgb)
        base=Image.composite(rgb,base,a)
    return base
comp().save(f'{S}/{DOC}_com-guia.png'); comp('GUIA').save(f'{S}/{DOC}.png')
comp().resize((360,640)).save(f'{S}/_prev_a.png')
json.dump({DOC:{'width':W,'height':H,'layers':layers}},open(S+'/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok')
