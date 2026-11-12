"""Intro 10s da logo why not? em vidro (takes gerados no Higgsfield/Kling 3.0 + SFX Mirelo).
Monta: slogan -> cacos montam a logo (take1 invertido) -> segura -> explode (take2).
Saídas: 16:9 com som, 9:16 com som, loop 16:9 sem slogan e sem som.
Uso: python3 intro_logo_vidro.py <pasta fontes>"""
import os, sys, base64, subprocess
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
D = R + '/intro-logo-vidro'; F = D + '/fontes'; A = D + '/assets'
SLOGAN = 'toda noite começa com uma pergunta.'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

# ---------- slogan (PNG transparente, Fraunces itálico, paleta lavanda) ----------
CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
*{{margin:0;padding:0}} body{{background:transparent;display:flex;align-items:center;justify-content:center;text-align:center}}
div{{font-family:Fr;font-style:italic;font-weight:480;color:#ece6f4;line-height:1.18;letter-spacing:.005em;
text-shadow:0 0 34px rgba(177,166,196,.55),0 0 90px rgba(120,96,170,.45)}}"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for name, W, H, fs, txt in [('slogan_16x9', 1920, 1080, 88, SLOGAN),
                                ('slogan_9x16', 1080, 1920, 92, 'toda noite começa<br>com uma pergunta.')]:
        pg = br.new_page(viewport={'width': W, 'height': H})
        pg.set_content(f"<style>{CSS}body{{width:{W}px;height:{H}px}}div{{font-size:{fs}px}}</style><div>{txt}</div>")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{A}/{name}.png', omit_background=True); pg.close()
    br.close()

# ---------- linha do tempo (s) ----------
LEAD = 1.3                      # preto + slogan antes dos cacos
A_D, B_D, C_D = 2.4167/1.5, 1.9167, 1.7083/1.25
LOCK = LEAD + A_D + B_D         # logo montada
T2 = LOCK + C_D                 # entra o take2
SP2 = 6.0417 / (10 - T2)        # acelera o take2 pra fechar em 10s
FLASH = T2 + 0.5 / SP2
print(f'lock {LOCK:.2f}s · take2 {T2:.2f}s · flash {FLASH:.2f}s · speed2 {SP2:.3f}')

PREP = 'scale=1936:1080:flags=lanczos,crop=1920:1080,setsar=1'
def video_chain(lead, total):
    lock, t2 = lead + A_D + B_D, lead + A_D + B_D + C_D
    return (f"[0:v]{PREP},reverse,split=3[r1][r2][r3];"
            f"[r1]trim=0:2.4167,setpts=(PTS-STARTPTS)/1.5[a];"
            f"[r2]trim=2.4167:4.3333,setpts=PTS-STARTPTS[b];"
            f"[r3]trim=4.3333:6.0417,setpts=(PTS-STARTPTS)/1.25[c];"
            f"[1:v]{PREP},setpts=PTS/{SP2:.4f}[d];"
            + (f"color=c=black:s=1920x1080:r=24:d={lead}[k];[k][a][b][c][d]concat=n=5:v=1:a=0" if lead else "[a][b][c][d]concat=n=4:v=1:a=0")
            + f",fps=24,trim=0:{total},setpts=PTS-STARTPTS,"
            f"eq=brightness='0.10*exp(-7*(t-{lock:.3f}))*gte(t,{lock:.3f})':eval=frame,"   # brilho quando a logo trava
            f"fade=t=in:st={lead}:d=0.5,fade=t=out:st={total-0.4:.2f}:d=0.4,"
            f"noise=alls=4:allf=t,format=yuv420p[base]")

def audio_chain(n0):
    # entradas n0..n0+3 = drone, montagem, impacto, explosao ; + 2 graves sintetizados
    d = lambda t: int(max(0, t) * 1000)
    return (f"[{n0}:a]asplit=2[d0][d1];"
            f"[d0]afade=t=in:d=0.4,afade=t=out:st=3.2:d=0.8,volume=0.75,adelay={d(0)}:all=1[s0];"
            # mesma textura grave subindo até a logo travar (tensão), corta seco no impacto
            f"[d1]atrim=0.6:2.9,asetpts=PTS-STARTPTS,afade=t=in:d=0.6,volume='min(1.1,0.3+0.4*t)':eval=frame,afade=t=out:st=2.2:d=0.1,adelay={d(LOCK-2.3)}:all=1[s4];"
            f"[{n0+1}:a]volume=3.0,adelay={d(LOCK-3.25)}:all=1[s1];"
            f"[{n0+2}:a]atrim=start=0.35,asetpts=PTS-STARTPTS,volume=1.0,adelay={d(LOCK-0.05)}:all=1[s2];"
            f"[{n0+3}:a]atrim=start=0.8,asetpts=PTS-STARTPTS,volume=1.3,afade=t=out:st=2.8:d=0.45,adelay={d(FLASH-0.1)}:all=1[s3];"
            f"sine=f=46:d=1.6,volume='1.0*exp(-3.2*t)':eval=frame,adelay={d(LOCK)}:all=1[b1];"
            f"sine=f=40:d=2.0,volume='1.2*exp(-2.4*t)':eval=frame,adelay={d(FLASH)}:all=1[b2];"
            f"[s0][s1][s2][s3][s4][b1][b2]amix=inputs=7:normalize=0:duration=longest,"
            f"aformat=sample_rates=48000:channel_layouts=stereo,alimiter=limit=0.9,atrim=0:10,apad=whole_dur=10,afade=t=out:st=9.55:d=0.45[mix]")

IN = ['-i', F + '/take1_desmorona.mp4', '-i', F + '/take2_explosao.mp4']
SFX = sum([['-i', f'{F}/sfx{k}.mp3'] for k in ['0-drone', '1-montagem', '2-impacto', '3-explosao']], [])
ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-maxrate', '16M', '-bufsize', '32M', '-pix_fmt', 'yuv420p', '-r', '24', '-movflags', '+faststart']
AENC = ['-c:a', 'aac', '-b:a', '256k']
run = lambda a: subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
SLG = "format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1,fade=t=out:st=2.0:d=0.5:alpha=1"

# 1) 16:9 com slogan e som
run(IN + ['-loop', '1', '-t', '2.6', '-r', '24', '-i', A + '/slogan_16x9.png'] + SFX + ['-filter_complex',
    video_chain(LEAD, 10) + f";[2:v]{SLG}[sl];[base][sl]overlay=0:0:eof_action=pass[v];" + audio_chain(3),
    '-map', '[v]', '-map', '[mix]', '-t', '10'] + ENC + AENC + [D + '/whynot-intro_16x9.mp4'])

# 2) 9:16: vídeo no meio sobre preto, bordas esfumadas + slogan em 2 linhas
run(IN + ['-loop', '1', '-t', '2.6', '-r', '24', '-i', A + '/slogan_9x16.png'] + SFX + ['-filter_complex',
    video_chain(LEAD, 10) + ";color=c=black:s=1080x1920:r=24:d=10[bg];"
    "[base]scale=1216:684:flags=lanczos,crop=1080:684,format=rgba,"
    "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/70,(H-1-Y)/150))'[fg];"
    f"[bg][fg]overlay=0:618[c];[2:v]{SLG}[sl];[c][sl]overlay=0:0:eof_action=pass,format=yuv420p[v];" + audio_chain(3),
    '-map', '[v]', '-map', '[mix]', '-t', '10'] + ENC + AENC + [D + '/whynot-intro_9x16.mp4'])

# 3) loop 16:9: só a logo (monta, segura, explode), sem slogan e sem som, começa e termina no preto
TL = A_D + B_D + C_D + 6.0417 / SP2
run(IN + ['-filter_complex', video_chain(0, round(TL - 0.05, 2)).replace('[base]', '[v]'), '-map', '[v]', '-an'] + ENC + [D + '/whynot-intro_loop_16x9_sem-som.mp4'])
print('ok')
