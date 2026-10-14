"""Monta o reels Halloween 'no one leaves.' a partir dos clipes Higgsfield.
Uso: python3 edit.py  (gera reel_final.mp4 na mesma pasta)"""
import subprocess, os
S = os.path.dirname(os.path.abspath(__file__))
D = '/mnt/user-data/uploads/Downloads/'
SND = D + '_claude_assets/snd/'
R = os.path.join(S, '..', 'reel') + '/'
C = {1: D + 'A-single-candle-in-an-antique-candlestic.mp4', 2: D + 'The-old-ornate-door-slowly-creaks-open-b.mp4',
     3: D + 'The-clown-stands-perfectly-still-in-the.mp4', 4: D + 'The-woman-stands-still-among-tall-lit-ca.mp4',
     5: D + 'Top-down-view-the-camera-slowly-rotates.mp4', 6: D + 'Close-up-of-the-candle-The-flame-flicke.mp4'}
W, H, FPS = 1080, 1920, 30
run = lambda a: subprocess.run(a, check=True)

GRADE = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=%d,setsar=1,"
         "eq=brightness=-0.035:contrast=1.08:saturation=0.86,"
         "colorbalance=rs=.05:gs=.01:bs=-.06:rm=.04:bm=-.04" % (W, H, W, H, FPS))

# (tipo, fonte, inicio_na_fonte, duracao, extra_filtro)
seq = [
    ('c', 1, 0.50, 2.20, ''),
    ('c', 2, 1.80, 1.70, ''),
    ('w', 0, 0, 0.08, ''), ('k', 0, 0, 0.06, ''),
    ('c', 4, 2.80, 1.55, ''),
    ('k', 0, 0, 0.10, ''),
    ('c', 5, 1.00, 1.20, ''),
    ('c', 3, 2.60, 1.50, ''),
    ('k', 0, 0, 0.08, ''),
    ('c', 3, 4.20, 0.52, ',eq=brightness=0.06:contrast=1.25'),
    ('c', 6, 1.25, 0.55, ''),
    ('w', 0, 0, 0.05, ''),
    ('c', 6, 3.55, 1.45, ''),
    ('k', 0, 0, 0.60, ''),
    ('k', 0, 0, 4.76, ''),  # fundo do cartão final
]
os.makedirs(S + '/seg', exist_ok=True)
lst = []
for n, (t, src, ss, d, ex) in enumerate(seq):
    out = f'{S}/seg/{n:02d}.mp4'
    if t == 'c':
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(d), '-i', C[src], '-vf', GRADE + ex,
             '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    else:
        col = '#efe4d0' if t == 'w' else '#0b0706'
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c={col}:s={W}x{H}:r={FPS}:d={d}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    lst.append(out)
open(S + '/seg/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in lst))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', S + '/seg/list.txt', '-c', 'copy', S + '/base.mp4'])

# tempos (cumulativos) para textos e sons
t = 0; marks = []
for s in seq: marks.append(t); t += s[3]
TOTAL = t
END = marks[-1]
print('total', round(TOTAL, 2), 'cartao final em', round(END, 2))

fade = lambda a, b, fi=0.25, fo=0.25: (f"format=rgba,fade=t=in:st={a}:d={fi}:alpha=1,fade=t=out:st={b-fo}:d={fo}:alpha=1")
vf = (
    f"[0:v]format=yuv420p[v0];"
    f"[1:v]{fade(5.00, 6.62)}[q];[2:v]{fade(6.75, 8.39, .15, .08)}[f];"
    f"[3:v]format=rgba,fade=t=in:st={END+0.25}:d=0.9:alpha=1[lg];"
    f"[4:v]format=rgba,fade=t=in:st={END+1.15}:d=0.8:alpha=1[ti];"
    f"[5:v]format=rgba,fade=t=in:st={END+2.0}:d=0.6:alpha=1[so];"
    f"[v0][q]overlay=enable='between(t,5.0,6.62)'[a];[a][f]overlay=enable='between(t,6.75,8.39)'[b];"
    f"[b][lg]overlay=enable='gte(t,{END})'[c];[c][ti]overlay=enable='gte(t,{END})'[d];[d][so]overlay=enable='gte(t,{END})'[e];"
    f"[e]vignette=angle=PI/4.2,noise=alls=9:allf=t,format=yuv420p,fade=t=in:st=0:d=0.5[vout]"
)
img = lambda p: ['-loop', '1', '-t', str(TOTAL), '-i', p]

# ---- audio ----
V0 = 0.60
A = [  # (arquivo, inicio, volume, inicio_na_fonte, duracao)
    (SND + '2022-04-23 Occult Blood - Spooky Times.wav', 0.0, 0.55, 0, TOTAL),
    (S + '/voz_fx2.wav', V0, 1.0, 0, 9),
    (R + 'creak.wav', 2.15, 0.55, 0, 2.0),
    (SND + '2022-08-17 Approaching the Crash Site - Boom.wav', marks[2], 0.75, 0, 2.5),
    (SND + '2022-08-17 Approaching the Crash Site - Boom.wav', marks[5], 0.45, 0, 1.6),
    (R + 'laugh_deep.wav', 7.85, 0.85, 0, 2.6),
    (SND + '2022-04-16 Triple-C THICCC - Heavy Breathing.wav', marks[10] - 0.3, 0.35, 0, 0.9),
    (R + 'blow.wav', marks[11] - 0.12, 1.0, 0, 1.5),
    (SND + '2023-02-15 Dancing in the Shallows - Reverse Cymbals.wav', None, 0.6, 0, None),
    (SND + '2022-08-17 Approaching the Crash Site - Boom.wav', END, 0.9, 0, 3.5),
    (R + 'laugh_tail.wav', END + 2.2, 0.45, 0, 2.5),
]
def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)
ain, af = [], []
for k, (p, st, vol, ss, d) in enumerate(A):
    if st is None:  # riser termina no cartão final
        d = min(dur(p), 2.6); ss = max(0, dur(p) - d); st = END - d
    ain += ['-ss', str(ss), '-t', str(d), '-i', p]
    idx = 6 + k
    extra = ',afade=t=out:st=%f:d=1.4' % (TOTAL - 1.6) if k == 0 else ''
    af.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol}{extra},adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
mix = ';'.join(af) + ';' + ''.join(f'[a{k}]' for k in range(len(A))) + \
      f"amix=inputs={len(A)}:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.2,atrim=0:{TOTAL}[aout]"

cmd = ['ffmpeg', '-v', 'error', '-y', '-i', S + '/base.mp4'] + img(S + '/tx_quem.png') + img(S + '/tx_fica.png') + \
      img(S + '/end_logo.png') + img(S + '/end_title.png') + img(S + '/end_soon.png') + ain + \
      ['-filter_complex', vf + ';' + mix, '-map', '[vout]', '-map', '[aout]', '-t', str(TOTAL),
       '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(FPS),
       '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', S + '/reel_final.mp4']
run(cmd)
print('ok', S + '/reel_final.mp4')
