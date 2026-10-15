"""Reels 'o anfitrião' (motosserra): clipe Higgsfield + legendas + voz Vlad + cartão final.
Uso: python3 edit_moto.py <voz.mp3>"""
import subprocess, os, sys
S = os.path.dirname(os.path.abspath(__file__))
N = '/mnt/user-data/uploads/Downloads/_claude_assets/snd/'
VOZ = sys.argv[1]
W, H, FPS = 1080, 1920, 30
CLIP = 14.85
END = 4.4
TOTAL = CLIP + END
run = lambda a: subprocess.run(a, check=True)

# voz: corta silêncio inicial, acelera 12% e aplica o eco aprovado; separa as 2 frases
run(['ffmpeg', '-v', 'error', '-y', '-i', VOZ, '-af',
     'silenceremove=start_periods=1:start_threshold=-45dB,atempo=1.12,aecho=0.85:0.6:160|330:0.22|0.11,lowpass=f=9500',
     '-ar', '48000', '-ac', '2', S + '/voz_fx.wav'])
out = subprocess.run(['ffmpeg', '-i', S + '/voz_fx.wav', '-af', 'silencedetect=n=-32dB:d=0.35', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
import re
sil = [(float(a), float(b)) for a, b in zip(re.findall(r'silence_start: ([\d.]+)', out), re.findall(r'silence_end: ([\d.]+)', out))]
# a pausa mais longa separa "ele já chegou... esperando por você" de "sexta-feira..."
mid = [p for p in sil if 3.5 < p[0] < 7.0]  # pausa entre 'por você' e 'sexta-feira'
cut = mid[0] if mid else (4.8, 5.4)
P1_END, P2_START = cut[0] + 0.25, cut[1] - 0.05
print('frase1 0-%.2f  frase2 %.2f-' % (P1_END, P2_START), sil)

GRADE = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
         "eq=brightness=-0.02:contrast=1.06:saturation=0.9,colorbalance=rs=.04:bs=-.05")
fadeov = lambda i, a, b: f"[{i}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b-0.3}:d=0.3:alpha=1[o{i}]"
v = (f"[0:v]trim=0:{CLIP},setpts=PTS-STARTPTS,{GRADE},tpad=stop_mode=add:stop_duration={END}:color=0x0b0706,"
     f"vignette=angle=PI/4.3,noise=alls=8:allf=t,format=yuv420p,fade=t=in:st=0:d=0.4[bg];"
     + fadeov(1, 0.7, 2.75) + ';' + fadeov(2, 2.8, 5.75) + ';' + fadeov(3, 11.9, CLIP + 0.05) + ';'
     f"[4:v]format=rgba,fade=t=in:st={CLIP+0.2}:d=0.8:alpha=1[lg];[5:v]format=rgba,fade=t=in:st={CLIP+0.9}:d=0.7:alpha=1[ti];"
     f"[6:v]format=rgba,fade=t=in:st={CLIP+1.6}:d=0.6:alpha=1[da];"
     "[bg][o1]overlay[a];[a][o2]overlay[b];[b][o3]overlay[c];"
     f"[c][lg]overlay=enable='gte(t,{CLIP})'[d];[d][ti]overlay=enable='gte(t,{CLIP})'[e];[e][da]overlay=enable='gte(t,{CLIP})',format=yuv420p[vout]")

# áudio: som original do clipe (motosserra) + drone + voz (frase 1 no começo, frase 2 sobre o cartão) + impacto grave
A_in = ['-i', S + '/voz_fx.wav', '-i', N + '2022-04-23 Occult Blood - Spooky Times.wav',
        '-i', N + '2022-08-17 Approaching the Crash Site - Boom.wav']
a = (f"[0:a]atrim=0:{CLIP},asetpts=PTS-STARTPTS,volume='if(lt(t,11.7),1.5,0.75)':eval=frame,afade=t=out:st={CLIP-0.08}:d=0.08,apad=pad_dur={END}[sfx];"
     "[7:a]asplit[va][vb];"
     f"[va]atrim=0:{P1_END},asetpts=PTS-STARTPTS,afade=t=out:st={P1_END-0.15}:d=0.15,adelay=800|800[v1];"
     f"[vb]atrim={P2_START},asetpts=PTS-STARTPTS,volume=1.25,adelay=12000|12000[v2];"
     f"[8:a]volume=0.4,afade=t=out:st={TOTAL-1.3}:d=1.3[dr];"
     f"[9:a]atrim=0:3.5,lowpass=f=170,lowpass=f=170,volume=1.6,adelay={int(CLIP*1000)}|{int(CLIP*1000)}[bm];"
     "[sfx][v1][v2][dr][bm]amix=inputs=5:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.2,"
     f"atrim=0:{TOTAL}[aout]")
img = lambda p: ['-loop', '1', '-framerate', str(FPS), '-t', str(TOTAL), '-i', S + '/' + p]
run(['ffmpeg', '-v', 'error', '-y', '-i', S + '/in.mp4'] + img('t1.png') + img('t2.png') + img('t3.png') +
    img('e_logo.png') + img('e_title.png') + img('e_date.png') + A_in +
    ['-filter_complex', v + ';' + a, '-map', '[vout]', '-map', '[aout]', '-t', str(TOTAL),
     '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p',
     '-r', str(FPS), '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', S + '/motosserra_final.mp4'])
print('ok', TOTAL)
