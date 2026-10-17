import subprocess, os
S=os.path.dirname(os.path.abspath(__file__)); N='/mnt/user-data/uploads/Downloads/_claude_assets/snd/'
R='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/reel/'
W,H,FPS=1080,1920,30; CLIP=15.0; END=4.6; TOTAL=CLIP+END; V0=5.4
run=lambda a: subprocess.run(a, check=True)
# voz: +3 semitons (mais fina), mesma duração aproximada, eco leve
run(['ffmpeg','-v','error','-y','-i',S+'/voz.mp3','-af','aresample=44100,asetrate=44100*1.19,aresample=44100,atempo=0.88,aecho=0.85:0.55:150|310:0.2|0.1,highpass=f=120','-ar','48000','-ac','2',S+'/voz_fx.wav'])
GRADE=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,eq=brightness=-0.02:contrast=1.06:saturation=0.9,colorbalance=rs=.03:bs=-.04"
fo=lambda i,a,b: f"[{i}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b-0.3}:d=0.3:alpha=1[o{i}]"
fi=lambda i,a,lab: f"[{i}:v]format=rgba,fade=t=in:st={a}:d=0.7:alpha=1[{lab}]"
v=(f"[0:v]trim=0:{CLIP},setpts=PTS-STARTPTS,{GRADE},tpad=stop_mode=add:stop_duration={END}:color=0x0b0706,vignette=angle=PI/4.3,noise=alls=8:allf=t,format=yuv420p,fade=t=in:st=0:d=0.5[bg];"
   +fo(1,V0+3.0,V0+4.9)+';'+fo(2,V0+5.0,CLIP+0.05)+';'+fi(3,CLIP+0.2,'lg')+';'+fi(4,CLIP+0.8,'dt')+';'+fi(5,CLIP+1.3,'ti')+';'+fi(6,CLIP+1.9,'ct')+';'
   f"[bg][o1]overlay[a];[a][o2]overlay[b];[b][lg]overlay=enable='gte(t,{CLIP})'[c];[c][dt]overlay=enable='gte(t,{CLIP})'[d];[d][ti]overlay=enable='gte(t,{CLIP})'[e];[e][ct]overlay=enable='gte(t,{CLIP})',format=yuv420p[vout]")
A=['-i',S+'/voz_fx.wav','-i',N+'2022-04-23 Occult Blood - Spooky Times.wav','-i',N+'Laugh2.wav','-i',N+'2022-08-17 Approaching the Crash Site - Boom.wav']
a=(f"[7:a]volume=1.35,adelay={int(V0*1000)}|{int(V0*1000)}[vz];"
   f"[8:a]volume=0.5,afade=t=out:st={TOTAL-1.4}:d=1.4[dr];"
      f"[10:a]atrim=0:3.5,lowpass=f=170,lowpass=f=170,volume=1.5,adelay={int(CLIP*1000)}|{int(CLIP*1000)}[bm];"
   f"[vz][dr][bm]amix=inputs=3:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.2,atrim=0:{TOTAL}[aout]")
img=lambda p: ['-loop','1','-framerate',str(FPS),'-t',str(TOTAL),'-i',S+'/'+p]
run(['ffmpeg','-v','error','-y','-i',S+'/in.mp4']+img('s1.png')+img('s2.png')+img('e_logo.png')+img('e_date.png')+img('e_title.png')+img('e_cta.png')+A+
    ['-filter_complex',v+';'+a,'-map','[vout]','-map','[aout]','-t',str(TOTAL),'-c:v','libx264','-preset','slow','-crf','20','-maxrate','10M','-bufsize','20M','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','256k','-movflags','+faststart',S+'/1710_reels-palhaco-balao-ingressos.mp4'])
print('ok',TOTAL)
