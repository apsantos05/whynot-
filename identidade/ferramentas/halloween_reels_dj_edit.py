import subprocess, os
S=os.path.dirname(os.path.abspath(__file__)); B='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/balao/'
SRC=[S+'/v1.mp4',S+'/v2.mp4',S+'/v3.mp4']; FPS=30; OUT=S+'/1910_reels-dj02-oliver.mp4'
INTRO=(1,0.3,4.7)  # (fonte, início, duração) fundo das logos
CUTS=[(1,14.2,0.8),(0,4.0,1.0),(2,10.5,0.9),(1,2.0,0.6),(0,22.0,1.0),(2,15.0,0.7),(1,15.5,0.8),(2,6.0,1.5)]
T_CAIO=2.2; T_CUT=4.7; CUTLEN=sum(c[2] for c in CUTS); T_END=T_CUT+CUTLEN; END=3.0; TOTAL=T_END+END
GR="scale=1080:1920,setsar=1,fps=30,eq=contrast=1.12:brightness=-0.03:saturation=0.42:gamma=0.95,colorbalance=rs=.10:gs=.02:bs=-.10:rm=.06:bm=-.08:rh=.04:bh=-.06,curves=all='0/0 0.08/0.03 0.5/0.47 1/0.94'"
n_src=len(SRC); f=[]
uses=[INTRO[0]]+[c[0] for c in CUTS]
from collections import Counter
cnt=Counter(uses); lab={}
for s,k in cnt.items():
    f.append(f"[{s}:v]split={k}"+''.join(f'[x{s}_{j}]' for j in range(k))); lab[s]=0
def take(s):
    l=f'x{s}_{lab[s]}'; lab[s]+=1; return l
f.append(f"[{take(INTRO[0])}]trim={INTRO[1]}:{INTRO[1]+INTRO[2]},setpts=PTS-STARTPTS,{GR},gblur=sigma=6,eq=brightness=-0.16[s0]")
for k,(s,a,d) in enumerate(CUTS):
    f.append(f"[{take(s)}]trim={a}:{a+d},setpts=PTS-STARTPTS,{GR},scale=1134:2016,crop=1080:1920:'27+27*t/{d}':'48+48*t/{d}'[s{k+1}]")
n=len(CUTS)+1
f.append(''.join(f'[s{k}]' for k in range(n))+f"concat=n={n}:v=1:a=0,tpad=stop_mode=add:stop_duration={END}:color=0x0b0706,vignette=angle=PI/4.2,noise=alls=9:allf=t,format=yuv420p,fade=t=in:st=0:d=0.6[bg]")
o=n_src
fade=lambda i,a,b,fi,fo,l: f"[{i}:v]format=rgba,fade=t=in:st={a}:d={fi}:alpha=1,fade=t=out:st={b-fo}:d={fo}:alpha=1[{l}]"
f.append(fade(o,0.3,T_CAIO,0.7,0.5,'o1')); f.append(fade(o+1,T_CAIO,T_CUT,0.6,0.6,'o2')); f.append(fade(o+2,T_CUT+0.2,T_END,0.4,0.3,'o3'))
for i,(l,st) in enumerate([('lg',0.2),('dt',0.7),('ti',1.1),('ct',1.6)]):
    f.append(f"[{o+3+i}:v]format=rgba,fade=t=in:st={T_END+st}:d=0.6:alpha=1[{l}]")
f.append(f"[bg][o1]overlay[a];[a][o2]overlay[b];[b][o3]overlay[c];[c][lg]overlay=enable='gte(t,{T_END})'[d];[d][dt]overlay=enable='gte(t,{T_END})'[e];[e][ti]overlay=enable='gte(t,{T_END})'[g];[g][ct]overlay=enable='gte(t,{T_END})',fade=t=out:st={TOTAL-0.35}:d=0.35,format=yuv420p[vout]")
img=lambda p: ['-loop','1','-framerate',str(FPS),'-t',str(TOTAL),'-i',p]
ins=sum([['-i',s] for s in SRC],[])
subprocess.run(['ffmpeg','-v','error','-y']+ins+img(S+'/i_logo.png')+img(S+'/c_logo.png')+img(S+'/l_tag.png')+img(B+'e_logo.png')+img(B+'e_date.png')+img(B+'e_title.png')+img(B+'e_cta.png')+
  ['-f','lavfi','-t',str(TOTAL),'-i','anullsrc=r=48000:cl=stereo','-filter_complex',';'.join(f),'-map','[vout]','-map',f'{o+7}:a','-t',str(TOTAL),
   '-c:v','libx264','-preset','slow','-crf','18','-maxrate','12M','-bufsize','24M','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','128k','-movflags','+faststart',OUT],check=True)
print('ok',TOTAL)
