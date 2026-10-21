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

P='2410_carrossel-inspiracao'
LOOKS=[('f_vampira','vampira vitoriana','FEMININA','vestido de renda preta, gola alta,<br>batom vinho e um castiçal na mão.'),
 ('m_vampiro','vampiro clássico','MASCULINA','terno escuro, capa com forro vermelho,<br>cabelo pra trás e presas.'),
 ('f_noiva','noiva fantasma','FEMININA','vestido branco rasgado, véu longo,<br>olheira escura e buquê de flores secas.'),
 ('m_esqueleto','esqueleto de terno','MASCULINA','terno e gravata-borboleta pretos,<br>caveira no rosto e luvas brancas.'),
 ('f_bruxa','bruxa','FEMININA','chapéu de aba larga, vestido preto longo,<br>anéis prata e olho esfumado.'),
 ('m_peste','médico da peste','MASCULINA','sobretudo de couro, máscara de bico,<br>chapéu e uma lanterna.')]
man={}
# capa: grade 3x2 com os 6 looks
g=Image.new('RGBA',(W,H),(11,7,6,255)); tw,th=W//3,H//2
for k,(f,*_ ) in enumerate([l for l in LOOKS]):
    im=Image.open(S+f'/{f}.png').convert('RGB'); s=max(tw/im.width,th/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-tw)//2; y=max(0,int((im.height-th)*0.25)); g.paste(im.crop((x,y,x+tw,y+th)),((k%3)*tw,(k//3)*th))
dk=Image.new('RGBA',(W,H),(11,7,6,60))
gr=Image.linear_gradient('L').resize((W,H)).point(lambda v:int(max(0,min(255,(abs(v-150)*-2.6+255)))*.8))
band=Image.new('RGBA',(W,H),(11,7,6,255)); band.putalpha(gr)
man.update(build(P+'-01-capa',[('FOTOS · grade dos 6 looks',g,None,1),('Escurecer',dk,None,1),('Faixa escura (título)',band,None,1)],[
  ('Logo',logo(960,460)),
  ('INSPIRAÇÃO',sm(1180,44,'NÃO SABE DO QUE IR?')),('Título',fr(1260,220,'inspiração<br>de fantasia.',extra='line-height:1')),
  ('3 + 3',sm(1780,38,'3 FEMININAS · 3 MASCULINAS','#efe4d0',.34)),('ARRASTA',sm(2450,36,'ARRASTA  →','#c4a582',.5))],seed=31))
for i,(f,nome,tipo,dica) in enumerate(LOOKS):
    man.update(build(P+f'-{i+2:02d}-{f}',bg_photo(S+f'/{f}.png',0,1600),[
      ('Logo',logo(130,320)),
      (f'Número {i+1:02d}/06',sm(1920,34,f'{i+1:02d}/06 · {tipo}','#c4a582',.36)),
      (f'Nome · {nome}',fr(1990,170,nome)),
      ('Dica',(f"<div class='c sh' style=\"top:2220px;font-family:SM;font-weight:700;font-size:40px;line-height:1.5;letter-spacing:.03em;color:rgba(239,228,208,.85)\">{dica}</div>",{'text':dica.replace('<br>',' '),'font':'SpaceMono-Bold','size':40,'color':'#efe4d0','x':W/2,'y':2260,'ls':.03,'anchor':'middle'}))],seed=32+i))
man.update(build(P+'-08-final',bg_glow(1200),[
  ('Logo',logo(150,560)),('no one leaves.',fr(325,64,'no one leaves.',extra='opacity:.9')),
  ('Frase',fr(900,200,'qual vai ser<br>a sua?',extra='line-height:1')),
  ('Concurso',fr(1420,76,'a melhor fantasia leva prêmio.','#c4a582')),
  ('2+2',sm(1560,40,'2 VENCEDORES MASCULINOS · 2 FEMININOS','#efe4d0',.3)),
  ('Info',sm(1800,42,'02.11 · 17H · THE WEEK · JK RIO PRETO','#c4a582',.32)),
  ('INGRESSOS NA BIO',(f"<div style='position:absolute;left:50%;transform:translateX(-50%);top:1960px;border:3px solid rgba(196,165,130,.8);border-radius:999px;padding:34px 80px;font-family:SM;font-weight:700;font-size:44px;letter-spacing:.32em;color:#efe4d0;white-space:nowrap'>INGRESSOS NA BIO</div>",None))],foot=2470,seed=39))
json.dump(man,open(S+'/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok')
