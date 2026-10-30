import subprocess, os
S=os.path.dirname(os.path.abspath(__file__)); SRC=S+'/v1.mp4'; FPS=30; OUT=S+'/3110_reels-atracao-surpresa-aloira.mp4'
INTRO=(25.6,4.7)
CUTS=[(0.2,0.9),(13.6,0.8),(12.0,1.0),(2.6,0.8),(25.6,1.0),(9.2,0.7),(33.0,0.8),(15.2,0.9),(1.6,0.8),(34.6,1.3)]
Q=2.3; T_CUT=4.7; CUTLEN=sum(d for _,d in CUTS); T_END=T_CUT+CUTLEN; END=3.0; TOTAL=T_END+END
GR="scale=1080:1920,setsar=1,fps=30,eq=contrast=1.1:brightness=-0.02:saturation=0.7,colorbalance=rs=.06:bs=-.08:rm=.04:bm=-.06,curves=all='0/0 0.08/0.03 0.5/0.48 1/0.96'"
f=[f"[0:v]split={len(CUTS)+1}"+''.join(f'[x{k}]' for k in range(len(CUTS)+1))]
f.append(f"[x0]trim={INTRO[0]}:{INTRO[0]+INTRO[1]},setpts=PTS-STARTPTS,{GR},gblur=sigma=14,eq=brightness=-0.25[s0]")
for k,(a,d) in enumerate(CUTS):
    f.append(f"[x{k+1}]trim={a}:{a+d},setpts=PTS-STARTPTS,{GR},scale=1134:2016,crop=1080:1920:'27+27*t/{d}':'48+48*t/{d}'[s{k+1}]")
n=len(CUTS)+1
f.append(''.join(f'[s{k}]' for k in range(n))+f"concat=n={n}:v=1:a=0,tpad=stop_mode=add:stop_duration={END}:color=0x0b0706,vignette=angle=PI/4.2,noise=alls=7:allf=t,format=yuv420p,fade=t=in:st=0:d=0.5[bg]")
fd=lambda i,a,b,fi,fo,l: f"[{i}:v]format=rgba,fade=t=in:st={a}:d={fi}:alpha=1,fade=t=out:st={b-fo}:d={fo}:alpha=1[{l}]"
f+= [fd(1,0.2,Q,0.5,0.4,'q'),fd(2,0.5,Q,0.5,0.4,'qt'),fd(3,Q,T_CUT,0.3,0.4,'rk'),fd(4,Q+0.25,T_CUT,0.5,0.4,'rl'),fd(5,Q+0.8,T_CUT,0.4,0.4,'rs'),fd(6,T_CUT+0.2,T_END,0.4,0.3,'tg')]
for i,(l,st) in enumerate([('lg',0.2),('dt',0.7),('ti',1.1),('ct',1.6)]): f.append(f"[{7+i}:v]format=rgba,fade=t=in:st={T_END+st}:d=0.6:alpha=1[{l}]")
f.append(f"[bg][q]overlay[a1];[a1][qt]overlay[a2];[a2][rk]overlay[a3];[a3][rl]overlay[a4];[a4][rs]overlay[a5];[a5][tg]overlay[a6];[a6][lg]overlay=enable='gte(t,{T_END})'[a7];[a7][dt]overlay=enable='gte(t,{T_END})'[a8];[a8][ti]overlay=enable='gte(t,{T_END})'[a9];[a9][ct]overlay=enable='gte(t,{T_END})',fade=t=out:st={TOTAL-0.35}:d=0.35,format=yuv420p[vout]")
img=lambda p: ['-loop','1','-framerate',str(FPS),'-t',str(TOTAL),'-i',S+'/'+p]
ins=['-i',SRC]+sum([img(x) for x in ['q.png','q_txt.png','r_kick.png','r_logo.png','r_sub.png','tag.png','e_logo.png','e_date.png','e_title.png','e_cta.png']],[])
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-f','lavfi','-t',str(TOTAL),'-i','anullsrc=r=48000:cl=stereo','-filter_complex',';'.join(f),'-map','[vout]','-map','11:a','-t',str(TOTAL),
  '-c:v','libx264','-preset','slow','-crf','18','-maxrate','12M','-bufsize','24M','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','128k','-movflags','+faststart',S+'/tmp_out.mp4'],check=True)
os.replace(S+'/tmp_out.mp4',OUT); print('ok',TOTAL)
