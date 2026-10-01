import re, os, sys, asyncio
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "latest/project")
OUT = os.path.join(D, sys.argv[1] if len(sys.argv) > 1 else "render")
os.makedirs(OUT, exist_ok=True)
FD = "file://" + os.path.join(D, "fr/UnderCaseType_Fraunces_1.000/Fonts - Desktop/static/ttf/")
FONTS = f"""
@font-face{{font-family:'Fraunces';font-weight:400;font-style:normal;src:url('{FD}Fraunces72pt-Regular.ttf')}}
@font-face{{font-family:'Fraunces';font-weight:400;font-style:italic;src:url('{FD}Fraunces72pt-Italic.ttf')}}
@font-face{{font-family:'Fraunces';font-weight:900;font-style:normal;src:url('{FD}Fraunces144pt-Black.ttf')}}
@font-face{{font-family:'Space Mono';font-weight:400;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')}}
@font-face{{font-family:'Space Mono';font-weight:700;src:url('file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')}}
"""
BLOBS = {"/_blob/e72d80fe5295e0f6d618ed57794eed5f": "file://" + os.path.join(D, "lineup/y_coiote.png"), "/_blob/607d52ea78957bb726e94c0c74697b22": "file://" + os.path.join(D, "lineup/y_maka.png"), "/_blob/6f9f48c2a707bac59f303674344e74e9": "file://" + os.path.join(D, "lineup/y_tom.png"), "/_blob/6bbdaa5f85f08507008edcd2f3e1625f": "file://" + os.path.join(D, "lineup/y_maycon.png"), "/_blob/cae97cc1258c489bf475fc64ab556147": "file://" + os.path.join(D, "lineup/y_mex.png"), "/_blob/f14ebfcf15696bce8a104165027909ae": "file://" + os.path.join(D, "lineup/y_possani3.png"), "/_blob/ac64e495432b9d0103a5fa0b45884bb5": "file://" + os.path.join(D, "lineup/y_possani2.png"), "/_blob/997d8588bb4240ff02319aaa67f12151": "file://" + os.path.join(D, "lineup/y_possani.png"), "/_blob/153db1e60f8da6de296edbd3a49d7018": "file://" + os.path.join(D, "lineup/x_coiote.png"), "/_blob/f0f50e821b95559bd16f5ff6a3aa4f59": "file://" + os.path.join(D, "lineup/x_maka.png"), "/_blob/b96cb778bf68e47c492881328cd6e634": "file://" + os.path.join(D, "lineup/x_tom.png"), "/_blob/6b157239bb93aefbb40e2db4c363a99a": "file://" + os.path.join(D, "lineup/x_maycon.png"), "/_blob/2c1563636045c98448989cf770ae6b21": "file://" + os.path.join(D, "lineup/x_mex.png"), "/_blob/d7ab5ea2fd9194f7c8107a3e5fa019ed": "file://" + os.path.join(D, "lineup/x_possani.png"), "/_blob/23f1b5e8f6700eb0afa1caa5406f4afc": "file://" + os.path.join(D, "lineup/g_coiote.png"), "/_blob/a71ae21feb22aeec495a3dce635de885": "file://" + os.path.join(D, "lineup/g_maka.png"), "/_blob/336b3eb60fb35655146d4f73ade775b2": "file://" + os.path.join(D, "lineup/g_tom.jpg"), "/_blob/cf76cff641827cf41f59ee95d831fd4c": "file://" + os.path.join(D, "lineup/g_maycon.jpg"), "/_blob/5b4120833f2f5311758976da6625a979": "file://" + os.path.join(D, "lineup/g_mex.jpg"), "/_blob/73bf00f7bf17e277f7520353b1b221da": "file://" + os.path.join(D, "lineup/g_possani.jpg"), "/_blob/61fe9268be9546536f564e16c5ca8035": "file://" + os.path.join(D, "tom/foto.jpg"), "/_blob/f630657ea00da58da8f948bf4bf674cd": "file://" + os.path.join(D, "wn/logo.png"),
         "/_blob/e1675d9aa871be3e2ad4e98de756f702": "file://" + os.path.join(D, "mex/foto-mex.jpg"), "/_blob/939bd0cc3dc170954d571757c9e7f137": "file://" + os.path.join(D, "may/foto-maycon.jpg"), "/_blob/dbcde4075317bf019963d992a6a3a381": "file://" + os.path.join(D, "dl/capa-reels-whynot-09-10.jpg")}

def page_html(src):
    body = re.search(r"<x-dc>(.*)</x-dc>", src, re.S).group(1)
    body = re.sub(r"<link[^>]*>", "", body)
    body = body.replace("<helmet>", "").replace("</helmet>", "")
    for k, v in BLOBS.items(): body = body.replace(k, v)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}</style></head><body style='margin:0'>{body}</body></html>"

async def main():
    files = sys.argv[2:]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f in files:
            src = open(os.path.join(SRC, f)).read()
            h = 1920 if "height: 1920px" in src else 1350
            pg = await b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=2)
            tmp = os.path.join(OUT, f + ".html"); open(tmp, "w").write(page_html(src))
            await pg.goto("file://" + tmp); await pg.wait_for_timeout(300)
            # report overflow + smallest text
            info = await pg.evaluate("""() => {
              const root = document.body.firstElementChild; const rr = root.getBoundingClientRect();
              let min = 999, over = [], wrap = [];
              document.querySelectorAll('span,p,div').forEach(el => {
                const hasText = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim());
                if (!hasText) return;
                const cs = getComputedStyle(el); const fs = parseFloat(cs.fontSize); if (fs < min) min = fs;
                if (cs.transform !== 'none') { const r = el.getBoundingClientRect(); if (r.right > rr.right-10 || r.left < rr.left+10) over.push('BIG:'+el.textContent.trim().slice(0,20)); return; }
                const r = el.getBoundingClientRect();
                if (r.right > rr.right - 60 || r.left < rr.left + 60) over.push(el.textContent.trim().slice(0,30));
                const lh = parseFloat(cs.lineHeight) || fs*1.2;
                if (cs.textTransform === 'uppercase' && r.height > lh*1.6) wrap.push(el.textContent.trim().slice(0,30));
              });
              return {min, over, wrap};
            }""")
            print(f, "min", info["min"], "OVER", info["over"], "WRAP", info["wrap"])
            await pg.screenshot(path=os.path.join(OUT, f.replace(".dc.html", ".png")))
            await pg.close()
        await b.close()
asyncio.run(main())
