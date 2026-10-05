"""Banner 1024x600 para o site da Bally (página de ingressos). Gera 1x e 2x."""
import os, sys, asyncio, json
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
FD = "file://" + os.path.join(D, "fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/")
FONTS = f"""
@font-face{{font-family:'Fraunces';font-weight:400;font-style:italic;src:url('{FD}Fraunces72pt-Italic.ttf')}}
@font-face{{font-family:'Fraunces';font-weight:900;font-style:normal;src:url('{FD}Fraunces144pt-Black.ttf')}}
@font-face{{font-family:'Mono';font-weight:400;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')}}
@font-face{{font-family:'Mono';font-weight:700;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')}}
"""
L = lambda f: "file://" + os.path.join(D, "lineup", f)
IMG = {"tom": L("y_tom.png"), "coiote": L("z_coiote.png"), "maka": L("z_maka6.png"),
       "maycon": L("z_maycon.png"), "mex": L("z_mex.png"), "possani": L("z_possani.png")}
ASP = json.load(open(os.path.join(D, "lineup/asp.json"))); ASP.update(json.load(open(os.path.join(D, "lineup/asp_hq.json"))))
ASP["maka"] = 0.7146

def place(k, cx, top=None, bottom=None, h=300, z=1):
    w = int(h * ASP[k]); pos = f"top:{top}px" if top is not None else f"bottom:{bottom}px"
    return (f'<img src="{IMG[k]}" style="position:absolute;left:{int(cx - w/2)}px;{pos};height:{h}px;z-index:{z};'
            f'filter:drop-shadow(0 8px 20px rgba(0,0,0,.85))">')

EXT = ("text-shadow:-1px 1px 0 #b3cfd6,-2px 2px 0 #9bbdc6,-3px 3px 0 #85abb5,-4px 4px 0 #7199a4,-5px 5px 0 #5f8792,"
       "-6px 6px 0 #4f7580,-7px 7px 0 #41646e,-8px 8px 0 #35535c,-9px 9px 0 #2a434b,-10px 10px 0 #20343a,-11px 11px 0 #17262b,-12px 12px 0 #0f191d")
EXT8 = ("text-shadow:-1px 1px 0 #b3cfd6,-2px 2px 0 #9bbdc6,-3px 3px 0 #7199a4,-4px 4px 0 #5f8792,-5px 5px 0 #4f7580,-6px 6px 0 #35535c,-7px 7px 0 #20343a,-8px 8px 0 #0f191d")
EXT2 = "text-shadow:-1px 1px 0 #9bbdc6,-2px 2px 0 #4f7580,-3px 3px 0 #20343a,-4px 4px 0 #0f191d"

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{box-sizing:border-box}} body{{margin:0;background:#060a0c}}
.wrap{{position:relative;width:1024px;height:600px;overflow:hidden;color:#e4f2f6;font-family:'Mono',monospace;
 background:radial-gradient(ellipse 620px 520px at 735px 300px,#12302f 0%,#0b1719 45%,#060a0c 78%)}}
.mono{{font-family:'Mono',monospace;text-transform:uppercase}}
.serif{{font-family:'Fraunces',serif}}
</style></head><body><div class="wrap">

<!-- feixes de luz atrás dos DJs -->
<div style="position:absolute;left:735px;top:-120px;width:900px;height:760px;transform:translateX(-50%);
 background:conic-gradient(from 180deg at 50% 0%,transparent 150deg,rgba(228,242,246,.07) 163deg,transparent 171deg,transparent 189deg,rgba(228,242,246,.07) 197deg,transparent 210deg)"></div>
<div style="position:absolute;left:735px;top:40px;width:560px;height:560px;transform:translateX(-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(80,150,155,.34) 0%,rgba(18,48,46,.18) 42%,rgba(6,10,12,0) 70%)"></div>

<!-- DJs: atrás Tom · Coiote · Maka, na frente Maycon · Mexikanno · Possani -->
<div style="position:absolute;left:0;top:0;width:1024px;height:600px">
 {place('tom', 556, top=78, h=318, z=1)}
 {place('maka', 910, top=70, h=330, z=1)}
 {place('coiote', 742, top=38, h=380, z=2)}
 {place('maycon', 628, bottom=88, h=232, z=5)}
 {place('mex', 766, bottom=84, h=228, z=6)}
 {place('possani', 900, bottom=80, h=240, z=5)}
</div>
<!-- fusão com o fundo: base e borda esquerda do grupo -->
<div style="position:absolute;left:0;right:0;bottom:0;height:120px;z-index:7;background:linear-gradient(to top,#060a0c 8%,rgba(6,10,12,.6) 55%,rgba(6,10,12,0))"></div>
<div style="position:absolute;left:330px;top:0;bottom:0;width:240px;z-index:7;background:linear-gradient(to right,#060a0c 18%,rgba(6,10,12,0))"></div>

<!-- bloco de texto -->
<div style="position:absolute;left:52px;top:46px;bottom:44px;width:440px;z-index:9;display:flex;flex-direction:column">
 <span class="mono" style="font-size:12px;font-weight:700;letter-spacing:.32em;color:#9dbcc4">Sexta 09.10 — Edição 01</span>
 <div class="serif" style="font-weight:900;font-size:64px;line-height:.9;margin-top:46px;margin-left:12px;transform:rotate(-8deg);transform-origin:left center;white-space:nowrap;{EXT}">why not?</div>
 <img src="{L('bally_logo_gelo.png')}" style="width:150px;margin-top:74px;opacity:.92">

 <div style="margin-top:auto">
  <div class="serif" style="font-weight:900;font-size:41px;line-height:.92;letter-spacing:-.005em;{EXT8};white-space:nowrap">Coiote · Maka · Tom Keller</div>
  <div class="mono" style="font-size:14px;font-weight:700;letter-spacing:.14em;line-height:1.75;margin-top:20px">Maycon Beats · Mexikanno · Possani</div>
 </div>

 <div style="margin-top:22px;display:flex;align-items:center;gap:14px">
  <span class="serif" style="font-weight:900;font-size:34px;line-height:1;white-space:nowrap">09.10 — 22h</span>
  <span class="mono" style="padding:7px 12px;background:#e4f2f6;color:#060a0c;font-size:11px;font-weight:700;letter-spacing:.1em;white-space:nowrap">Open gin 22h–23h</span>
 </div>
 <span class="mono" style="font-size:11px;letter-spacing:.24em;color:#9dbcc4;margin-top:14px">Av. Dr. Alberto Andaló, 3837</span>
</div>

<!-- grão sutil -->
<div style="position:absolute;inset:0;z-index:10;pointer-events:none;opacity:.06;mix-blend-mode:screen;
 background-image:url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22><filter id=%22n%22><feTurbulence baseFrequency=%22.9%22 numOctaves=%222%22/></filter><rect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22/></svg>')"></div>
</div></body></html>"""

async def main():
    out = os.path.join(D, "bally"); os.makedirs(out, exist_ok=True)
    p = os.path.join(out, "banner.html"); open(p, "w").write(HTML)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for s, name in ((1, "whynot-bally-1024x600.png"), (2, "whynot-bally-1024x600@2x.png")):
            pg = await b.new_page(viewport={"width": 1024, "height": 600}, device_scale_factor=s)
            await pg.goto("file://" + p); await pg.wait_for_timeout(500)
            await pg.screenshot(path=os.path.join(out, name), clip={"x": 0, "y": 0, "width": 1024, "height": 600})
        await b.close()
    print("ok")
asyncio.run(main())
