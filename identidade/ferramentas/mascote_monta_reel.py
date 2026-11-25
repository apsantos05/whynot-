"""Monta o Reel do mascote: vídeo do ElevenLabs (OmniHuman) + legendas por frase + tela final de 2,5 s.
Uso: python3 mascote_monta_reel.py <video_mascote.mp4> <pasta legendas (tempos.json, tela_final.png)> <saida.mp4>"""
import sys, json, subprocess
VID, LEG, OUT = sys.argv[1:4]
tempos = json.load(open(f'{LEG}/tempos.json'))
ins = ['-i', VID] + sum([['-i', f] for _, _, f in tempos], [])
# normaliza para 1080x1920 30fps, cola cada legenda no seu intervalo
f = '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p[v0];'
ult = 'v0'
for i, (a, b, _) in enumerate(tempos):
    f += f"[{ult}][{i+1}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i+1}];"; ult = f'v{i+1}'
f = f.rstrip(';')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', f, '-map', f'[{ult}]', '-map', '0:a', '-c:v', 'libx264', '-crf', '18',
                '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', '-shortest', '/tmp/_corpo.mp4'], check=True)
# tela final com fade e silêncio, depois concatena
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-t', '2.5', '-i', f'{LEG}/tela_final.png', '-f', 'lavfi', '-t', '2.5', '-i', 'anullsrc=r=44100:cl=stereo',
                '-vf', 'scale=1080:1920,fps=30,setsar=1,format=yuv420p,fade=t=in:st=0:d=0.35', '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', '/tmp/_fim.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '/tmp/_corpo.mp4', '-i', '/tmp/_fim.mp4', '-filter_complex',
                '[0:v]setsar=1[x];[1:v]setsar=1[y];[x][0:a][y][1:a]concat=n=2:v=1:a=1[v][a]', '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', OUT], check=True)
print(OUT)
