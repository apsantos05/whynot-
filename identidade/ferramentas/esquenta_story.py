import asyncio,os
from playwright.async_api import async_playwright
D='/tmp/claude-0/-home-claude/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
FD="file://"+D+"/fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/"
EXT="text-shadow:-2px 2px 0 #b3cfd6,-4px 4px 0 #9bbdc6,-6px 6px 0 #85abb5,-8px 8px 0 #7199a4,-10px 10px 0 #5f8792,-12px 12px 0 #4f7580,-14px 14px 0 #41646e,-16px 16px 0 #35535c,-18px 18px 0 #2a434b,-20px 20px 0 #20343a,-22px 22px 0 #17262b,-24px 24px 0 #0f191d"
EXTM="text-shadow:-1px 1px 0 #b3cfd6,-2px 2px 0 #9bbdc6,-3px 3px 0 #7199a4,-4px 4px 0 #5f8792,-5px 5px 0 #4f7580,-6px 6px 0 #35535c,-7px 7px 0 #20343a,-8px 8px 0 #0f191d"
H=f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:F;font-weight:900;src:url('{FD}Fraunces144pt-Black.ttf')}}
@font-face{{font-family:F;font-style:italic;font-weight:400;src:url('{FD}Fraunces72pt-Italic.ttf')}}
@font-face{{font-family:M;font-weight:400;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')}}
@font-face{{font-family:M;font-weight:700;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')}}
body{{margin:0}} .w{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#060a0c;color:#e4f2f6;font-family:M}}
</style></head><body><div class=w>
<img src="file://{D}/tw/tw_logo.png" style="position:absolute;left:50%;transform:translateX(-50%);top:360px;height:600px">
<div style="position:absolute;left:80px;right:80px;top:250px;display:flex;justify-content:space-between;font-size:28px;letter-spacing:.16em;color:#c9dde2"><span>WHY NOT? · ESQUENTA</span><span>SEXTA · 09.10</span></div>
<div style="position:absolute;left:80px;right:80px;top:1040px">
<div style="font:900 150px/0.86 F;{EXT};transform:rotate(-6deg);transform-origin:left center;white-space:nowrap;margin-left:14px">esquenta.</div>
<div style="margin-top:44px;font:italic 40px F">antes da Bally, o aquecimento é no The Week.</div>
<div style="margin-top:30px;display:flex;flex-direction:column;gap:14px">
<div style="display:flex;align-items:center;gap:20px"><span style="padding:12px 20px;background:#e4f2f6;color:#060a0c;font-size:30px;font-weight:700;letter-spacing:.06em;white-space:nowrap">TODO MUNDO FREE ATÉ 21H</span></div>
<div style="display:flex;align-items:center;gap:20px"><span style="padding:10px 18px;border:2px solid #9dbcc4;font-size:30px;font-weight:700;letter-spacing:.06em;white-space:nowrap">MENINAS DA LISTA GANHAM UM DRINK 🍸</span></div>
</div>
<div style="margin-top:20px;font-size:24px;letter-spacing:.1em;color:#9dbcc4">* VÁLIDO PARA QUEM ESTÁ NA LISTA VIP DA BALLY</div>
</div>
<div style="position:absolute;left:80px;right:80px;bottom:250px;display:flex;justify-content:space-between;align-items:flex-end;padding-top:22px;border-top:2px solid #35535c">
<span style="font-size:26px;letter-spacing:.08em;color:#9dbcc4;line-height:1.5">DEPOIS, 22H<br><b style="color:#e4f2f6">WHY NOT? NA BALLY CLUB</b></span>
<span style="font:900 64px/1 F;{EXTM};transform:rotate(-6deg);white-space:nowrap">why not?</span></div>
</div></body></html>"""
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for s,n in ((1,'esqs1.png'),(2,'story-esquenta-the-week-HD.png')):
            pg=await b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=s)
            open(D+'/tw/es.html','w').write(H); await pg.goto('file://'+D+'/tw/es.html'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=D+'/tw/'+n)
        await b.close()
asyncio.run(m())
