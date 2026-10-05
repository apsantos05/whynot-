import os, sys, asyncio, subprocess, re
sys.argv=['x']; exec(open('render2.py').read().split('async def main')[0])
from playwright.async_api import async_playwright
src=open(os.path.join(SRC,'FlyerStory.dc.html')).read()
html=page_html(src)
CTA='<div id="cta" style="position:absolute;left:0;right:0;top:1700px;text-align:center;z-index:9;font-family:\'Space Mono\';font-weight:700;font-size:30px;letter-spacing:.3em;color:#e4f2f6">GARANTA O SEU NO LINK ↓</div>'
html=html.replace('</body>', CTA+'</body>')
JS=r"""
(() => {
 const root=document.body.firstElementChild; const A=[];
 const add=(el,kf,delay,dur,opt={})=>{ if(!el) return; A.push(el.animate(kf,{delay,duration:dur,fill:'both',easing:opt.e||'cubic-bezier(.2,.8,.2,1)',iterations:opt.it||1,direction:opt.dir||'normal'})); };
 const q=s=>document.querySelector(s); const img=n=>[...document.images].find(i=>i.src.includes(n));
 const spans=[...document.querySelectorAll('span')];
 const top=spans.find(s=>s.textContent.includes('EDIÇÃO 01'));
 add(top,[{opacity:0,transform:'translateY(20px)'},{opacity:1,transform:'none'}],100,700);
 add(q('.extm'),[{opacity:0,transform:'rotate(-24deg) scale(.55)'},{opacity:1,transform:'rotate(-8deg) scale(1)'}],350,900,{e:'cubic-bezier(.3,1.5,.5,1)'});
 add(img('bally_logo'),[{opacity:0,transform:'translateY(16px)'},{opacity:.92,transform:'none'}],1000,700);
 const cl=img('z_coiote').parentElement;
 [...cl.children].filter(c=>c.tagName==='DIV').slice(0,2).forEach((d,i)=>add(d,[{opacity:0},{opacity:1}],1100+i*150,1200,{e:'ease-out'}));
 add(cl,[{transform:'scale(1)'},{transform:'scale(1.045)'}],0,15000,{e:'linear'});
 add(img('z_coiote'),[{opacity:0,transform:'translateY(70px)'},{opacity:1,transform:'none'}],1400,900);
 add(img('y_tom'),[{opacity:0,transform:'translateX(-90px)'},{opacity:1,transform:'none'}],1850,900);
 add(img('z_maka6'),[{opacity:0,transform:'translateX(90px)'},{opacity:1,transform:'none'}],2050,900);
 ['z_maycon','z_mex','z_possani'].forEach((n,i)=>add(img(n),[{opacity:0,transform:'translateY(90px) scale(.96)'},{opacity:1,transform:'none'}],2650+i*220,750,{e:'cubic-bezier(.3,1.35,.5,1)'}));
 add(q('.ext'),[{clipPath:'inset(-40px 100% -40px 0px)',transform:'translateX(-30px)'},{clipPath:'inset(-40px -40px -40px -40px)',transform:'none'}],3700,1000);
 const names=spans.find(s=>s.textContent.includes('MAYCON'));
 add(names,[{opacity:0,letterSpacing:'.5em'},{opacity:1,letterSpacing:'.16em'}],4600,800);
 const date=spans.find(s=>s.textContent.includes('SEX.22H'));
 add(date,[{opacity:0,transform:'translateY(24px)'},{opacity:1,transform:'none'}],5200,600);
 const chips=[...document.querySelectorAll('span')].filter(s=>/OPEN GIN|ANTECIPADOS/.test(s.textContent));
 chips.forEach((c,i)=>add(c,[{opacity:0,transform:'scale(.9)'},{opacity:1,transform:'none'}],5600+i*180,500));
 add(spans.find(s=>s.textContent.includes('ANDALÓ')),[{opacity:0},{opacity:1}],6100,600);
 const cta=q('#cta');
 add(cta,[{opacity:0,transform:'translateY(16px)'},{opacity:1,transform:'none'}],6700,600);
 A.push(cta.animate([{transform:'translateY(0)'},{transform:'translateY(10px)'}],{delay:7300,duration:600,iterations:20,direction:'alternate',easing:'ease-in-out',composite:'add'}));
 A.forEach(a=>a.pause()); window.__A=A;
 window.__seek=t=>{A.forEach(a=>{a.currentTime=t});};
})();
"""
async def main():
    FPS=30; T=15; N=FPS*T
    out=os.path.join(D,'whynot-divulgacao-story.mp4')
    tmp=os.path.join(D,'anim_story.html'); open(tmp,'w').write(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+tmp); await pg.wait_for_timeout(800); await pg.evaluate(JS)
        ff=subprocess.Popen(['ffmpeg','-y','-f','image2pipe','-framerate',str(FPS),'-i','-','-f','lavfi','-t',str(T),'-i','anullsrc=r=44100:cl=stereo','-c:v','libx264','-pix_fmt','yuv420p','-b:v','7M','-preset','medium','-movflags','+faststart','-c:a','aac','-shortest',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for i in range(N):
            await pg.evaluate(f'window.__seek({i*1000/FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg',quality=95))
            if i in (15,45,75,105,135,165,200,449): await pg.screenshot(path=os.path.join(D,f'anim_f{i}.png'))
        ff.stdin.close(); ff.wait(); await b.close()
    print(out)
asyncio.run(main())
