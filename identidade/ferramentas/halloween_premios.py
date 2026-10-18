"""Prêmios do concurso de fantasia: máscara + 'melhor fantasia.' + grade dos 4 prêmios + rodapé patrocinadores. Feed 2160x2700 e story 2160x3840."""
import os, json, random, base64
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); SC='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
FOOT='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/patro/rodape_patrocinadores_2160.png'
F=SC+'/hwb/fonts'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode(); LOGO=SC+'/hwb/out/_logo_reto.png'
CSS=(f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 "html,body{margin:0;background:transparent}.c{position:absolute;text-align:center}")
PR=[('kit completo',"LA'BRIZZA"),('perfume','A COSMÉTIC PERFUMARIA'),('R$300 em consumação','THE WEEK'),('voucher R$250','HYPE BARBEARIA')]
def build(doc,W,H,L):
    D=os.path.join(S,doc); os.makedirs(D,exist_ok=True); layers=[]
    def add(name,im,blend=None,opacity=1,text=None):
        p=os.path.join(D,f'{len(layers):02d}.png'); im.save(p); d={'name':name,'png':p,'blend':blend,'opacity':opacity}
        if text: d['text']=text
        layers.append(d)
    add('Fundo',Image.new('RGBA',(W,H),(11,7,6,255)))
    ph=Image.open(SC+'/hwf/photo-1640869444601-e791c41bae6b.png').convert('RGB'); cw=round(1160*4/5); cx=1015
    ph=ph.crop((cx-cw//2,0,cx+cw//2,1160)); g=ImageOps.grayscale(ph).point(lambda v:max(0,v-10)*1.05)
    ph=ImageOps.colorize(g,black=(9,6,5),mid=(122,86,58),white=(228,214,190),midpoint=118)
    pw=L['ph_w']; ph=ph.resize((pw,round(ph.height*pw/ph.width)),Image.LANCZOS)
    m=Image.new('L',ph.size,0); ImageDraw.Draw(m).ellipse((90,90,ph.width-90,ph.height-90),fill=255); m=m.filter(ImageFilter.GaussianBlur(150))
    fo=Image.new('RGBA',(W,H),(0,0,0,0)); fl=ph.convert('RGBA'); fl.putalpha(m); fo.alpha_composite(fl,((W-pw)//2,L['ph_y'])); add('FOTO · máscara (Unsplash)',fo)
    gm=Image.new('L',(W,H),0); cy=L['ph_y']+ph.height//2; ImageDraw.Draw(gm).ellipse((W/2-650,cy-450,W/2+600,cy+400),fill=120); gm=gm.filter(ImageFilter.GaussianBlur(240))
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); gl.paste((122,58,22,255),(0,0),gm); add('Brilho brasa (tela)',gl,blend='screen',opacity=.6)
    gr=Image.linear_gradient('L').resize((W,H)); y0=L['dark_from']/H*255; gr=gr.point(lambda v:0 if v<y0 else min(255,(v-y0)*3.2))
    es=Image.new('RGBA',(W,H),(11,7,6,255)); es.putalpha(gr); add('Escurecer base (leitura do texto)',es)
    vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-500,-300,W+500,H+300),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(380))
    add('Vinheta',Image.composite(Image.new('RGBA',(W,H),(255,255,255,255)),Image.new('RGBA',(W,H),(36,24,18,255)),vg),blend='multiply')
    gx=L['grid_x']; gw=W-2*gx; cw2=gw//2; ch=L['cell_h']; gy=L['grid_y']
    items={'logo':f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-L['logo_w'])//2}px;top:{L['logo_y']}px;width:{L['logo_w']}px'>",
     'nol':f"<div class=c style=\"left:0;right:0;top:{L['nol_y']}px;font-family:Fr;font-style:italic;font-size:{L['nol_s']}px;color:#efe4d0;opacity:.9\">no one leaves.</div>",
     'kick':f"<div class=c style=\"left:0;right:0;top:{L['kick_y']}px;font-family:SM;font-weight:700;font-size:{L['kick_s']}px;letter-spacing:.42em;text-indent:.42em;color:#c4a582\">CONCURSO</div>",
     'title':f"<div class=c style=\"left:0;right:0;top:{L['title_y']}px;font-family:Fr;font-style:italic;font-size:{L['title_s']}px;line-height:1;color:#efe4d0;text-shadow:0 0 50px rgba(196,165,130,.25)\">melhor fantasia.</div>",
     'sub':f"<div class=c style=\"left:0;right:0;top:{L['sub_y']}px;font-family:Fr;font-style:italic;font-size:{L['sub_s']}px;color:#c4a582\">vem fantasiado e concorra.</div>",
     'grid':f"<div style='position:absolute;left:{gx}px;top:{gy}px;width:{gw}px;height:{2*ch}px;box-sizing:border-box;border-top:2px solid rgba(196,165,130,.45);border-bottom:2px solid rgba(196,165,130,.45)'></div>"
            f"<div style='position:absolute;left:{W//2-1}px;top:{gy+30}px;width:2px;height:{2*ch-60}px;background:rgba(196,165,130,.35)'></div>"
            f"<div style='position:absolute;left:{gx+40}px;top:{gy+ch-1}px;width:{gw-80}px;height:2px;background:rgba(196,165,130,.35)'></div>",
     'winners':f"<div class=c style=\"left:0;right:0;top:{L['win_y']}px;font-family:SM;font-weight:700;font-size:{L['win_s']}px;letter-spacing:.3em;text-indent:.3em;color:#efe4d0\">2 VENCEDORES MASCULINOS · 2 FEMININOS</div>",
     'info':f"<div class=c style=\"left:0;right:0;top:{L['info_y']}px;font-family:SM;font-weight:700;font-size:{L['info_s']}px;letter-spacing:.34em;text-indent:.34em;color:#c4a582\">02.11 · 17H · THE WEEK · JK RIO PRETO</div>"}
    for i,(v,sp) in enumerate(PR):
        x=gx+(i%2)*cw2; y=gy+(i//2)*ch
        items[f'v{i}']=f"<div class=c style=\"left:{x}px;width:{cw2}px;top:{y+L['val_dy']}px;font-family:Fr;font-style:italic;font-size:{L['val_s']}px;color:#efe4d0\">{v}</div>"
        items[f's{i}']=f"<div class=c style=\"left:{x}px;width:{cw2}px;top:{y+L['sp_dy']}px;font-family:SM;font-weight:700;font-size:{L['sp_s']}px;letter-spacing:.28em;text-indent:.28em;color:#c4a582\">{sp}</div>"
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={'width':W,'height':H})
        for k,body in items.items():
            pg.set_content(f"<style>{CSS}html,body{{width:{W}px;height:{H}px}}</style>{body}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{D}/_{k}.png',omit_background=True)
        br.close()
    im=lambda k: Image.open(f'{D}/_{k}.png').convert('RGBA')
    T=lambda t,f,s,c,x,y,ls=0:{'text':t,'font':f,'size':s,'color':c,'x':x,'y':y,'ls':ls,'anchor':'middle'}
    add('Logo why not? halloween',im('logo'))
    add('Slogan · no one leaves.',im('nol'),text=T('no one leaves.','Fraunces-Italic',L['nol_s'],'#efe4d0',W/2,L['nol_y']+L['nol_s']*.8))
    add('CONCURSO',im('kick'),text=T('CONCURSO','SpaceMono-Bold',L['kick_s'],'#c4a582',W/2,L['kick_y']+L['kick_s'],.42))
    add('Título · melhor fantasia.',im('title'),text=T('melhor fantasia.','Fraunces-Italic',L['title_s'],'#efe4d0',W/2,L['title_y']+L['title_s']*.8))
    add('Frase · vem fantasiado e concorra.',im('sub'),text=T('vem fantasiado e concorra.','Fraunces-Italic',L['sub_s'],'#c4a582',W/2,L['sub_y']+L['sub_s']*.8))
    add('Grade dos prêmios (linhas)',im('grid'))
    for i,(v,sp) in enumerate(PR):
        x=gx+(i%2)*cw2+cw2/2; y=gy+(i//2)*ch
        add(f'Prêmio {i+1} · {v}',im(f'v{i}'),text=T(v,'Fraunces-Italic',L['val_s'],'#efe4d0',x,y+L['val_dy']+L['val_s']*.8))
        add(f'Patrocinador {i+1} · {sp}',im(f's{i}'),text=T(sp,'SpaceMono-Bold',L['sp_s'],'#c4a582',x,y+L['sp_dy']+L['sp_s'],.28))
    add('Vencedores · 2 masc · 2 fem',im('winners'),text=T('2 VENCEDORES MASCULINOS · 2 FEMININOS','SpaceMono-Bold',L['win_s'],'#efe4d0',W/2,L['win_y']+L['win_s'],.3))
    add('Info · 02.11 · 17H · THE WEEK',im('info'),text=T('02.11 · 17H · THE WEEK · JK RIO PRETO','SpaceMono-Bold',L['info_s'],'#c4a582',W/2,L['info_y']+L['info_s'],.34))
    ft=Image.open(FOOT).convert('RGBA'); fl=Image.new('RGBA',(W,H),(0,0,0,0)); fl.alpha_composite(ft,(0,L['foot_y'])); add('Patrocinadores (rodapé)',fl)
    random.seed(6); n=Image.effect_noise((W,H),22).convert('L')
    add('Grão (sobrepor · 18%)',Image.merge('RGBA',(n,n,n,Image.new('L',(W,H),255))),blend='overlay',opacity=.18)
    c=Image.open(layers[0]['png']).convert('RGB')
    for d in layers[1:]:
        i=Image.open(d['png']).convert('RGBA'); a=i.split()[3].point(lambda v:v*d['opacity']); rgb=i.convert('RGB')
        if d['blend']=='multiply': rgb=ImageChops.multiply(c,rgb)
        elif d['blend']=='screen': rgb=ImageChops.screen(c,rgb)
        elif d['blend']=='overlay': rgb=ImageChops.overlay(c,rgb)
        c=Image.composite(rgb,c,a)
    c.save(D+'/_composite.png'); c.resize((W//2,H//2),Image.LANCZOS).save(f'{S}/{doc}.png')
    return {doc:{'width':W,'height':H,'layers':layers}}
man={}
man.update(build('1810_feed_premios-melhor-fantasia',2160,2700,dict(ph_w=1180,ph_y=360,dark_from=1150,logo_w=520,logo_y=130,nol_y=290,nol_s=60,
  kick_y=1240,kick_s=40,title_y=1310,title_s=210,sub_y=1550,sub_s=84,grid_x=190,grid_y=1720,cell_h=230,val_dy=52,val_s=76,sp_dy=152,sp_s=30,
  win_y=2228,win_s=38,info_y=2310,info_s=34,foot_y=2470)))
man.update(build('1810_story_premios-melhor-fantasia',2160,3840,dict(ph_w=1500,ph_y=560,dark_from=1650,logo_w=600,logo_y=320,nol_y=500,nol_s=70,
  kick_y=1780,kick_s=46,title_y=1860,title_s=240,sub_y=2130,sub_s=96,grid_x=170,grid_y=2340,cell_h=280,val_dy=70,val_s=80,sp_dy=186,sp_s=34,
  win_y=2960,win_s=44,info_y=3050,info_s=38,foot_y=3240)))
json.dump(man,open(S+'/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok')
