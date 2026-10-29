import os, base64, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); F=S+'/fonts'
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
LOGO='/home/claude/whynot-/identidade/assets/logo/halloween/logo-why-not-halloween.png'
PH='/mnt/user-data/attachments/85f2d3d2-8d73-51f7-b638-521bd0946f03/f2dd82bc-Cinematic-still-life-photograph-an-orna.png'
W,H=3840,2160
c=Image.new('RGBA',(W,H),(11,7,6,255))
ph=Image.open(PH).convert('RGB'); k=H/ph.height*1.05; ph=ph.resize((round(ph.width*k),round(ph.height*k)),Image.LANCZOS)
ph=ImageEnhance.Brightness(ph).enhance(1.08)
m=Image.new('L',ph.size,255); d=ImageDraw.Draw(m)
for x in range(0,700): d.line((x,0,x,ph.height),fill=int(255*(x/700)**1.4))
for y in range(ph.height-300,ph.height): d.line((0,y,ph.width,y),fill=0)
m2=Image.new('L',ph.size,0); m2.paste(m)
for y in range(ph.height-500,ph.height):
    v=int(255*(ph.height-y)/500); ImageDraw.Draw(m2).line((0,y,ph.width,y),fill=0)
m=ImageChops.multiply(m,Image.linear_gradient('L').rotate(180).resize(ph.size).point(lambda v:min(255,int(v*3))))
pl=ph.convert('RGBA'); pl.putalpha(m); c.alpha_composite(pl,(W-ph.width+60,-60))
gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).ellipse((-400,200,2000,2100),fill=90); gm=gm.filter(ImageFilter.GaussianBlur(380))
gl=Image.new('RGBA',(W,H),(0,0,0,0)); gl.paste((122,58,22,255),(0,0),gm); c=Image.alpha_composite(c,Image.blend(Image.new('RGBA',(W,H),(0,0,0,0)),gl,1)) if False else c
base=c.convert('RGB'); glow=Image.new('RGB',(W,H),(0,0,0)); glow.paste((122,58,22),(0,0),gm); base=ImageChops.screen(base,glow)
vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse((-900,-500,W+900,H+500),fill=255); vg=vg.filter(ImageFilter.GaussianBlur(500))
base=Image.composite(base,ImageChops.multiply(base,Image.new('RGB',(W,H),(40,26,20))),vg)
c=base.convert('RGBA')
CSS=(f"@font-face{{font-family:'FrV';font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'Fr';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'/fv/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}"
 f"@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{b64(F+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}"
 f"html,body{{margin:0;width:{W}px;height:{H}px;background:transparent}}"
 ".col{position:absolute;left:300px;width:1900px;text-align:center;top:250px;color:#efe4d0}"
 ".sm{font-family:SM;font-weight:700;letter-spacing:.34em;text-indent:.34em}"
 ".it{font-family:Fr;font-style:italic;font-weight:400}")
html=(f"<div class=col>"
 f"<img src='data:image/png;base64,{b64(LOGO)}' style='width:980px;filter:drop-shadow(0 10px 40px rgba(0,0,0,.8))'>"
 "<div class=it style='font-size:96px;margin-top:20px;opacity:.9'>no one leaves.</div>"
 "<div style=\"font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;font-size:520px;line-height:1;margin-top:90px;letter-spacing:-.01em;text-shadow:0 0 90px rgba(196,165,130,.28)\">02.11</div>"
 "<div class=sm style='font-size:56px;color:#c4a582;margin-top:40px'>SEGUNDA · 17H · AQUI NO THE WEEK</div>"
 "<div class=it style='font-size:150px;margin-top:70px'>vem fantasiado.</div>"
 "<div class=sm style='font-size:40px;color:#c4a582;margin-top:34px;opacity:.9'>CONCURSO DE MELHOR FANTASIA COM PRÊMIOS</div>"
 "<div style='display:inline-block;margin-top:90px;border:4px solid rgba(196,165,130,.85);border-radius:999px;padding:34px 80px' class=sm><span style='font-size:46px'>INGRESSOS NO LINK DA BIO · @WHYNOT.SJRP</span></div>"
 "</div>")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    pg.set_content(f"<style>{CSS}</style>{html}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(600)
    pg.screenshot(path=S+'/_t.png',omit_background=True); b.close()
c.alpha_composite(Image.open(S+'/_t.png').convert('RGBA'))
random.seed(9); n=Image.effect_noise((W,H),22).convert('L'); c=c.convert('RGB'); c=Image.blend(c,ImageChops.overlay(c,Image.merge('RGB',(n,n,n))),0.16)
c.save(S+'/2910_tv_halloween-the-week_4K.png'); c.resize((1920,1080),Image.LANCZOS).save(S+'/2910_tv_halloween-the-week_1080p.png')
c.resize((1280,720)).save(S+'/_prev.png'); print('ok')
