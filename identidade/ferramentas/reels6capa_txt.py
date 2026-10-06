P='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/latest/project/'
H=open(P+'MeioListaElas.dc.html').read(); pre=H[:H.index('<x-dc>')]; post=H[H.index('</x-dc>'):]
FONT='<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,900;1,9..144,400&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">'
EXTL=".extl{text-shadow:-2px 2px 0 #35535c,-4px 4px 0 #41646e,-6px 6px 0 #4f7580,-8px 8px 0 #5f8792,-10px 10px 0 #7199a4,-12px 12px 0 #85abb5,-14px 14px 0 #9bbdc6,-16px 16px 0 #b3cfd6,-18px 18px 0 #c3dbe1,-20px 20px 0 #cfe3e8}"
names=['Tom Keller','Maycon Beats','Possani','Mexikanno','Maka','Coiote']
FR="font-family: 'Fraunces', serif"
rows=''.join('<div style="display: flex; align-items: baseline; gap: 26px; padding: 16px 0; border-bottom: 2px solid #b3cfd6"><span style="font-size: 26px; font-weight: 700; letter-spacing: 0.14em; color: #4f7580">0%d</span><span style="%s; font-weight: 900; font-size: 64px; line-height: 1; color: #060a0c">%s</span></div>'%(i+1,FR,n) for i,n in enumerate(names))
body=f'''<div style="width: 1080px; height: 1920px; box-sizing: border-box; padding: 270px 80px 250px; display: flex; flex-direction: column; background: #e4f2f6; color: #060a0c; overflow: hidden">
<div style="display: flex; justify-content: space-between; font-size: 32px; letter-spacing: 0.14em; text-transform: uppercase; color: #2f4e56"><span>why not? · edição 01</span><span>09.10</span></div>
<div class="extl" style="margin: 120px 0 0 10px; {FR}; font-weight: 900; font-size: 196px; line-height: 0.86; color: #060a0c; transform: rotate(-6deg); transform-origin: left bottom; white-space: nowrap">line-up<br>completo.</div>
<div style="margin-top: 80px; {FR}; font-style: italic; font-size: 56px; color: #060a0c">6 DJs. uma noite só.</div>
<div style="margin-top: 40px; border-top: 3px solid #060a0c">{rows}</div>
<div style="margin-top: auto; display: flex; justify-content: space-between; padding-top: 22px; border-top: 2px solid #9bbdc6; font-size: 30px; letter-spacing: 0.08em; text-transform: uppercase; color: #2f4e56"><span style="white-space: nowrap">@ballyclub.oficial · 22h</span><span style="white-space: nowrap; color: #060a0c">Ingressos na bio →</span></div>
</div>'''
doc=pre.replace('<title>A lista VIP é delas</title>','<title>Reels 6 DJs · capa</title>')+f'''<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0;background:#e4f2f6;font-family:'Space Mono',monospace;color:#060a0c}}
{EXTL}
</style>
</helmet>
{body}
'''+post.replace('"height":1350','"height":1920')
open(P+'Reels6Capa.dc.html','w').write(doc); print('ok')
