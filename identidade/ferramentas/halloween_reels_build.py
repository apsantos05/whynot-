import base64, os, sys
S='/tmp/claude-0/-home-claude-whynot-/85f2d3d2-8d73-51f7-b638-521bd0946f03/scratchpad'
R=S+'/reel'
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
FF=S+'/hwb/node_modules/@fontsource-variable/fraunces/files/'
SM=S+'/hwb/node_modules/@fontsource/space-mono/files/'
LOCAL = len(sys.argv)>1 and sys.argv[1]=='local'
img=lambda k: 'data:image/jpeg;base64,'+b64(f'{R}/img/{k}.jpg')
logo='data:image/png;base64,'+b64('/home/claude/whynot-/identidade/assets/logo/halloween/logo-why-not-halloween.png')
audio='data:audio/mpeg;base64,'+b64(R+'/mix.mp3')
J='/mnt/user-data/uploads/Downloads/_claude_assets/js/'
if LOCAL:
    scripts=f'<script src="file://{J}gsap.min.js"></script>'
else:
    scripts=('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n'
             '<script src="https://cdn.jsdelivr.net/npm/@hyperframes/core/dist/hyperframe.runtime.iife.js"></script>')
def chars(s, cls):
    return ''.join(f'<span class="{cls}">{c if c!=" " else "&nbsp;"}</span>' for c in s)
html=f'''<!doctype html>
<html lang="pt-BR" style="overflow:hidden; margin:0">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>why not? · no one leaves — reels de apresentação</title>
{scripts}
<style>
@font-face{{font-family:"WN Serif";font-style:italic;font-weight:100 900;font-display:block;src:url(data:font/woff2;base64,{b64(FF+'fraunces-latin-full-italic.woff2')}) format("woff2")}}
@font-face{{font-family:"WN Serif";font-style:normal;font-weight:100 900;font-display:block;src:url(data:font/woff2;base64,{b64(FF+'fraunces-latin-full-normal.woff2')}) format("woff2")}}
@font-face{{font-family:"WN Mono";font-weight:700;font-display:block;src:url(data:font/woff2;base64,{b64(SM+'space-mono-latin-700-normal.woff2')}) format("woff2")}}
:root{{--bg:#0b0706;--osso:#efe4d0;--ambar:#c4a582;--brasa:#2e160a;--serif:"WN Serif",Georgia,serif;--mono:"WN Mono",monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--bg);color:var(--osso)}}
.scene{{position:absolute;top:0;left:0;width:1080px;height:1920px;overflow:hidden;background:var(--bg)}}
.scene-content{{position:relative;z-index:2;width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center}}
.photo{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;transform-origin:50% 45%}}
.shade{{position:absolute;inset:0;background:#0b0706;opacity:0;z-index:1;pointer-events:none}}
.glow{{position:absolute;left:50%;top:38%;width:900px;height:900px;margin:-450px 0 0 -450px;border-radius:50%;background:radial-gradient(circle,rgba(230,140,60,.28),rgba(46,22,10,.12) 45%,rgba(11,7,6,0) 70%);z-index:0}}
.kicker{{font-family:var(--mono);font-weight:700;font-size:28px;letter-spacing:.32em;color:var(--ambar)}}
.line{{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--osso);line-height:1;text-shadow:0 0 40px rgba(230,140,60,.35)}}
.ch{{display:inline-block}}
.grain{{position:absolute;inset:0;pointer-events:none;z-index:50;opacity:.16;mix-blend-mode:overlay;background-image:radial-gradient(rgba(255,255,255,.08) 1px,transparent 1.2px),radial-gradient(rgba(0,0,0,.18) 1px,transparent 1.2px);background-size:3px 3px,5px 5px;background-position:0 0,1px 2px}}
</style>
</head>
<body>
<div id="main" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="21">
<audio id="trilha" data-start="0" data-duration="21" data-track-index="1" src="{audio}"></audio>

<div class="scene clip" id="s1" data-start="0" data-duration="2.2" data-track-index="0">
  <img id="s1-img" class="photo" src="{img('candle')}" alt="vela acesa">
  <div id="s1-shade" class="shade" style="opacity:1"></div>
  <div class="scene-content"></div>
</div>

<div class="scene clip" id="s2" data-start="2.2" data-duration="3.8" data-track-index="0" style="visibility:hidden;">
  <img id="s2-a" class="photo" src="{img('door')}" alt="porta entreaberta" style="opacity:0">
  <img id="s2-b" class="photo" src="{img('chandelier')}" alt="arandela" style="opacity:0">
  <img id="s2-c" class="photo" src="{img('mask')}" alt="máscara" style="opacity:0">
  <img id="s2-d" class="photo" src="{img('door')}" alt="porta" style="opacity:0">
  <img id="s2-e" class="photo" src="{img('mask')}" alt="máscara" style="opacity:0">
  <div class="scene-content"></div>
</div>

<div class="scene clip" id="s3" data-start="6" data-duration="3" data-track-index="0" style="visibility:hidden;">
  <div class="glow" id="s3-glow"></div>
  <div class="scene-content">
    <div id="s3-k" class="kicker">WHY NOT? · HALLOWEEN</div>
    <div id="s3-t" class="line" style="font-size:150px;margin-top:70px">{chars('quem entra…','ch s3c')}</div>
  </div>
</div>

<div class="scene clip" id="s4" data-start="9" data-duration="4" data-track-index="0" style="visibility:hidden;">
  <img id="s4-a" class="photo" src="{img('woman')}" alt="mulher com candelabros">
  <img id="s4-b" class="photo" src="{img('table')}" alt="mesa com velas" style="opacity:0">
  <img id="s4-c" class="photo" src="{img('pumpkins')}" alt="abóboras no escuro" style="opacity:0">
  <img id="s4-d" class="photo" src="{img('skull')}" alt="vela derretida" style="opacity:0">
  <div id="s4-shade" class="shade"></div>
  <div class="scene-content"></div>
</div>

<div class="scene clip" id="s5" data-start="13" data-duration="2" data-track-index="0" style="visibility:hidden;">
  <div class="glow" id="s5-glow"></div>
  <div class="scene-content">
    <div id="s5-t" class="line" style="font-size:230px">{chars('…fica.','ch s5c')}</div>
  </div>
</div>

<div class="scene clip" id="s6" data-start="15" data-duration="3.2" data-track-index="0" style="visibility:hidden;">
  <img id="s6-a" class="photo" src="{img('candle')}" alt="vela acesa">
  <img id="s6-b" class="photo" src="{img('smoke')}" alt="vela apagada com fumaça" style="opacity:0">
  <div id="s6-shade" class="shade"></div>
  <div class="scene-content" style="justify-content:flex-end;padding-bottom:420px">
    <div id="s6-t" class="line" style="font-size:132px">no one leaves.</div>
  </div>
</div>

<div class="scene clip" id="s7" data-start="18.2" data-duration="2.8" data-track-index="0" style="visibility:hidden;">
  <div class="glow" id="s7-glow" style="top:45%"></div>
  <div class="scene-content">
    <img id="s7-logo" src="{logo}" alt="why not? Halloween" style="width:720px">
    <div id="s7-k" class="kicker" style="margin-top:80px;font-size:34px;letter-spacing:.5em">COMING SOON</div>
  </div>
  <div id="s7-shade" class="shade"></div>
</div>

<div class="grain"></div>
</div>

<script>
window.__timelines = window.__timelines || {{}};
var tl = gsap.timeline({{ paused: true }});
// visibilidade das cenas (cortes secos)
tl.set("#s1", {{autoAlpha:0}}, 2.2);
[["#s2",2.2,6],["#s3",6,9],["#s4",9,13],["#s5",13,15],["#s6",15,18.2]].forEach(function(s){{
  tl.set(s[0], {{autoAlpha:1}}, s[1]); tl.set(s[0], {{autoAlpha:0}}, s[2]);
}});
tl.set("#s7", {{autoAlpha:1}}, 18.2);

// S1 — a vela acende no escuro
tl.to("#s1-shade", {{opacity:0, duration:1.1, ease:"power2.out"}}, 0.3);
tl.fromTo("#s1-img", {{scale:1.0}}, {{scale:1.09, duration:2.2, ease:"sine.inOut"}}, 0);
tl.to("#s1-shade", {{opacity:0.22, duration:0.09, yoyo:true, repeat:5, ease:"sine.inOut"}}, 1.25);

// S2 — flashes no escuro, sincronizados com as batidas
[["#s2-a",2.2],["#s2-b",3.0],["#s2-c",3.8],["#s2-d",4.6],["#s2-e",5.3]].forEach(function(f,i){{
  tl.set(f[0], {{opacity:1, scale:1.06, x:(i%2?-14:14)}}, f[1]);
  tl.to(f[0], {{scale:1.0, x:0, duration:0.4, ease:"power4.out"}}, f[1]);
  tl.to(f[0], {{opacity:0, duration:0.35, ease:"power2.in"}}, f[1]+0.22);
}});
tl.to("#s2-e", {{opacity:0.35, duration:0.06, yoyo:true, repeat:3, ease:"none"}}, 5.62);

// S3 — "quem entra…"
tl.from("#s3-k", {{autoAlpha:0, y:20, duration:0.5, ease:"power2.out"}}, 6.15);
tl.from(".s3c", {{autoAlpha:0, y:40, filter:"blur(8px)", duration:0.45, ease:"expo.out", stagger:{{each:0.09, from:"start"}}}}, 6.4);
tl.fromTo("#s3-glow", {{opacity:0.4, scale:0.9}}, {{opacity:1, scale:1.08, duration:0.7, yoyo:true, repeat:3, ease:"sine.inOut"}}, 6.0);
tl.to("#s3-t", {{y:-12, duration:1.2, yoyo:true, repeat:1, ease:"sine.inOut"}}, 6.6);

// S4 — cortes na batida
[["#s4-a",9],["#s4-b",10],["#s4-c",11],["#s4-d",12]].forEach(function(c,i){{
  if(i>0) tl.set(c[0], {{opacity:1}}, c[1]);
  tl.fromTo(c[0], {{scale:1.14}}, {{scale:1.0, duration:1.0, ease:"power2.out"}}, c[1]);
  tl.fromTo("#s4-shade", {{opacity:0.85}}, {{opacity:0, duration:0.25, ease:"power4.out"}}, c[1]);
  tl.to("#s4-shade", {{opacity:0.18, duration:0.08, yoyo:true, repeat:3, ease:"sine.inOut"}}, c[1]+0.45);
}});

// S5 — "…fica."
tl.from(".s5c", {{autoAlpha:0, scale:1.6, duration:0.5, ease:"back.out(1.6)", stagger:{{each:0.07, from:"start"}}}}, 13.1);
tl.fromTo("#s5-glow", {{opacity:0.3}}, {{opacity:1, duration:0.45, yoyo:true, repeat:3, ease:"sine.inOut"}}, 13.0);
tl.to("#s5-t", {{letterSpacing:"0.04em", duration:1.6, ease:"sine.out"}}, 13.3);

// S6 — o sopro: a vela apaga
tl.fromTo("#s6-a", {{scale:1.05}}, {{scale:1.12, duration:0.5, ease:"sine.in"}}, 15.0);
tl.to("#s6-shade", {{opacity:0.35, duration:0.05, yoyo:true, repeat:5, ease:"none"}}, 15.15);
tl.set("#s6-shade", {{opacity:1}}, 15.5);
tl.set("#s6-b", {{opacity:1}}, 15.5);
tl.to("#s6-shade", {{opacity:0, duration:0.7, ease:"power2.out"}}, 15.75);
tl.fromTo("#s6-b", {{scale:1.0}}, {{scale:1.08, duration:2.6, ease:"sine.inOut"}}, 15.5);
tl.from("#s6-t", {{autoAlpha:0, y:30, filter:"blur(10px)", duration:0.8, ease:"power3.out"}}, 16.3);

// S7 — logo + coming soon
tl.from("#s7-logo", {{autoAlpha:0, scale:0.86, duration:0.8, ease:"expo.out"}}, 18.3);
tl.from("#s7-k", {{autoAlpha:0, letterSpacing:"1.1em", duration:0.9, ease:"power2.out"}}, 18.8);
tl.fromTo("#s7-glow", {{opacity:0.4}}, {{opacity:1, duration:0.5, yoyo:true, repeat:1, ease:"sine.inOut"}}, 18.2);
tl.to("#s7-logo", {{y:-8, duration:0.6, yoyo:true, repeat:1, ease:"sine.inOut"}}, 19.2);
tl.fromTo("#s7-shade", {{opacity:0}}, {{opacity:1, duration:0.6, ease:"power2.in"}}, 20.35);

window.__timelines["main"] = tl;
</script>
</body>
</html>'''
out = R+('/reel_local.html' if LOCAL else '/whynot-no-one-leaves-reels.html')
open(out,'w').write(html); print(out, len(html)//1024, 'KB')
