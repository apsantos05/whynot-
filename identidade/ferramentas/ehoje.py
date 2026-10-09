P='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/latest/project/'
H=open(P+'MeioListaElas.dc.html').read(); pre=H[:H.index('<x-dc>')]; post=H[H.index('</x-dc>'):]
FONT='<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,900;1,9..144,400&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">'
EXT=".ext{text-shadow:-2px 2px 0 #b3cfd6,-4px 4px 0 #9bbdc6,-6px 6px 0 #85abb5,-8px 8px 0 #7199a4,-10px 10px 0 #5f8792,-12px 12px 0 #4f7580,-14px 14px 0 #41646e,-16px 16px 0 #35535c,-18px 18px 0 #2a434b,-20px 20px 0 #20343a,-22px 22px 0 #17262b,-24px 24px 0 #0f191d} .extm{text-shadow:-1.5px 1.5px 0 #b3cfd6,-3px 3px 0 #9bbdc6,-4.5px 4.5px 0 #85abb5,-6px 6px 0 #7199a4,-7.5px 7.5px 0 #5f8792,-9px 9px 0 #4f7580,-10.5px 10.5px 0 #41646e,-12px 12px 0 #35535c,-13.5px 13.5px 0 #2a434b,-15px 15px 0 #20343a,-16.5px 16.5px 0 #17262b,-18px 18px 0 #0f191d}"
FR="font-family: 'Fraunces', serif"
BG="background: radial-gradient(ellipse at 50% 38%, #12302e 0%, #0a1315 46%, #060a0c 80%)"
def info(fs=30):
    return f'''<div style="font-size: {fs}px; font-weight: 700; letter-spacing: 0.1em; line-height: 1.7; color: #e4f2f6">BALLY CLUB · 22H<br>OPEN GIN DAS 22H ÀS 23H</div>
<div style="margin-top: 18px; font-size: {fs-6}px; letter-spacing: 0.08em; line-height: 1.6; color: #9dbcc4">COIOTE · MAKA · TOM KELLER<br>MAYCON BEATS · MEXIKANNO · POSSANI</div>'''
def page(title,h,body):
    return pre.replace('<title>A lista VIP é delas</title>',f'<title>{title}</title>')+f'''<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0;background:#060a0c;font-family:'Space Mono',monospace;color:#e4f2f6}}
{EXT}
</style>
</helmet>
{body}
'''+post.replace('"height":1350',f'"height":{h}')
feed=f'''<div style="width: 1080px; height: 1350px; box-sizing: border-box; padding: 80px; display: flex; flex-direction: column; {BG}; color: #e4f2f6; overflow: hidden">
<div style="display: flex; justify-content: space-between; font-size: 30px; letter-spacing: 0.14em; text-transform: uppercase; color: #9dbcc4"><span>Sexta · 09.10</span><span>Edição 01</span></div>
<div class="ext" style="margin: 110px 0 0 20px; {FR}; font-weight: 900; font-size: 250px; line-height: 0.86; transform: rotate(-8deg); transform-origin: left center; white-space: nowrap">é hoje.</div>
<div style="margin-top: 110px; {FR}; font-style: italic; font-size: 64px; line-height: 1.1">preparados?</div>
<div class="extm" style="margin: 26px 0 0 8px; {FR}; font-weight: 900; font-size: 92px; line-height: 0.9; transform: rotate(-6deg); transform-origin: left center; white-space: nowrap">why not?</div>
<div style="margin-top: auto">{info(30)}</div>
<div style="margin-top: 30px; display: flex; justify-content: space-between; padding-top: 22px; border-top: 2px solid #35535c; font-size: 28px; letter-spacing: 0.08em; text-transform: uppercase; color: #9dbcc4"><span style="white-space: nowrap">@ballyclub.oficial</span><span style="white-space: nowrap; color: #e4f2f6">Ingressos na bio →</span></div>
</div>'''
story=f'''<div style="width: 1080px; height: 1920px; box-sizing: border-box; padding: 260px 90px 250px; display: flex; flex-direction: column; {BG}; color: #e4f2f6; overflow: hidden">
<div style="display: flex; justify-content: space-between; font-size: 30px; letter-spacing: 0.14em; text-transform: uppercase; color: #9dbcc4"><span>Sexta · 09.10</span><span>Edição 01</span></div>
<div class="ext" style="margin: 120px 0 0 20px; {FR}; font-weight: 900; font-size: 250px; line-height: 0.86; transform: rotate(-8deg); transform-origin: left center; white-space: nowrap">é hoje.</div>
<div style="margin-top: 120px; {FR}; font-style: italic; font-size: 66px; line-height: 1.1">preparados?</div>
<div class="extm" style="margin: 28px 0 0 8px; {FR}; font-weight: 900; font-size: 96px; line-height: 0.9; transform: rotate(-6deg); transform-origin: left center; white-space: nowrap">why not?</div>
<div style="margin-top: 90px">{info(30)}</div>
<div style="margin-top: 22px; font-size: 24px; letter-spacing: 0.2em; color: #9dbcc4">AV. DR. ALBERTO ANDALÓ, 3837</div>
<div style="margin-top: auto; text-align: center; font-size: 28px; font-weight: 700; letter-spacing: 0.3em; color: #e4f2f6">INGRESSOS NO LINK ↓</div>
<div style="height: 170px"></div>
</div>'''
open(P+'EHojeFeed.dc.html','w').write(page('É hoje · feed',1350,feed))
open(P+'EHojeStory.dc.html','w').write(page('É hoje · story',1920,story))
print('ok')
