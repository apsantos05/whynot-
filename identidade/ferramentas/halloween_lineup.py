import os, base64, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); F='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/tv/fonts'
R='/home/claude/whynot-/identidade'; b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
LOGO=R+'/assets/logo/halloween/logo-why-not-halloween.png'; FOOT=R+'/halloween-no-one-leaves/patrocinadores/rodape_patrocinadores_2160.png'
D=R+'/halloween-no-one-leaves/djs/'
DJS=[('01','Caio Tofole','logo_caio-tofole.png'),('02','Oliver','logo_oliver.png'),('03','Matheus Sanchez','logo_matheus.png'),('04','Possani','logo_possani.png'),('05','Maka','logo_maka.png'),('06','Coiote','logo_coiote.png')]
def build(name,W,H,L):
    c=Image.new('RGB',(W,H),(11,7,6))
    gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).ellipse((W/2-1100,L['grid_y']-300,W/2+1100,L['grid_y']+L['ch']*3+300),fill=110); gm=gm.filter(ImageFilter.GaussianBlur(380))
    gl=Image.new('RGB',(W,H),(0,0,0)); gl.paste((122,58,22),(0,0),gm); c=ImageChops.screen(c,gl)
    vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-600,-400,W+600,H+400),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(420))
    c=Image.composite(c,ImageChops.multiply(c,Image.new('RGB',(W,H),(36,24,18))),vg).convert('RGBA')
    CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
     f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
     f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
     f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}.c{{position:absolute;left:0;right:0;text-align:center}}"
     ".sm{font-family:SM;font-weight:700;letter-spacing:.34em;text-indent:.34em}.it{font-family:Fr;font-style:italic}")
    gx=L['gx']; gw=W-2*gx; cw=gw//2; ch=L['ch']; gy=L['grid_y']
    h=[f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-L['logo_w'])//2}px;top:{L['logo_y']}px;width:{L['logo_w']}px'>",
       f"<div class='c it' style='top:{L['nol_y']}px;font-size:{L['nol_s']}px;color:#efe4d0;opacity:.9'>no one leaves.</div>",
       f"<div class='c sm' style='top:{L['k_y']}px;font-size:{L['k_s']}px;color:#c4a582'>LINE-UP COMPLETO</div>",
       f"<div class='c it' style='top:{L['t_y']}px;font-size:{L['t_s']}px;line-height:1;color:#efe4d0;text-shadow:0 0 60px rgba(196,165,130,.25)'>seis nomes. uma noite.</div>",
       f"<div style='position:absolute;left:{gx}px;top:{gy}px;width:{gw}px;height:{3*ch}px;box-sizing:border-box;border-top:2px solid rgba(196,165,130,.4);border-bottom:2px solid rgba(196,165,130,.4)'></div>",
       f"<div style='position:absolute;left:{W//2-1}px;top:{gy+40}px;width:2px;height:{3*ch-80}px;background:rgba(196,165,130,.3)'></div>"]
    for r in (1,2): h.append(f"<div style='position:absolute;left:{gx+40}px;top:{gy+r*ch-1}px;width:{gw-80}px;height:2px;background:rgba(196,165,130,.3)'></div>")
    for i,(n,nm,f) in enumerate(DJS):
        x=gx+(i%2)*cw; y=gy+(i//2)*ch
        im=Image.open(D+f); mw,mh=L['lw'],L['lh']; k=min(mw/im.width,mh/im.height); w,hh=int(im.width*k),int(im.height*k)
        h.append(f"<img src='data:image/png;base64,{b64(D+f)}' style='position:absolute;left:{x+(cw-w)//2}px;top:{y+L['l_dy']+(mh-hh)//2}px;width:{w}px;height:{hh}px'>")
        h.append(f"<div class='sm' style='position:absolute;left:{x}px;width:{cw}px;text-align:center;top:{y+L['n_dy']}px;font-size:{L['n_s']}px;color:#c4a582'>DJ {n} · {nm.upper()}</div>")
    h.append(f"<div class='c it' style='top:{L['s_y']}px;font-size:{L['s_s']}px;color:#efe4d0'>+ atração surpresa. <span style='color:#c4a582'>revelação amanhã.</span></div>")
    h.append(f"<div class='c sm' style='top:{L['i_y']}px;font-size:{L['i_s']}px;color:#c4a582'>02.11 · SEGUNDA · 17H · THE WEEK · JK RIO PRETO</div>")
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
        pg.set_content(f"<style>{CSS}</style>"+''.join(h)); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(600)
        pg.screenshot(path=S+'/_t.png',omit_background=True); b.close()
    c.alpha_composite(Image.open(S+'/_t.png').convert('RGBA'))
    ft=Image.open(FOOT).convert('RGBA'); 
    if ft.width!=W: ft=ft.resize((W,round(ft.height*W/ft.width)),Image.LANCZOS)
    c.alpha_composite(ft,(0,L['foot_y']))
    random.seed(5); n=Image.effect_noise((W,H),22).convert('L'); c=c.convert('RGB'); c=Image.blend(c,ImageChops.overlay(c,Image.merge('RGB',(n,n,n))),0.16)
    c.save(S+f'/{name}.png')
build('3010_feed_line-up-completo',2160,2700,dict(logo_w=520,logo_y=130,nol_y=290,nol_s=60,k_y=470,k_s=40,t_y=545,t_s=150,gx=150,grid_y=800,ch=440,lw=680,lh=230,l_dy=70,n_dy=330,n_s=30,s_y=2170,s_s=80,i_y=2330,i_s=34,foot_y=2470))
build('3010_story_line-up-completo',2160,3840,dict(logo_w=600,logo_y=320,nol_y=500,nol_s=70,k_y=780,k_s=46,t_y=860,t_s=170,gx=130,grid_y=1180,ch=560,lw=760,lh=280,l_dy=100,n_dy=420,n_s=34,s_y=2920,s_s=90,i_y=3090,i_s=38,foot_y=3240))
print('ok')
