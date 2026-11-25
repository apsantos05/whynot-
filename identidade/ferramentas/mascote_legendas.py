"""Legendas e tela final do Reel do mascote (quinta 26.11, ressaca das provas).
Gera PNGs transparentes 1080x1920 (uma por frase) + tela final, e o roteiro de tempos (tempos.json).
Uso: python3 mascote_legendas.py <pasta fontes> <pasta saída>"""
import os, sys, json, base64
from playwright.sync_api import sync_playwright

FD, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
W, H = 1080, 1920
# (início, fim, texto) em segundos, a partir da transcrição com tempo por palavra
FRASES = [(0.0, 1.06, 'e aí, galera!'), (1.06, 3.3, 'sou eu, o mascote<br>da <b>why not?</b>'), (3.3, 4.58, 'acabaram as provas?'),
          (4.58, 7.2, 'então amanhã é<br><b>ressaca das provas!</b>'), (7.2, 9.08, 'quinta, com a Baruc,<br>lá na Bally,'),
          (9.08, 10.85, 'a partir das 22h.'), (10.85, 12.3, 'Mexikanno, Camuri,'), (12.3, 15.05, 'Maycon Beats, Jhonatan Soares<br>e Possani.'),
          (15.05, 16.34, '<b>lista vip</b> no link.'), (16.34, 17.8, 'vai ficar em casa?'), (17.8, 20.0, 'por que não<br>vir pra <b>why not?</b>')]
CSS = f"""@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:FrR;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;overflow:hidden}}
.l{{position:absolute;left:0;right:0;top:1450px;text-align:center;font-family:Fr;font-style:italic;font-weight:480;font-size:70px;line-height:1.08;color:#f6f1fb;
   letter-spacing:-.01em;font-variation-settings:"WONK" 0;text-shadow:0 3px 0 rgba(20,8,40,.55),0 0 34px rgba(20,8,40,.9),0 0 10px rgba(20,8,40,.8)}}
.l b{{font-weight:560;color:#cdb8ff}}"""
FIM = (f"<div style='position:absolute;inset:0;background:#0a0810'></div>"
       f"<img src='data:image/png;base64,{b64(R + '/assets/logo/lavanda/logo-why-not-lavanda.png')}' style='position:absolute;left:50%;transform:translateX(-50%);top:560px;width:420px'>"
       f"<img src='data:image/png;base64,{b64(R + '/quintas-bally/semanas/2026-11-26/logo_baruc.png')}' style='position:absolute;left:50%;transform:translateX(-50%);top:760px;width:190px'>"
       "<div style='position:absolute;left:0;right:0;top:1000px;text-align:center;font-family:Fr;font-style:italic;font-weight:440;font-size:104px;color:#f3eef8;line-height:1'>ressaca<br>das provas.</div>"
       "<div style='position:absolute;left:0;right:0;top:1250px;text-align:center;font-family:FrR;font-size:34px;color:#cdb8ff;font-variation-settings:\"opsz\" 14'>quinta, 26.11, na Bally Club, a partir das 22h.</div>"
       "<div style='position:absolute;left:0;right:0;top:1310px;text-align:center;font-family:FrR;font-size:34px;color:#f3eef8;font-variation-settings:\"opsz\" 14'>lista vip no link.</div>")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H}); tempos = []
    for i, (a, b, t) in enumerate(FRASES):
        pg.set_content(f"<style>{CSS}</style><div class='l'>{t}</div>"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(150)
        f = f'{OUT}/leg_{i:02d}.png'; pg.screenshot(path=f, omit_background=True); tempos.append([a, b, f])
    pg.set_content(f"<style>{CSS}</style>{FIM}"); pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(250)
    pg.screenshot(path=f'{OUT}/tela_final.png'); br.close()
json.dump(tempos, open(f'{OUT}/tempos.json', 'w')); print(len(tempos), 'legendas + tela final')
