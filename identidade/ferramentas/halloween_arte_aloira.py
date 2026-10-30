import os, base64, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); F='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/tv/fonts'
R='/home/claude/whynot-/identidade'; LOGO=R+'/assets/logo/halloween/logo-why-not-halloween.png'; FOOT=R+'/halloween-no-one-leaves/patrocinadores/rodape_patrocinadores_2160.png'; AL=S+'/logo_aloira.png'
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 "html,body{margin:0;background:transparent}.c{position:absolute;left:0;right:0;text-align:center}"
 ".sm{font-family:SM;font-weight:700;letter-spacing:.4em;text-indent:.4em;color:#c4a582;text-shadow:0 2px 20px rgba(0,0,0,.9)}.it{font-family:Fr;font-style:italic;color:#efe4d0;text-shadow:0 4px 30px rgba(0,0,0,.95)}")
def build(name,W,H,L,foot=True):
    ph=Image.open(S+'/foto.jpg').convert('RGB'); k=max(W/ph.width,H/ph.height)*L['zoom']; ph=ph.resize((round(ph.width*k),round(ph.height*k)),Image.LANCZOS)
    ph=ImageEnhance.Color(ph).enhance(0.8); r,g,b=ph.split()
    ph=Image.merge('RGB',(r.point(lambda v:int(255*((v/255)**1.25)*0.95)),g.point(lambda v:int(255*((v/255)**1.35)*0.8)),b.point(lambda v:int(255*((v/255)**1.5)*0.62))))
    c=Image.new('RGB',(W,H),(11,7,6)); m=Image.new('L',ph.size,255); dm=ImageDraw.Draw(m)
    for y in range(0,int(300*W/2160)): dm.line((0,y,ph.width,y),fill=int(255*y/(300*W/2160)))
    c.paste(ph,((W-ph.width)//2,L['ph_y']),m)
    c=c.convert('RGBA')
    gr=Image.linear_gradient('L').resize((W,H)); y0=L['dark_from']/H*255; gr=gr.point(lambda v:0 if v<y0 else min(248,int((v-y0)*2.8)))
    es=Image.new('RGBA',(W,H),(11,7,6,255)); es.putalpha(gr); c.alpha_composite(es)
    tp=Image.linear_gradient('L').resize((W,H)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v:max(0,int((v-200)*4.2)))
    et=Image.new('RGBA',(W,H),(11,7,6,255)); et.putalpha(tp); c.alpha_composite(et)
    vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-W*.3,-H*.2,W*1.3,H*1.2),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(W//5))
    base=c.convert('RGB'); base=Image.composite(base,ImageChops.multiply(base,Image.new('RGB',(W,H),(36,24,18))),vg); c=base.convert('RGBA')
    s=W/2160
    h=(f"<img src='data:image/png;base64,{b64(LOGO)}' style='position:absolute;left:{(W-int(520*s))//2}px;top:{L['logo_y']}px;width:{int(520*s)}px'>"
       f"<div class='c it' style='top:{L['logo_y']+int(155*s)}px;font-size:{int(60*s)}px;opacity:.9'>no one leaves.</div>"
       f"<div class='c sm' style='top:{L['k_y']}px;font-size:{int(42*s)}px'>A ATRAÇÃO SURPRESA É</div>"
       f"<img src='data:image/png;base64,{b64(AL)}' style='position:absolute;left:{(W-int(1500*s))//2}px;top:{L['k_y']+int(90*s)}px;width:{int(1500*s)}px;filter:drop-shadow(0 0 {int(60*s)}px rgba(196,165,130,.45)) drop-shadow(0 {int(8*s)}px {int(40*s)}px rgba(0,0,0,.9))'>"
       f"<div class='c it' style='top:{L['k_y']+int(500*s)}px;font-size:{int(96*s)}px'>ela vem pro nosso halloween.</div>"
       f"<div class='c sm' style='top:{L['k_y']+int(680*s)}px;font-size:{int(36*s)}px;letter-spacing:.32em;text-indent:.32em'>02.11 · SEGUNDA · 17H · THE WEEK · JK RIO PRETO</div>")
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
        pg.set_content(f"<style>{CSS}html,body{{width:{W}px;height:{H}px}}</style>{h}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(500)
        pg.screenshot(path=S+'/_t.png',omit_background=True); b.close()
    c.alpha_composite(Image.open(S+'/_t.png').convert('RGBA'))
    if foot:
        ft=Image.open(FOOT).convert('RGBA')
        if ft.width!=W: ft=ft.resize((W,round(ft.height*W/ft.width)),Image.LANCZOS)
        c.alpha_composite(ft,(0,L['foot_y']))
    random.seed(4); n=Image.effect_noise((W,H),22).convert('L'); c=c.convert('RGB'); c=Image.blend(c,ImageChops.overlay(c,Image.merge('RGB',(n,n,n))),0.16)
    c.save(S+f'/{name}.png')
build('3110_feed_atracao-surpresa-aloira',2160,2700,dict(zoom=1.0,ph_y=300,dark_from=1350,logo_y=120,k_y=1560,foot_y=2470))
build('3110_story_atracao-surpresa-aloira',2160,3840,dict(zoom=1.0,ph_y=560,dark_from=2050,logo_y=320,k_y=2300,foot_y=3240))
build('3110_capa-reels-atracao-surpresa-aloira',1080,1920,dict(zoom=1.0,ph_y=290,dark_from=1000,logo_y=230,k_y=1200,foot_y=0),foot=False)
print('ok')
