"""Carrossel 'como participar do concurso' — 4 slides feed 4:5 (2160x2700), camadas + manifest p/ PSD."""
import os, json, random, base64, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); SC='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
FOOT='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/patro/rodape_patrocinadores_2160.png'
F=SC+'/hwb/fonts'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode(); LOGO=SC+'/hwb/out/_logo_reto.png'
W,H=2160,2700
CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center}}.sh{{text-shadow:0 4px 30px rgba(0,0,0,.9)}}")
fr=lambda y,s,t,c='#efe4d0',extra='': (f"<div class='c sh' style=\"top:{y}px;font-family:Fr;font-style:italic;font-size:{s}px;line-height:1.05;color:{c};{extra}\">{t}</div>",
     {'text':t,'font':'Fraunces-Italic','size':s,'color':c,'x':W/2,'y':y+s*.8,'ls':0,'anchor':'middle'})
sm=lambda y,s,t,c='#c4a582',ls=.4: (f"<div class='c sh' style=\"top:{y}px;font-family:SM;font-weight:700;font-size:{s}px;letter-spacing:{ls}em;text-indent:{ls}em;color:{c}\">{t}</div>",
     {'text':t,'font':'SpaceMono-Bold','size':s,'color':c,'x':W/2,'y':y+s,'ls':ls,'anchor':'middle'})
logo=lambda y,w: (f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-w)//2}px;top:{y}px;width:{w}px;filter:drop-shadow(0 6px 30px rgba(0,0,0,.85))'>",None)
def bg_photo(path,y_off=0,dark_from=1300):
    ph=Image.open(path).convert('RGB'); k=max(W/ph.width,H/ph.height)*1.02; ph=ph.resize((round(ph.width*k),round(ph.height*k)),Image.LANCZOS)
    r,g,b=ph.split(); ph=Image.merge('RGB',(r.point(lambda v:min(255,v*1.03)),g.point(lambda v:v*.95),b.point(lambda v:v*.8)))
    L=Image.new('RGBA',(W,H),(0,0,0,0)); L.paste(ph,(-(ph.width-W)//2,y_off)); out=[('FOTO',L,None,1)]
    gr=Image.linear_gradient('L').resize((W,H)); y0=dark_from/H*255; gr=gr.point(lambda v:0 if v<y0 else min(245,(v-y0)*3))
    es=Image.new('RGBA',(W,H),(11,7,6,255)); es.putalpha(gr); out.append(('Escurecer base',es,None,1))
    tp=Image.linear_gradient('L').resize((W,H)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v:max(0,(v-200)*4))
    et=Image.new('RGBA',(W,H),(11,7,6,255)); et.putalpha(tp); out.append(('Escurecer topo',et,None,1)); return out
def bg_glow(cy=1100):
    gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).ellipse((W/2-900,cy-700,W/2+900,cy+700),fill=150); gm=gm.filter(ImageFilter.GaussianBlur(320))
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); gl.paste((122,58,22,255),(0,0),gm); return [('Brilho brasa (tela)',gl,'screen',.7)]
def build(doc,bgl,items,foot=None,seed=1):
    D=os.path.join(S,doc); os.makedirs(D,exist_ok=True); layers=[]
    def add(name,im,blend=None,opacity=1,text=None):
        p=os.path.join(D,f'{len(layers):02d}.png'); im.save(p); d={'name':name,'png':p,'blend':blend,'opacity':opacity}
        if text: d['text']=text
        layers.append(d)
    add('Fundo',Image.new('RGBA',(W,H),(11,7,6,255)))
    for n,im,bl,op in bgl: add(n,im,bl,op)
    vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-500,-300,W+500,H+300),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(380))
    add('Vinheta',Image.composite(Image.new('RGBA',(W,H),(255,255,255,255)),Image.new('RGBA',(W,H),(36,24,18,255)),vg),blend='multiply')
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={'width':W,'height':H})
        for k,(name,(html,txt)) in enumerate(items):
            pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{D}/_t{k}.png',omit_background=True); add(name,Image.open(f'{D}/_t{k}.png').convert('RGBA'),text=txt)
        br.close()
    if foot is not None:
        ft=Image.open(FOOT).convert('RGBA'); fl=Image.new('RGBA',(W,H),(0,0,0,0)); fl.alpha_composite(ft,(0,foot)); add('Patrocinadores (rodapé)',fl)
    random.seed(seed); n=Image.effect_noise((W,H),22).convert('L')
    add('Grão (sobrepor · 18%)',Image.merge('RGBA',(n,n,n,Image.new('L',(W,H),255))),blend='overlay',opacity=.18)
    c=Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        i=Image.open(d['png']).convert('RGBA'); a=i.split()[3].point(lambda v:v*d['opacity']); rgb=i.convert('RGB')
        if d['blend']=='multiply': rgb=ImageChops.multiply(c,rgb)
        elif d['blend']=='screen': rgb=ImageChops.screen(c,rgb)
        elif d['blend']=='overlay': rgb=ImageChops.overlay(c,rgb)
        c=Image.composite(rgb,c,a)
    c.save(D+'/_composite.png'); c.resize((1080,1350),Image.LANCZOS).save(f'{S}/{doc}.png')
    return {doc:{'width':W,'height':H,'layers':layers}}
P='2010_carrossel-concurso'
man={}
# 1 capa
man.update(build(P+'-01-capa',bg_photo(SC+'/hwf/photo-1787419187501-71fa264bafa4.png',-200,1250),[
  ('Logo',logo(150,560)),('no one leaves.',fr(325,64,'no one leaves.',extra='opacity:.9')),
  ('CONCURSO · MELHOR FANTASIA',sm(1700,44,'CONCURSO · MELHOR FANTASIA')),('Título · como participar.',fr(1790,250,'como participar.')),
  ('Info · 02.11 · THE WEEK',sm(2140,38,'02.11 · 17H · THE WEEK','#efe4d0',.34)),('ARRASTA →',sm(2420,36,'ARRASTA  →','#c4a582',.5))],seed=11))
# 2 passos
steps=[('01','vem fantasiado.','capricha no look: terror, clássico ou criativo.'),('02','chega cedo.','a porta abre às 17h. quanto antes, mais gente vê sua fantasia.'),
       ('03','posta e marca a gente.','fantasia nos stories marcando @whynot.sjrp.'),('04','fica até o fim.','os vencedores são anunciados durante a festa.')]
it=[('Logo',logo(150,400)),('COMO PARTICIPAR',sm(330,40,'COMO PARTICIPAR')),('Título · 4 passos.',fr(420,170,'4 passos.'))]
y=780
for n,t,d in steps:
    it.append((f'Passo {n} · número',(f"<div style=\"position:absolute;left:300px;top:{y}px;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:150px;line-height:1;color:#c4a582\">{n}</div>",{'text':n,'font':'Fraunces-Black','size':150,'color':'#c4a582','x':300,'y':y+120,'ls':0,'anchor':'start'})))
    it.append((f'Passo {n} · {t}',(f"<div style=\"position:absolute;left:600px;top:{y+6}px;font-family:Fr;font-style:italic;font-size:96px;line-height:1;color:#efe4d0\">{t}</div>",{'text':t,'font':'Fraunces-Italic','size':96,'color':'#efe4d0','x':600,'y':y+84,'ls':0,'anchor':'start'})))
    it.append((f'Passo {n} · descrição',(f"<div style=\"position:absolute;left:604px;top:{y+128}px;width:1300px;font-family:SM;font-weight:700;font-size:42px;line-height:1.4;letter-spacing:.03em;color:rgba(239,228,208,.78)\">{d}</div>",{'text':d,'font':'SpaceMono-Bold','size':42,'color':'#efe4d0','x':604,'y':y+162,'ls':.04,'anchor':'start'})))
    y+=420
man.update(build(P+'-02-passos',bg_glow(1500),it,seed=12))
# 3 prêmios
PR=[('kit completo',"LA'BRIZZA"),('perfume','A COSMÉTIC PERFUMARIA'),('R$300 em consumação','THE WEEK'),('voucher R$250','HYPE BARBEARIA')]
gx,gy,ch=190,1000,300; gw=W-2*gx; cw=gw//2
it=[('Logo',logo(150,400)),('OS PRÊMIOS',sm(420,40,'O QUE ESTÁ EM JOGO')),('Título · os prêmios.',fr(510,200,'os prêmios.')),
    ('Grade (linhas)',(f"<div style='position:absolute;left:{gx}px;top:{gy}px;width:{gw}px;height:{2*ch}px;box-sizing:border-box;border-top:2px solid rgba(196,165,130,.45);border-bottom:2px solid rgba(196,165,130,.45)'></div><div style='position:absolute;left:{W//2-1}px;top:{gy+40}px;width:2px;height:{2*ch-80}px;background:rgba(196,165,130,.35)'></div><div style='position:absolute;left:{gx+40}px;top:{gy+ch-1}px;width:{gw-80}px;height:2px;background:rgba(196,165,130,.35)'></div>",None))]
for i,(v,sp) in enumerate(PR):
    x=gx+(i%2)*cw; yy=gy+(i//2)*ch
    it.append((f'Prêmio {i+1} · {v}',(f"<div style=\"position:absolute;left:{x}px;width:{cw}px;text-align:center;top:{yy+70}px;font-family:Fr;font-style:italic;font-size:84px;color:#efe4d0\">{v}</div>",{'text':v,'font':'Fraunces-Italic','size':84,'color':'#efe4d0','x':x+cw/2,'y':yy+137,'ls':0,'anchor':'middle'})))
    it.append((f'Patrocinador {i+1} · {sp}',(f"<div style=\"position:absolute;left:{x}px;width:{cw}px;text-align:center;top:{yy+190}px;font-family:SM;font-weight:700;font-size:32px;letter-spacing:.28em;text-indent:.28em;color:#c4a582\">{sp}</div>",{'text':sp,'font':'SpaceMono-Bold','size':32,'color':'#c4a582','x':x+cw/2,'y':yy+222,'ls':.28,'anchor':'middle'})))
it.append(('Vencedores',sm(1700,44,'2 VENCEDORES MASCULINOS · 2 FEMININOS','#efe4d0',.3)))
it.append(('Frase · cada vencedor leva um prêmio.',fr(1800,64,'cada vencedor leva um dos prêmios.','#c4a582')))
man.update(build(P+'-03-premios',bg_glow(1300),it,foot=2470,seed=13))
# 4 final
man.update(build(P+'-04-final',bg_photo(SC+'/hwf/premium_photo-1664033881574-af981f4edd53.png',-300,1200),[
  ('Logo',logo(150,560)),('no one leaves.',fr(325,64,'no one leaves.',extra='opacity:.9')),
  ('Frase · e aí, qual vai ser?',fr(1300,110,'e aí, qual vai ser a sua?')),
  ('Data · 02.11',(f"<div class='c' style=\"top:1480px;font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:380px;line-height:1;color:#efe4d0;text-shadow:0 0 60px rgba(196,165,130,.25),0 6px 30px rgba(0,0,0,.9)\">02.11</div>",{'text':'02.11','font':'Fraunces-Black','size':380,'color':'#efe4d0','x':W/2,'y':1480+300,'ls':0,'anchor':'middle'})),
  ('Info',sm(1930,42,'SEGUNDA · 17H · THE WEEK · JK RIO PRETO','#c4a582',.32)),
  ('INGRESSOS NA BIO',(f"<div style='position:absolute;left:50%;transform:translateX(-50%);top:2100px;border:3px solid rgba(196,165,130,.8);border-radius:999px;padding:34px 80px;font-family:SM;font-weight:700;font-size:44px;letter-spacing:.32em;color:#efe4d0;white-space:nowrap'>INGRESSOS NA BIO</div>",None))],foot=2470,seed=14))
json.dump(man,open(S+'/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok')
