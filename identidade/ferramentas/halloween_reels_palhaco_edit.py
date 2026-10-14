"""Reels curto do palhaço: clipe + risadas no sorriso + cartão why not? / no one leaves. / COMING SOON."""
import subprocess, os
S = os.path.dirname(os.path.abspath(__file__))
O = os.path.join(S, '..', 'hgf') + '/'          # PNGs de texto/logo já renderizados
R = os.path.join(S, '..', 'reel') + '/'
N = '/mnt/user-data/uploads/Downloads/_claude_assets/snd/'
W, H, FPS = 1080, 1920, 30
CLIP = 5.0            # usa o clipe inteiro
HOLD = 3.6            # cartão sobre o último quadro escurecido
TOTAL = CLIP + HOLD
run = lambda a: subprocess.run(a, check=True)

GRADE = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
         "eq=brightness=-0.03:contrast=1.08:saturation=0.86,colorbalance=rs=.05:bs=-.06:rm=.04:bm=-.04")
# clipe + congelamento do último quadro com leve zoom e escurecimento
v = (f"[0:v]{GRADE},trim=0:{CLIP},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={HOLD},"
     f"zoompan=z='if(gte(in_time,{CLIP}),1+0.012*(in_time-{CLIP}),1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
     f"eq=brightness='if(gte(t,{CLIP}),-0.03-min((t-{CLIP})/0.6,1)*0.20,-0.03)':eval=frame,"
     f"vignette=angle=PI/4.2,noise=alls=9:allf=t,format=yuv420p,fade=t=in:st=0:d=0.4[bg];"
     f"[1:v]format=rgba,fade=t=in:st={CLIP+0.15}:d=0.8:alpha=1[lg];"
     f"[2:v]format=rgba,fade=t=in:st={CLIP+0.9}:d=0.7:alpha=1[ti];"
     f"[3:v]format=rgba,fade=t=in:st={CLIP+1.6}:d=0.5:alpha=1[so];"
     f"[bg][lg]overlay=enable='gte(t,{CLIP})'[a];[a][ti]overlay=enable='gte(t,{CLIP})'[b];"
     f"[b][so]overlay=enable='gte(t,{CLIP})',format=yuv420p[vout]")

ECHO = 'aecho=0.8:0.6:140|300:0.25|0.12'
A = [  # arquivo, inicio, volume, filtro extra
    (N + '2022-04-23 Occult Blood - Spooky Times.wav', 0.0, 0.55, f',afade=t=out:st={TOTAL-1.4}:d=1.4'),
    (N + '2022-04-16 Triple-C THICCC - Heavy Breathing.wav', 0.6, 0.25, ',atrim=0:2.4,afade=t=out:st=1.8:d=0.6'),
    (R + 'laugh_deep.wav', 3.62, 1.0, ',' + ECHO),                         # no sorriso
    (N + '2022-08-17 Approaching the Crash Site - Boom.wav', CLIP, 0.8, ',atrim=0:3'),
    (N + 'Laugh1.wav', CLIP + 0.55, 0.55, ',asetrate=48000*0.82,aresample=48000,' + ECHO),
    (R + 'laugh_tail.wav', CLIP + 2.3, 0.42, ',' + ECHO + ',afade=t=out:st=1.0:d=1.2'),
]
ain, af = [], []
for k, (p, st, vol, ex) in enumerate(A):
    ain += ['-i', p]
    af.append(f"[{4+k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol}{ex},adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
mix = ';'.join(af) + ';' + ''.join(f'[a{k}]' for k in range(len(A))) + \
      f"amix=inputs={len(A)}:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.2,atrim=0:{TOTAL}[aout]"

img = lambda p: ['-loop', '1', '-framerate', str(FPS), '-t', str(TOTAL), '-i', p]
run(['ffmpeg', '-v', 'error', '-y', '-i', S + '/in.mp4'] + img(O + 'end_logo.png') + img(O + 'end_title.png') +
    img(O + 'end_soon.png') + ain + ['-filter_complex', v + ';' + mix, '-map', '[vout]', '-map', '[aout]',
    '-t', str(TOTAL), '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-maxrate', '12M', '-bufsize', '24M',
    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', S + '/palhaco.mp4'])
print('ok', TOTAL)
