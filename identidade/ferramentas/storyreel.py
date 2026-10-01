import numpy as np, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
exec(open('dj02reel.py').read().split('SRC = ')[0])   # consts + imports
src2=open('dj02reel.py').read()
exec(src2[src2.index('def grade'):src2.index('yv = np.linspace')])  # grade, txt, ext, put, ease, BG
def load(path, start, dur, vf):
    raw = subprocess.run(["ffmpeg","-loglevel","error","-ss",str(start),"-i",path,"-t",str(dur+0.1),"-vf",vf+f",fps={FPS},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    return raw
def frames(raw,h,w,n):
    fr=np.frombuffer(raw,np.uint8).reshape(-1,h,w)
    if len(fr)<n: fr=np.concatenate([fr,np.repeat(fr[-1:],n-len(fr),0)])
    return fr[:n]
C=0.9; n=int(C*FPS)
# Tom: band
tom=[]
for fn,crop,st,fo in [("take1.mp4",(1024,576,112,0),0.3,0.56),("take3.mp4",(1024,576,112,0),0.2,0.62),("take4.mp4",(1024,576,112,0),0.3,0.25)]:
    cw,ch,cx,cy=crop; sw=int(round(cw*BAND_H/ch/2)*2); x0=int(min(max(fo*sw-W/2,0),sw-W))
    tom.append(frames(load(os.path.join(D,'tom',fn),st,C,f"crop={cw}:{ch}:{cx}:{cy},scale={sw}:{BAND_H}:flags=lanczos,crop={W}:{BAND_H}:{x0}:0"),BAND_H,W,n))
may=[frames(load(os.path.join(D,'may/AFTER__MOVIE_MB.mp4'),st,C,f"scale={W}:{H}"),H,W,n) for st in (7.3,11.8,20.9)]
mex=[frames(load(os.path.join(D,'mex/video.mp4'),st,1.0,f"scale={W}:{H}"),H,W,30) for st in (5.2,7.2,8.2)]
yv=np.linspace(0,1,H)[:,None,None]
SH=np.clip(1-0.92*np.clip((0.30-yv)/0.30,0,1)**0.9-0.85*np.clip((yv-0.66)/0.34,0,1)**1.0,0,1)
F=lambda s:ImageFont.truetype(MONO,s); FB=lambda s:ImageFont.truetype(MONOB,s)
hdrL=txt("WHY NOT? · LINE-UP",F(34),ICE+(255,),6); hdrR=txt("09.10",F(34),ICE+(255,),6)
lab={1:(ext("01",200),txt("TOM KELLER",FB(64),ICE+(255,),10),txt("2× TOMORROWLAND",F(38),MUTED+(255,),8)),
     2:(ext("02",200),txt("MAYCON BEATS",FB(64),ICE+(255,),10),txt("BAILE FUNK RAVE",F(38),MUTED+(255,),8)),
     3:(ext("03",200),txt("? ? ?",FB(64),ICE+(255,),24),txt("QUEM SERÁ?",F(38),MUTED+(255,),8))}
intro_a=txt("WHY NOT? APRESENTA",F(36),MUTED+(255,),8); intro_b={k:ext("até agora.",190,layers=k) for k in range(13)}
end_a={k:ext("sexta.",240,layers=k) for k in range(13)}; end_b=txt("03 / 06 · 12H",FB(52),ICE+(255,),10); end_c=txt("FICA LIGADO NO FEED",F(36),MUTED+(255,),8)
INTRO=1.3; T1=INTRO+3*C; T2=T1+3*C; T3=T2+3.0; END=12.0
out=os.path.join(D,'whynot-story-lineup-ate-agora.mp4')
p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-f","lavfi","-t",str(END),"-i","anullsrc=r=44100:cl=stereo","-c:v","libx264","-pix_fmt","yuv420p","-b:v","12M","-preset","slow","-movflags","+faststart","-c:a","aac","-shortest",out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
def labels(cv,k,tt):
    num,name,sub=lab[k]; put(cv,num,80+num.width/2-30,1390,ease(tt/0.3)); put(cv,name,80+name.width/2,1560,ease((tt-0.15)/0.3)); put(cv,sub,80+sub.width/2,1640,ease((tt-0.3)/0.3))
for i in range(int(END*FPS)):
    t=i/FPS
    if t<INTRO:
        cv=Image.fromarray(BG.astype(np.uint8)).convert("RGBA"); put(cv,intro_a,W/2,760,ease(t/0.4)); put(cv,intro_b[int(min(12,t/0.6*12))],W/2,960,ease((t-0.1)/0.3))
    elif t<T1:
        tt=t-INTRO; k=min(int(tt//C),2); fi=min(int((tt-k*C)*FPS),n-1); arr=BG.copy(); arr[BAND_Y:BAND_Y+BAND_H]=grade(tom[k][fi])
        cv=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); labels(cv,1,tt)
    elif t<T2:
        tt=t-T1; k=min(int(tt//C),2); fi=min(int((tt-k*C)*FPS),n-1); arr=grade(may[k][fi])*SH
        cv=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); labels(cv,2,tt)
    elif t<T3:
        tt=t-T2; k=min(int(tt//1.0),2); fi=min(int((tt-k)*FPS),29)
        g=Image.fromarray(mex[k][fi]).filter(ImageFilter.GaussianBlur(9)); g=np.asarray(g).astype(np.float32)
        g=np.clip(g*0.75,0,255); arr=grade(g)*SH
        if rng.random()<0.12: arr=arr*0.35
        cv=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); labels(cv,3,tt)
    else:
        tt=t-T3; cv=Image.fromarray(BG.astype(np.uint8)).convert("RGBA")
        put(cv,end_a[int(min(12,tt/0.6*12))],W/2,880,ease(tt/0.3)); put(cv,end_b,W/2,1150,ease((tt-0.4)/0.4)); put(cv,end_c,W/2,1230,ease((tt-0.6)/0.4))
    if T1-0.001>t>=INTRO or T3>t>=T1 or t<INTRO: pass
    if INTRO<=t<T3: put(cv,hdrL,80+hdrL.width/2,320); put(cv,hdrR,W-80-hdrR.width/2,320)
    arr=np.asarray(cv.convert("RGB")).astype(np.float32)
    for b in (INTRO,T1,T2,T3):
        if 0<=t-b<0.07: arr=arr*0.3+np.array(ICE,np.float32)*0.7
    g=rng.normal(0,8,(H//2,W//2)).astype(np.float32); arr=np.clip(arr+np.repeat(np.repeat(g,2,0),2,1)[...,None],0,255)
    if t>END-0.2: arr*=max(0,(END-t)/0.2)
    p.stdin.write(arr.astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print("ok",os.path.getsize(out))
