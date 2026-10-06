import os, subprocess, asyncio, numpy as np
from PIL import Image
D='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
W,H,FPS=1080,1920,30
FD="file://"+D+"/fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/"
intro=f"""<html><head><style>
@font-face{{font-family:F;font-weight:900;src:url('{FD}Fraunces144pt-Black.ttf')}}
@font-face{{font-family:F;font-style:italic;src:url('{FD}Fraunces72pt-Italic.ttf')}}
@font-face{{font-family:M;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')}}
body{{margin:0}} .w{{width:1080px;height:1920px;background:#e4f2f6;position:relative;color:#060a0c}}
.ex{{text-shadow:-2px 2px 0 #35535c,-4px 4px 0 #41646e,-6px 6px 0 #4f7580,-8px 8px 0 #5f8792,-10px 10px 0 #7199a4,-12px 12px 0 #85abb5,-14px 14px 0 #9bbdc6,-16px 16px 0 #b3cfd6,-18px 18px 0 #c3dbe1,-20px 20px 0 #cfe3e8}}
</style></head><body><div class="w">
<div style="position:absolute;left:80px;right:80px;top:270px;display:flex;justify-content:space-between;font:32px M;letter-spacing:.14em;color:#2f4e56"><span>WHY NOT? APRESENTA</span><span>09.10</span></div>
<div style="position:absolute;left:80px;top:760px">
<div class="ex" style="font:900 230px/0.86 F;transform:rotate(-6deg);transform-origin:left bottom">line-up</div>
<div style="font:italic 96px F;margin:60px 0 0 10px">completo.</div></div>
</div></body></html>"""
async def snap():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':H})
        open(D+'/r42/intro.html','w').write(intro); await pg.goto('file://'+D+'/r42/intro.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=D+'/r42/intro.png'); await b.close()
asyncio.run(snap())
def img(p): return np.asarray(Image.open(p).convert('RGB').resize((W,H)),dtype=np.float32)
def clip(path,st,dur):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(st),'-t',str(dur),'-i',path,'-vf',f'scale={W}:{H},fps={FPS}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32)
def zoom(a,s):
    if abs(s-1)<1e-3: return a
    im=Image.fromarray(a.astype(np.uint8)); w,h=int(W*s),int(H*s); im=im.resize((w,h),Image.BICUBIC)
    l,t=(w-W)//2,(h-H)//2; return np.asarray(im.crop((l,t,l+W,t+H)),dtype=np.float32)
ICE=np.array([228,242,246],np.float32)
DJ=[('dj01-tomkeller','DJ01Capa'),('dj02-mayconbeats','DJ02Capa'),('dj04-possani','DJ04Capa'),('dj03-mexikanno','DJ03Capa'),('dj06-maka','DJ06Capa'),('dj05-coiote','DJ05Capa')]
TAKE_ST={'dj01-tomkeller':2.4,'dj02-mayconbeats':2.4,'dj04-possani':2.4,'dj03-mexikanno':2.4,'dj06-maka':2.4,'dj05-coiote':2.4}
out=D+'/whynot-reels-6djs-lineup.mp4'
ff=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-f','lavfi','-t','16','-i','anullsrc=r=44100:cl=stereo','-c:v','libx264','-pix_fmt','yuv420p','-b:v','9M','-preset','medium','-movflags','+faststart','-c:a','aac','-shortest',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
w=lambda a: ff.stdin.write(np.clip(a,0,255).astype(np.uint8).tobytes())
ease=lambda x:1-(1-max(0,min(1,x)))**3
# intro 1.4s
I=img(D+'/r42/intro.png'); n=int(1.4*FPS)
for i in range(n):
    t=i/n; a=ease(t*2.2); w(ICE*(1-a)+zoom(I,1.06-0.06*ease(t))*a)
# DJs
for vid,cap in DJ:
    C=clip(D+f'/whynot-{vid}.mp4',TAKE_ST[vid],1.0)
    for k,f in enumerate(C[:30]):
        f=zoom(f,1.0+0.04*k/30)
        if k<3: f=f*(k/3)+255*(1-k/3)  # flash in
        w(f)
    P=img(D+f'/r42/{cap}.png'); m=int(0.8*FPS)
    for k in range(m):
        f=zoom(P,1.07-0.07*ease(k/m))
        if k<3: f=f*(k/3)+ICE*(1-k/3)
        w(f)
# end card 3.6s
E_=img(D+'/r42/Reels6Capa.png'); n=int(3.6*FPS)
for i in range(n):
    t=i/n; f=zoom(E_,1.06-0.06*ease(t*1.5))
    if i<5: f=f*(i/5)+255*(1-i/5)
    w(f)
ff.stdin.close(); ff.wait(); print(out)
