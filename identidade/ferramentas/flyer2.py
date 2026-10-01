P='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/latest/project/'
H=open(P+'MeioListaElas.dc.html').read(); pre=H[:H.index('<x-dc>')]; post=H[H.index('</x-dc>'):]
B={'coiote':'/_blob/874082e7e3c3ebc19c754947d2147472','maka':'/_blob/ad0d0f77c951c9c2a043783a4b433224','tom':'/_blob/6f9f48c2a707bac59f303674344e74e9','maycon':'/_blob/55a3bf7509ac2e1a93e04f79e566c966','mex':'/_blob/9175e9ba42ccfe1808ec8578f27d1f6c','possani':'/_blob/170496fafef725cc68299d6c884b5fe7'}
import json; ASP=json.load(open('/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/lineup/asp.json')); ASP.update(json.load(open('/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/lineup/asp_hq.json')))
FONT='<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,900;1,9..144,400&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">'
EXT=".ext{text-shadow:-2px 2px 0 #b3cfd6,-4px 4px 0 #9bbdc6,-6px 6px 0 #85abb5,-8px 8px 0 #7199a4,-10px 10px 0 #5f8792,-12px 12px 0 #4f7580,-14px 14px 0 #41646e,-16px 16px 0 #35535c,-18px 18px 0 #2a434b,-20px 20px 0 #20343a,-22px 22px 0 #17262b,-24px 24px 0 #0f191d} .ext2{text-shadow:-1px 1px 0 #9bbdc6,-2px 2px 0 #7199a4,-3px 3px 0 #4f7580,-4px 4px 0 #35535c,-5px 5px 0 #20343a,-6px 6px 0 #0f191d}"
def im(k,css,z,shadow=True): return f'<img src="{B[k]}" alt="" style="position: absolute; {css}; z-index: {z}; {"filter: drop-shadow(0 10px 30px rgba(0,0,0,0.85));" if shadow else ""}">'
def place(k,cx,anchor,off,h,z,br):
    w=int(h*ASP[k]); return f'<img src="{B[k]}" alt="" style="position: absolute; left: {int(cx-w/2)}px; {anchor}: {off}px; height: {h}px; z-index: {z}; filter: brightness({br}) drop-shadow(0 12px 30px rgba(0,0,0,0.85))">'
def cluster(Hc,s=1.0):
    S=lambda v:int(v*s)
    return f'''<div style="position: relative; width: 1080px; height: {Hc}px; margin: 0 auto; flex: none">
<div style="position: absolute; left: 50%; top: {S(-40)}px; width: 1100px; height: 1100px; transform: translateX(-50%); background: radial-gradient(circle, rgba(80,150,155,0.40) 0%, rgba(18,48,46,0.22) 38%, rgba(6,10,12,0) 68%)"></div>
<div style="position: absolute; left: 50%; top: {S(-260)}px; width: 1700px; height: {Hc+400}px; transform: translateX(-50%); background: conic-gradient(from 180deg at 50% 0%, transparent 152deg, rgba(228,242,246,0.08) 165deg, transparent 172deg, transparent 188deg, rgba(228,242,246,0.08) 195deg, transparent 208deg)"></div>
{place('tom',225,'top',S(30),S(470),1,1.0)}
{place('maka',850,'top',S(20),S(480),1,1.0)}
{place('coiote',540,'top',S(0),S(520),2,1.0)}
{place('maycon',305,'bottom',S(80),S(320),5,1.0)}
{place('mex',540,'bottom',S(70),S(320),6,1.0)}
{place('possani',778,'bottom',S(-26),S(436),5,1.0)}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: {S(230)}px; z-index: 6; background: linear-gradient(to top, #060a0c 10%, rgba(6,10,12,0.7) 50%, rgba(6,10,12,0))"></div>
</div>'''
def page(title,h,inset,body):
    return pre.replace('<title>A lista VIP é delas</title>',f'<title>{title}</title>')+f'''<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0;background:#060a0c;font-family:'Space Mono',monospace;color:#e4f2f6}}
{EXT}
</style>
</helmet>
<div style="width: 1080px; height: {h}px; position: relative; overflow: hidden; background: radial-gradient(ellipse at 50% 38%, #10292b 0%, #0a1315 48%, #060a0c 82%); color: #e4f2f6">
{body}
</div>
'''+post.replace('"height":1350',f'"height":{h}')
def block(top_label,date_line,addr,inset_pad,cl_h,logo_fs,name_fs,names_fs,date_fs,gap_top,extra=''):
    return f'''<div style="position: absolute; inset: {inset_pad}; display: flex; flex-direction: column; align-items: center; z-index: 7">
<span style="font-size: 26px; font-weight: 700; letter-spacing: 0.42em; color: #e4f2f6; white-space: nowrap; margin-top: {gap_top}px">{top_label}</span>
<div class="ext2" style="font-family: 'Fraunces', serif; font-weight: 900; font-size: {logo_fs}px; line-height: 0.9; color: #e4f2f6; margin: 18px 0 0; white-space: nowrap">why not?</div>
</div>
<div style="position: absolute; left: 0; right: 0; top: {cl_h[0]}px; z-index: 2">{cluster(cl_h[1],cl_h[2])}</div>
<div style="position: absolute; left: 0; right: 0; bottom: {cl_h[3]}px; z-index: 8; display: flex; flex-direction: column; align-items: center; text-align: center">
<div class="ext" style="font-family: 'Fraunces', serif; font-weight: 900; font-size: {name_fs}px; line-height: 0.92; color: #e4f2f6; white-space: nowrap">Coiote · Maka</div>
<span style="margin-top: 26px; font-size: {names_fs}px; font-weight: 700; letter-spacing: 0.16em; line-height: 1.55; color: #e4f2f6; white-space: nowrap">TOM KELLER · MAYCON BEATS<br>MEXIKANNO · POSSANI</span>
<span style="margin-top: 22px; font-family: 'Fraunces', serif; font-weight: 900; font-size: {date_fs}px; line-height: 1; color: #e4f2f6; white-space: nowrap">{date_line}</span>
{extra}
<span style="margin-top: 22px; font-size: 24px; letter-spacing: 0.34em; color: #9dbcc4; white-space: nowrap">{addr}</span>
</div>'''
ADDR='AV. DR. ALBERTO ANDALÓ, 3837'
chips='<div style="margin-top: 18px; display: flex; gap: 16px"><span style="padding: 10px 20px; background: #e4f2f6; color: #060a0c; font-size: 26px; font-weight: 700; letter-spacing: 0.08em; white-space: nowrap">OPEN GIN 22H–23H</span><span style="padding: 8px 18px; border: 2px solid #9dbcc4; font-size: 26px; font-weight: 700; letter-spacing: 0.08em; white-space: nowrap">INGRESSOS ANTECIPADOS</span></div>'
open(P+'FlyerFeed.dc.html','w').write(page('Flyer patrocinado · feed',1350,'34px',block('BALLY CLUB — 09.OUTUBRO','09.10 — SEX.22H',ADDR,'34px',(210,740,1.0,70),88,128,30,58,30,chips)))
open(P+'FlyerStory.dc.html','w').write(page('Flyer patrocinado · stories',1920,'34px',block('BALLY CLUB — 09.OUTUBRO','09.10 — SEX.22H',ADDR,'34px 34px',(440,800,1.06,330),100,136,32,62,200,chips)))
open(P+'FeedVespera.dc.html','w').write(page('É amanhã · line-up',1350,'34px',block('É AMANHÃ — SEXTA 09.10','amanhã · 22h',ADDR,'34px',(210,740,1.0,70),88,128,30,58,30,'<span style="margin-top: 14px; font-size: 26px; font-weight: 700; letter-spacing: 0.1em; color: #e4f2f6">OPEN GIN 22H–23H · INGRESSOS NA BIO</span>')))
print('ok')
