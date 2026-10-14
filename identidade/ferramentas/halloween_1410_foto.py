"""why not? · no one leaves — peças de teaser em camadas (SVG por camada -> PNG -> PSD).
Uso: python3 build.py <pasta fontes> <pasta logo/layers> <saida>"""
import sys, os, json, asyncio, base64
from playwright.async_api import async_playwright

FONTS, LOGO, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)

def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
FACES = f"""<style>
@font-face{{font-family:'FrauncesV';font-style:italic;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FONTS+'/fs/package/files/fraunces-latin-full-italic.woff2')}) format('woff2')}}
@font-face{{font-family:'FrauncesV';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{b64(FONTS+'/fs/package/files/fraunces-latin-full-normal.woff2')}) format('woff2')}}
@font-face{{font-family:'SpaceMono';font-weight:400;src:url(data:font/woff2;base64,{b64(FONTS+'/sm/package/files/space-mono-latin-400-normal.woff2')}) format('woff2')}}
@font-face{{font-family:'SpaceMono';font-weight:700;src:url(data:font/woff2;base64,{b64(FONTS+'/sm/package/files/space-mono-latin-700-normal.woff2')}) format('woff2')}}
</style>"""

OSSO, MEDIO, BASE = "#efe4d0", "#c4a582", "#0b0706"

def svg(w, h, inner, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{FACES}{inner}</svg>')

def bg(w, h, gx, gy, r):
    d = (f'<radialGradient id="g" gradientUnits="userSpaceOnUse" cx="{gx}" cy="{gy}" r="{r}">'
         '<stop offset="0" stop-color="#2e160a"/><stop offset=".45" stop-color="#150b07"/><stop offset="1" stop-color="#0b0706"/></radialGradient>')
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="{BASE}"/><rect width="{w}" height="{h}" fill="url(#g)"/>', d)

def nevoa(w, h, y):
    d = '<filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
    els = "".join(f'<ellipse cx="{cx}" cy="{y+dy}" rx="{rx}" ry="{ry}" fill="#efe4d0" opacity="{o}"/>'
                  for cx, dy, rx, ry, o in [(w*.2, 0, 380, 70, .05), (w*.62, 30, 460, 80, .06), (w*.9, -20, 300, 60, .04), (w*.4, 60, 420, 60, .05)])
    return svg(w, h, f'<g filter="url(#b)">{els}</g>', d)

def vela(w, h, cx, top, alt=210):
    """vela fina cor de osso com chama e halo de brasa (topo da vela = top)."""
    d = ('<radialGradient id="halo"><stop offset="0" stop-color="#ffb35c" stop-opacity=".42"/>'
         '<stop offset=".35" stop-color="#e0782c" stop-opacity=".14"/><stop offset="1" stop-color="#e0782c" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="chama" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff4d6"/>'
         '<stop offset=".5" stop-color="#ffc861"/><stop offset="1" stop-color="#e9792b"/></linearGradient>'
         '<linearGradient id="cera" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bfae92"/>'
         '<stop offset=".45" stop-color="#efe4d0"/><stop offset="1" stop-color="#8f7d62"/></linearGradient>'
         '<linearGradient id="sombra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0706" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#0b0706" stop-opacity=".9"/></linearGradient>'
         '<filter id="bl"><feGaussianBlur stdDeviation="2.5"/></filter>')
    cw = 34
    inner = (f'<circle cx="{cx}" cy="{top-38}" r="300" fill="url(#halo)"/>'
             f'<rect x="{cx-cw/2}" y="{top}" width="{cw}" height="{alt}" rx="3" fill="url(#cera)"/>'
             f'<path d="M{cx-cw/2} {top+4} q6 14 2 30 q-1 6 3 4 q4 -10 1 -30 z" fill="#efe4d0" opacity=".9"/>'
             f'<rect x="{cx-cw/2}" y="{top+alt*.45}" width="{cw}" height="{alt*.55}" fill="url(#sombra)"/>'
             f'<line x1="{cx}" y1="{top}" x2="{cx+1}" y2="{top-12}" stroke="#2a1a10" stroke-width="2.5"/>'
             f'<path d="M{cx} {top-92} C{cx+16} {top-58} {cx+17} {top-32} {cx} {top-12} C{cx-17} {top-32} {cx-14} {top-58} {cx} {top-92} Z" fill="url(#chama)" filter="url(#bl)"/>'
             f'<ellipse cx="{cx}" cy="{top-30}" rx="5" ry="11" fill="#fff8e8" opacity=".9"/>')
    return svg(w, h, inner, d)

def grao(w, h):
    # grão só no canal alfa (cor fixa osso) — arquivo bem mais leve
    d = ('<filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
         '<feColorMatrix type="matrix" values="0 0 0 0 0.94  0 0 0 0 0.89  0 0 0 0 0.82  0.12 0.12 0.12 0 -0.13"/></filter>')
    return svg(w, h, f'<rect width="{w}" height="{h}" filter="url(#n)"/>', d)

def img(w, h, href, x, y, iw, ih):
    return svg(w, h, f'<image href="data:image/png;base64,{b64(href)}" x="{x}" y="{y}" width="{iw}" height="{ih}"/>')

def texto(w, h, s, x, y, size, family, color, weight=400, italic=False, anchor="middle", ls=0, caps=False):
    st = f"font-family:{family};font-size:{size}px;font-weight:{weight};{'font-style:italic;' if italic else ''}letter-spacing:{ls}em"
    return svg(w, h, f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" style="{st}">{s}</text>')

# ---------- documentos (coordenadas em 1x; render em 2x) ----------
LOGO_RETO = OUT + "/_logo_reto.png"
LOGO_INCL = os.path.dirname(LOGO) + "/composite_inclinado.png"

def T(name, s, x, y, size, fam, color, ps, **k):
    return {"type": "text", "name": name, "svg": None, "args": (s, x, y, size, fam, color), "kw": k,
            "meta": {"text": s, "font": ps, "size": size, "color": color, "x": x, "y": y,
                     "anchor": k.get("anchor", "middle"), "ls": k.get("ls", 0)}}


def foto(w, h):
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="#1c1612"/>'
        f'<rect x="40" y="40" width="{w-80}" height="{h-80}" fill="none" stroke="#3a2c22" stroke-width="3" stroke-dasharray="18 14"/>'
        f'<text x="{w/2}" y="{h/2}" fill="#5a4636" text-anchor="middle" style="font-family:SpaceMono;font-weight:700;font-size:30px;letter-spacing:.24em">FOTO AQUI</text>'
        f'<text x="{w/2}" y="{h/2+46}" fill="#4a392c" text-anchor="middle" style="font-family:SpaceMono;font-size:20px;letter-spacing:.12em">arraste a foto para cima desta camada</text>')

def escurecer(w, h, topo=.35, base=.5):
    d = ('<linearGradient id="e" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#0b0706" stop-opacity=".92"/><stop offset="{topo}" stop-color="#0b0706" stop-opacity="0"/>'
         f'<stop offset="{1-base}" stop-color="#0b0706" stop-opacity="0"/><stop offset="1" stop-color="#0b0706" stop-opacity=".95"/></linearGradient>')
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="url(#e)"/>', d)

def vinheta(w, h):
    d = '<radialGradient id="v" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="url(#v)"/>', d)

def tom(w, h):
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="#7a3a16"/>')

BLEND = {"Névoa": ("screen", 1), "Tom brasa (cor · 40%)": ("color", .4), "Vinheta": ("multiply", 1)}


from PIL import Image, ImageFilter
import numpy as np
def foto_layer(w, h, photo, s, px, py, name):
    """foto escalada s (em 1x), posicionada em px,py, bordas esfumadas no fundo; render 2x."""
    im = Image.open(photo).convert("RGB")
    W2, H2 = w*2, h*2
    fw, fh = int(im.width*s*2), int(im.height*s*2)
    im = im.resize((fw, fh), Image.LANCZOS)
    a = np.ones((fh, fw), np.float32)
    f = int(min(fw, fh)*0.16)
    ramp = np.linspace(0, 1, f)
    a[:, :f] *= ramp[None, :]; a[:, -f:] *= ramp[::-1][None, :]
    a[-f:, :] *= ramp[::-1][:, None]; a[:f, :] *= ramp[None].T if py > 0 else 1
    rgba = np.dstack([np.asarray(im), (a*255).astype(np.uint8)])
    c = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    c.alpha_composite(Image.fromarray(rgba, "RGBA"), (int(px*2), int(py*2)))
    p = f"{OUT}/_{name}.png"; c.save(p); return p


PK = "/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/hwf/photo-1633977334114-3c912e72daef.png"
def abobora(w, h, cx, cy, width, blur, bright, name):
    im = Image.open(PK).convert("RGB").crop((215, 400, 625, 730))
    im = im.point(lambda v: v*bright)
    sc = width*2/im.width; im = im.resize((int(im.width*sc), int(im.height*sc)), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur*2))
    iw, ih = im.size; yy, xx = np.mgrid[0:ih, 0:iw]
    d = np.sqrt(((xx-iw/2)/(iw*.46))**2 + ((yy-ih*.53)/(ih*.47))**2)
    a = np.clip((1-d)/.35, 0, 1)
    rgba = np.dstack([np.asarray(im), (a*255).astype(np.uint8)])
    c = Image.new("RGBA", (w*2, h*2), (0,0,0,0))
    c.alpha_composite(Image.fromarray(rgba, "RGBA"), (int(cx*2-iw/2), int(cy*2-ih/2)))
    p = f"{OUT}/_{name}.png"; c.save(p); return p
PH = "/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad/hwf/photo-1640085461451-e3dc47415dd1.png"
docs = {}
W, H = 1080, 1350
s = 1.09
FP = foto_layer(W, H, PH, s, (W-774*s)/2, 205-275*s, "foto_feed")
docs["1410_no-one-leaves_feed"] = (W, H, [
    ("Fundo", bg(W, H, 540, 380, 700)),
    ("FOTO · vela (lhon karwan / Unsplash)", "IMG:" + FP),
    ("Abóbora longe (no escuro)", "IMG:" + abobora(1080, 1350, 875, 790, 250, 1.5, .42, "ab_longe_feed")),
    ("Abóbora perto (desfocada)", "IMG:" + abobora(1080, 1350, 85, 940, 470, 5, .58, "ab_perto_feed")),
    ("Escurecer topo e base (leitura do texto)", escurecer(W, H, .22, .30)),
    ("Vinheta", vinheta(W, H)),
    ("Tom brasa (cor · 40%)", tom(W, H)),
    ("Logo why not? Halloween", "LOGO_RETO:390:50:300"),
    T("Título · no one leaves.", "no one leaves.", 540, 1180, 128, "FrauncesV", OSSO, "Fraunces-Italic", italic=True),
    T("Info · data", "COMING SOON", 540, 1272, 28, "SpaceMono", MEDIO, "SpaceMono-Bold", weight=700, ls=.42),
    ("Grão", grao(W, H)),
])
W, H = 1080, 1920
s = 1.34
FP2 = foto_layer(W, H, PH, s, (W-774*s)/2, 360-275*s, "foto_story")
docs["1410_no-one-leaves_story"] = (W, H, [
    ("Fundo", bg(W, H, 540, 560, 900)),
    ("FOTO · vela (lhon karwan / Unsplash)", "IMG:" + FP2),
    ("Abóbora longe (no escuro)", "IMG:" + abobora(1080, 1920, 885, 1110, 275, 1.5, .42, "ab_longe_story")),
    ("Abóbora perto (desfocada)", "IMG:" + abobora(1080, 1920, 70, 1250, 560, 5, .58, "ab_perto_story")),
    ("Escurecer topo e base (leitura do texto)", escurecer(W, H, .2, .34)),
    ("Vinheta", vinheta(W, H)),
    ("Tom brasa (cor · 40%)", tom(W, H)),
    ("Logo why not? Halloween", "LOGO_RETO:375:215:330"),
    T("Título · no one leaves.", "no one leaves.", 540, 1560, 132, "FrauncesV", OSSO, "Fraunces-Italic", italic=True),
    T("Info · data", "COMING SOON", 540, 1660, 28, "SpaceMono", MEDIO, "SpaceMono-Bold", weight=700, ls=.42),
    ("Grão", grao(W, H)),
])
async def render(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=2)
        for src, dst in jobs:
            open(dst[:-4] + ".svg", "w").write(src)
            await pg.goto("file://" + dst[:-4] + ".svg")
            await pg.wait_for_timeout(150)
            el = await pg.query_selector("svg")
            await el.screenshot(path=dst, omit_background=True)
            os.remove(dst[:-4] + ".svg")
        await b.close()

# logo reto: recorta o PNG transparente existente
from PIL import Image
lg = Image.open(os.path.dirname(LOGO) + "/logo-why-not-halloween.png"); lg.save(LOGO_RETO)

jobs, manifest = [], {}
for doc, (w, h, layers) in docs.items():
    d = f"{OUT}/{doc}"; os.makedirs(d, exist_ok=True)
    man = {"width": w * 2, "height": h * 2, "layers": []}
    for i, L in enumerate(layers):
        if isinstance(L, dict):
            a, k = L["args"], L["kw"]
            src = texto(w, h, *a, **k)
            f = f"{d}/{i:02d}.png"; jobs.append((src, f))
            m = dict(L["meta"]); m["x"] *= 2; m["y"] *= 2; m["size"] *= 2
            man["layers"].append({"name": L["name"], "png": f, "text": m})
        else:
            name, src = L
            if src.startswith("IMG:"):
                f = f"{d}/{i:02d}.png"; Image.open(src[4:]).save(f)
                man["layers"].append({"name": name, "png": f, "blend": None, "opacity": 1}); continue
            if src.startswith("LOGO_"):
                key, x, y, iw = src.split(":"); x, y, iw = float(x), float(y), float(iw)
                path = LOGO_RETO if key == "LOGO_RETO" else LOGO_INCL
                im = Image.open(path); ih = iw * im.height / im.width
                if key == "LOGO_INCL":  # composite tem fundo: usa só camadas sem fundo
                    path = OUT + "/_logo_incl_sem_fundo.png"
                    if not os.path.exists(path):
                        import glob
                        fs = sorted(glob.glob(LOGO + "/*.png"))[1:]
                        c = Image.open(fs[0]).convert("RGBA")
                        for f2 in fs[1:]: c = Image.alpha_composite(c, Image.open(f2).convert("RGBA"))
                        c.save(path)
                src = img(w, h, path, x, y, iw, ih)
            f = f"{d}/{i:02d}.png"; jobs.append((src, f))
            man["layers"].append({"name": name, "png": f, "blend": BLEND.get(name, (None, 1))[0], "opacity": BLEND.get(name, (None, 1))[1]})
    manifest[doc] = man

asyncio.run(render(jobs))
# prévia composta
for doc, man in manifest.items():
    c = None
    for L in man["layers"]:
        if L.get("blend") == "color": continue
        im = Image.open(L["png"]).convert("RGBA")
        c = im if c is None else Image.alpha_composite(c, im)
    c.save(f"{OUT}/{doc}/_composite.png")
    c.resize((man["width"] // 2, man["height"] // 2)).save(f"{OUT}/{doc}.png")
json.dump(manifest, open(OUT + "/manifest.json", "w"), ensure_ascii=False, indent=1)
print("ok", list(manifest))
