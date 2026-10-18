import subprocess, os
S=os.path.dirname(os.path.abspath(__file__)); B='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/balao/'
SRC='/mnt/user-data/uploads/CAIO_2026.mp4'; W,H,FPS=1080,1920,30
INTRO=(13.6,4.7)   # fundo das logos (escurecido)
CUTS=[(3.0,0.9),(12.6,0.8),(4.75,0.45),(19.6,1.0),(17.4,0.8),(25.3,1.0),(35.0,1.0),(30.0,1.35)]
T_LOG=0.0; T_CAIO=2.2; T_CUT=4.7; CUTLEN=sum(d for _,d in CUTS); T_END=T_CUT+CUTLEN; END=3.0; TOTAL=T_END+END
GR="scale=1080:1920,setsar=1,fps=30,eq=contrast=1.12:brightness=-0.03:saturation=0.42:gamma=0.95,colorbalance=rs=.10:gs=.02:bs=-.10:rm=.06:bm=-.08:rh=.04:bh=-.06,curves=all='0/0 0.08/0.03 0.5/0.47 1/0.94'"
f=[f"[0:v]trim={INTRO[0]}:{INTRO[0]+INTRO[1]},setpts=PTS-STARTPTS,{GR},gblur=sigma=6,eq=brightness=-0.16[s0]"]
for k,(a,d) in enumerate(CUTS):
    f.append(f"[0:v]trim={a}:{a+d},setpts=PTS-STARTPTS,{GR},scale=1134:2016,crop=1080:1920:'27+27*t/{d}':'48+48*t/{d}'[s{k+1}]")
n=len(CUTS)+1
f.append(''.join(f'[s{k}]' for k in range(n))+f"concat=n={n}:v=1:a=0,tpad=stop_mode=add:stop_duration={END}:color=0x0b0706,vignette=angle=PI/4.2,noise=alls=9:allf=t,format=yuv420p,fade=t=in:st=0:d=0.6[bg]")
fade=lambda i,a,b,fi,fo,l: f"[{i}:v]format=rgba,fade=t=in:st={a}:d={fi}:alpha=1,fade=t=out:st={b-fo}:d={fo}:alpha=1[{l}]"
f.append(fade(1,0.3,T_CAIO,0.7,0.5,'o1')); f.append(fade(2,T_CAIO,T_CUT,0.6,0.6,'o2')); f.append(fade(3,T_CUT+0.2,T_END,0.4,0.3,'o3'))
for i,(lab,st) in enumerate([('lg',0.2),('dt',0.7),('ti',1.1),('ct',1.6)]):
    f.append(f"[{4+i}:v]format=rgba,fade=t=in:st={T_END+st}:d=0.6:alpha=1[{lab}]")
f.append(f"[bg][o1]overlay[a];[a][o2]overlay[b];[b][o3]overlay[c];[c][lg]overlay=enable='gte(t,{T_END})'[d];[d][dt]overlay=enable='gte(t,{T_END})'[e];[e][ti]overlay=enable='gte(t,{T_END})'[g];[g][ct]overlay=enable='gte(t,{T_END})',fade=t=out:st={TOTAL-0.35}:d=0.35,format=yuv420p[vout]")
img=lambda p: ['-loop','1','-framerate',str(FPS),'-t',str(TOTAL),'-i',p]
subprocess.run(['ffmpeg','-v','error','-y','-i',SRC]+img(S+'/i_logo.png')+img(S+'/c_logo.png')+img(S+'/l_tag.png')+img(B+'e_logo.png')+img(B+'e_date.png')+img(B+'e_title.png')+img(B+'e_cta.png')+
  ['-f','lavfi','-t',str(TOTAL),'-i','anullsrc=r=48000:cl=stereo','-filter_complex',';'.join(f),'-map','[vout]','-map','8:a','-t',str(TOTAL),
   '-c:v','libx264','-preset','slow','-crf','18','-maxrate','12M','-bufsize','24M','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','128k','-movflags','+faststart',S+'/1810_reels-dj01-caio-tofole.mp4'],check=True)
print('ok',TOTAL)
