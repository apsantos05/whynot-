exec(open('/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/flyer2.py').read().split("def cluster")[0])
LOGO='/_blob/e0514e9329075849b48df1e849424456'
EXTM=".extm{text-shadow:-1.5px 1.5px 0 #b3cfd6,-3px 3px 0 #9bbdc6,-4.5px 4.5px 0 #85abb5,-6px 6px 0 #7199a4,-7.5px 7.5px 0 #5f8792,-9px 9px 0 #4f7580,-10.5px 10.5px 0 #41646e,-12px 12px 0 #35535c,-13.5px 13.5px 0 #2a434b,-15px 15px 0 #20343a,-16.5px 16.5px 0 #17262b,-18px 18px 0 #0f191d}"
def cluster(Hc,s):
    S=lambda v:int(v*s)
    # mesma composição do banner da Bally (escala 1.368 a partir do banner)
    return f'''<div style="position: relative; width: 1080px; height: {Hc}px; margin: 0 auto; flex: none">
<div style="position: absolute; left: 50%; top: {S(-40)}px; width: 1100px; height: 1100px; transform: translateX(-50%); background: radial-gradient(circle, rgba(80,150,155,0.40) 0%, rgba(18,48,46,0.22) 38%, rgba(6,10,12,0) 68%)"></div>
<div style="position: absolute; left: 50%; top: {S(-260)}px; width: 1700px; height: {Hc+400}px; transform: translateX(-50%); background: conic-gradient(from 180deg at 50% 0%, transparent 152deg, rgba(228,242,246,0.08) 165deg, transparent 172deg, transparent 188deg, rgba(228,242,246,0.08) 195deg, transparent 208deg)"></div>
{place('tom',540+S(-254),'top',S(55),S(435),1,1.0)}
{place('maka',540+S(230),'top',S(44),S(451),1,1.0)}
{place('coiote',540,'top',0,S(520),2,1.0)}
{place('maycon',540+S(-156),'top',S(330),S(317),5,1.0)}
{place('mex',540+S(32),'top',S(342),S(312),6,1.0)}
{place('possani',540+S(216),'top',S(330),S(328),5,1.0)}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: {S(230)}px; z-index: 6; background: linear-gradient(to top, #060a0c 10%, rgba(6,10,12,0.7) 50%, rgba(6,10,12,0))"></div>
</div>'''
def page(title,h,body):
    return pre.replace('<title>A lista VIP é delas</title>',f'<title>{title}</title>')+f'''<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0;background:#060a0c;font-family:'Space Mono',monospace;color:#e4f2f6}}
{EXT} {EXTM}
</style>
</helmet>
<div style="width: 1080px; height: {h}px; position: relative; overflow: hidden; background: radial-gradient(ellipse at 50% 38%, #10292b 0%, #0a1315 48%, #060a0c 82%); color: #e4f2f6">
{body}
</div>
'''+post.replace('"height":1350',f'"height":{h}')
def block(top_label,date_line,top_pad,wn_fs,logo_w,cl_top,cl_h,cl_s,bot,name_fs,extra):
    return f'''<div style="position: absolute; left: 0; right: 0; top: {top_pad}px; display: flex; flex-direction: column; align-items: center; z-index: 7">
<span style="font-size: 26px; font-weight: 700; letter-spacing: 0.42em; color: #e4f2f6; white-space: nowrap">{top_label}</span>
<div class="extm" style="font-family: 'Fraunces', serif; font-weight: 900; font-size: {wn_fs}px; line-height: 0.9; color: #e4f2f6; margin-top: 40px; transform: rotate(-8deg); white-space: nowrap">why not?</div>
<img src="{LOGO}" alt="Bally Club" style="width: {logo_w}px; margin-top: 28px; opacity: 0.92">
</div>
<div style="position: absolute; left: 0; right: 0; top: {cl_top}px; z-index: 2">{cluster(cl_h,cl_s)}</div>
<div style="position: absolute; left: 0; right: 0; bottom: {bot}px; z-index: 8; display: flex; flex-direction: column; align-items: center; text-align: center">
<div class="ext" style="font-family: 'Fraunces', serif; font-weight: 900; font-size: {name_fs}px; line-height: 0.92; color: #e4f2f6; white-space: nowrap">Coiote · Maka · Tom Keller</div>
<span style="margin-top: 30px; font-size: 30px; font-weight: 700; letter-spacing: 0.16em; color: #e4f2f6; white-space: nowrap">MAYCON BEATS · MEXIKANNO · POSSANI</span>
<span style="margin-top: 22px; font-family: 'Fraunces', serif; font-weight: 900; font-size: 58px; line-height: 1; color: #e4f2f6; white-space: nowrap">{date_line}</span>
{extra}
<span style="margin-top: 22px; font-size: 24px; letter-spacing: 0.34em; color: #9dbcc4; white-space: nowrap">{ADDR}</span>
</div>'''
ADDR='AV. DR. ALBERTO ANDALÓ, 3837'
chips='<div style="margin-top: 18px; display: flex; gap: 16px"><span style="padding: 10px 20px; background: #e4f2f6; color: #060a0c; font-size: 26px; font-weight: 700; letter-spacing: 0.08em; white-space: nowrap">OPEN GIN 22H–23H</span><span style="padding: 8px 18px; border: 2px solid #9dbcc4; font-size: 26px; font-weight: 700; letter-spacing: 0.08em; white-space: nowrap">INGRESSOS ANTECIPADOS</span></div>'
TOP='SEXTA 09.10 — EDIÇÃO 01'
open(P+'FlyerFeed.dc.html','w').write(page('Flyer patrocinado · feed',1350,block(TOP,'09.10 — SEX.22H',54,80,165,322,680,0.94,60,82,chips)))
open(P+'FlyerStory.dc.html','w').write(page('Flyer patrocinado · stories',1920,block(TOP,'09.10 — SEX.22H',260,96,220,590,800,1.12,290,82,chips)))
open(P+'FeedVespera.dc.html','w').write(page('É amanhã · line-up',1350,block('É AMANHÃ — SEXTA 09.10','amanhã · 22h',54,80,165,322,680,0.94,60,82,'<span style="margin-top: 14px; font-size: 26px; font-weight: 700; letter-spacing: 0.1em; color: #e4f2f6">OPEN GIN 22H–23H · INGRESSOS NA BIO</span>')))
print('ok')
