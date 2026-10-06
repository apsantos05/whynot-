exec(open('/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/flyer2.py').read().split("def cluster")[0])
EXTL=".extl{text-shadow:-2px 2px 0 #35535c,-4px 4px 0 #41646e,-6px 6px 0 #4f7580,-8px 8px 0 #5f8792,-10px 10px 0 #7199a4,-12px 12px 0 #85abb5,-14px 14px 0 #9bbdc6,-16px 16px 0 #b3cfd6,-18px 18px 0 #c3dbe1,-20px 20px 0 #cfe3e8}"
def pl(k,cx,top,h,z):
    w=int(h*ASP[k]); return f'<img src="{B[k]}" alt="" style="position: absolute; left: {int(cx-w/2)}px; top: {top}px; height: {h}px; z-index: {z}; filter: grayscale(1) contrast(1.08) brightness(1.18); mix-blend-mode: multiply">'
DJS=[('01','Tom Keller','61fe9268be9546536f564e16c5ca8035','50% 0%'),('02','Maycon Beats','939bd0cc3dc170954d571757c9e7f137','50% 12%'),('03','Possani','ca5eb7e955a13eaf60912a65816cce1e','50% 0%'),('04','Mexikanno','e1675d9aa871be3e2ad4e98de756f702','50% 6%'),('05','Maka','a923d0a4dc3b7e15971ef2f755b0af33','50% 0%'),('06','Coiote','80b0c6439f917b90c14fc6392e85bb1a','50% 0%')]
def cell(n,name,b,pos): return f'''<div style="position: relative">
<div style="position: relative; height: 330px; overflow: hidden"><img src="/_blob/{b}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; filter: grayscale(1) brightness(1.26) contrast(1.12); mix-blend-mode: multiply">
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 110px; background: linear-gradient(to top, #e4f2f6 10%, rgba(228,242,246,0))"></div></div>
<div style="margin-top: -18px; position: relative; font-size: 22px; font-weight: 700; letter-spacing: 0.14em; color: #2f4e56">{n}</div>
<div style="margin-top: 6px; font-family: 'Fraunces', serif; font-weight: 900; font-size: 38px; line-height: 1; color: #060a0c; white-space: nowrap">{name}</div></div>'''
cl='<div style="position: absolute; left: 80px; right: 80px; top: 370px; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 24px; row-gap: 44px">'+''.join(cell(*d) for d in DJS)+'</div>'
body=f'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #e4f2f6; color: #060a0c">
<div style="position: absolute; left: 80px; right: 80px; top: 270px; display: flex; justify-content: space-between; font-size: 32px; letter-spacing: 0.14em; text-transform: uppercase; color: #2f4e56"><span>Line-up completo</span><span>09.10</span></div>
{cl}
<div style="position: absolute; left: 80px; right: 80px; top: 1255px; z-index: 8">
<div class="extl" style="font-family: 'Fraunces', serif; font-weight: 900; font-size: 190px; line-height: 0.86; color: #060a0c; transform: rotate(-6deg); transform-origin: left bottom; white-space: nowrap">6 DJs.</div>
<div style="margin-top: 50px; font-family: 'Fraunces', serif; font-style: italic; font-size: 54px; color: #060a0c">uma noite só.</div>
<div style="margin-top: 18px; font-size: 30px; font-weight: 700; letter-spacing: 0.08em; color: #060a0c">SEXTA · 09.10 · 22H</div>
</div>
<div style="position: absolute; left: 80px; right: 80px; bottom: 250px; display: flex; justify-content: space-between; padding-top: 22px; border-top: 2px solid #9bbdc6; font-size: 30px; letter-spacing: 0.08em; text-transform: uppercase; color: #2f4e56"><span style="white-space: nowrap">@ballyclub.oficial</span><span style="white-space: nowrap">Ingressos na bio →</span></div>
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
