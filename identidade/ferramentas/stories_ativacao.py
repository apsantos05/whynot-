"""Stories de movimentação (quinta, por que não? + afterzin). Espaço livre reservado pros stickers do Instagram. 1080x1920 @2x."""
import os, base64, random, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
OUT = R + '/stories-ativacao'; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

PAL = {
  'q': dict(base='#09080c', dest='#ece6f4', med='#b1a6c4', line='#3a3348', glow='#261f33', mid='#130f1a',
            logo=R + '/assets/logo/lavanda/logo-why-not-lavanda.png', tag='QUINTA, POR QUE NÃO? · BALLY CLUB'),
  'a': dict(base='#08090a', dest='#ececec', med='#a9adb1', line='#2c2f33', glow='#1f2225', mid='#111315',
            logo=R + '/assets/logo/grafite/logo-why-not-grafite.png', tag='AFTERZIN · 20.11 · 01H · BALLY CLUB'),
}

def css(p):
    return f"""
@font-face{{font-family:FrV;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-normal.woff2')})}}
@font-face{{font-family:Fr;font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FD+'/fv/files/fraunces-latin-full-italic.woff2')})}}
@font-face{{font-family:SM;font-weight:700;src:url(data:font/woff2;base64,{b64(FD+'/fontsource-space-mono/files/space-mono-latin-700-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:{p['base']};overflow:hidden;position:relative}}
.c{{position:absolute;left:80px;right:80px;text-align:center}}
.fr{{font-family:Fr;font-style:italic;color:{p['dest']}}}
.sm{{font-family:SM;font-weight:700;color:{p['med']};letter-spacing:.3em;text-indent:.3em}}
.bk{{font-family:FrV;font-weight:900;font-variation-settings:'opsz' 144;color:{p['dest']};line-height:.98;letter-spacing:-.015em}}
.md{{color:{p['med']}}}
.rule{{position:absolute;left:50%;height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,{p['med']},transparent);opacity:.55}}
"""

def frame(p, body, gy=760):
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% {gy}px,{p['glow']} 0,{p['mid']} 430px,{p['base']} 900px)'></div>"
            f"<img src='data:image/png;base64,{b64(p['logo'])}' style='position:absolute;left:50%;top:250px;width:220px;transform:translateX(-50%)'>"
            + body +
            f"<div class='c sm' style='top:1560px;font-size:18px'>{p['tag']}</div>")

STORIES = [
 # (arquivo, paleta, html, onde vai o sticker)
 ('q1_contagem-estreia', 'q', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>FALTAM POUCOS DIAS</div>
<div class='c bk' style='top:540px;font-size:150px'>quinta,</div>
<div class='c fr' style='top:700px;font-size:96px'>por que não?</div>
<div class='c fr md' style='top:860px;font-size:44px'>estreia 12.11 · coquetel às 21h</div>
<div class='c fr' style='top:1380px;font-size:40px'>ativa o lembrete ↑</div>""", 'Sticker CONTAGEM REGRESSIVA ("quinta, por que não?" · 12/11 · 21h) no espaço vazio entre 960 e 1340px.'),

 ('q2_enquete-quinta', 'q', """
<div class='c bk' style='top:520px;font-size:120px'>quinta é<br>dia de sair?</div>
<div class='c fr md' style='top:820px;font-size:46px'>responde aí embaixo ↓</div>
<div class='c sm' style='top:1400px;font-size:22px;color:VAR_DEST'>12.11 · A GENTE TE ESPERA</div>""", 'Sticker ENQUETE: "óbvio que sim" / "agora é" — entre 920 e 1360px.'),

 ('q3_marca-a-amiga', 'q', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>LISTA VIP PARA ELAS</div>
<div class='c bk' style='top:540px;font-size:122px'>marca a<br>amiga que<br>vai com você.</div>
<div class='c fr md' style='top:960px;font-size:46px'>nome na lista só pelo grupo.<br>link na bio.</div>""", 'Sticker MENÇÃO ou LINK (grupo VIP) entre 1120 e 1460px.'),

 ('q4_open-gin', 'q', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>TODA QUINTA</div>
<div class='c bk' style='top:550px;font-size:170px'>open<br>gin.</div>
<div class='c sm' style='top:930px;font-size:40px;color:VAR_DEST'>22H ÀS 23H</div>
<div class='c fr md' style='top:1010px;font-size:52px'>quem chega cedo, brinda.</div>
<div class='c fr' style='top:1300px;font-size:40px'>quinta, por que não? · 12.11</div>""", 'Sem sticker (ou link da lista entre 1100 e 1280px).'),

 ('q5_caixinha-musica', 'q', """
<div class='c bk' style='top:520px;font-size:112px'>qual música<br>não pode faltar<br>na quinta?</div>
<div class='c fr md' style='top:930px;font-size:44px'>a gente passa pro DJ.</div>""", 'Sticker CAIXINHA DE PERGUNTAS entre 1030 e 1460px.'),

 ('a1_contagem-afterzin', 'a', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>ACABOU O VINTAGE CULTURE?</div>
<div class='c bk' style='top:540px;font-size:170px'>afterzin.</div>
<div class='c fr md' style='top:740px;font-size:52px'>a noite continua às 01h.</div>
<div class='c fr' style='top:1380px;font-size:40px'>ativa o lembrete ↑</div>""", 'Sticker CONTAGEM REGRESSIVA ("afterzin why not?" · 20/11 · 01h) entre 860 e 1340px.'),

 ('a2_enquete-vai-nos-dois', 'a', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>SEXTA · 20.11</div>
<div class='c bk' style='top:540px;font-size:118px'>vai no show<br>e depois?</div>
<div class='c fr md' style='top:830px;font-size:46px'>o after é na Bally, a partir da 01h.</div>""", 'Sticker ENQUETE: "vou nos dois" / "só no after" — entre 940 e 1360px.'),

 ('a3_qual-dj', 'a', """
<div class='c sm' style='top:470px;font-size:24px;color:VAR_DEST'>LINE-UP DO AFTERZIN</div>
<div class='c bk' style='top:540px;font-size:112px'>quem você<br>mais quer ver?</div>
<div class='c fr md' style='top:820px;font-size:44px'>Mexikanno · Kaio Alves · Coiote<br>ALOIRA · Maka</div>""", 'Sticker TESTE/QUIZ com os 5 nomes (ou enquete com 4 opções) entre 960 e 1460px.'),
]

guia = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for nome, k, body, sticker in STORIES:
        p = PAL[k]; body = body.replace('VAR_DEST', p['dest'])
        pg = br.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=2)
        pg.set_content(f"<style>{css(p)}</style>{frame(p, body)}")
        pg.evaluate('document.fonts.ready.then(()=>0)'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{OUT}/_t.png'); pg.close()
        im = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
        random.seed(11); n = Image.effect_noise(im.size, 24).convert('RGB')
        Image.blend(im, ImageChops.overlay(im, n), .14).save(f'{OUT}/{nome}.png'); print(nome)
        guia.append(f'{nome}.png — {sticker}')
    br.close()
open(OUT + '/GUIA-STICKERS.txt', 'w').write('\n'.join(guia) + '\n')
