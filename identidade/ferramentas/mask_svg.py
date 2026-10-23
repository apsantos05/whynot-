import os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__))
# máscara original desenhada (traço âmbar + brilho), fundo transparente
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1600" height="896">
<defs>
 <radialGradient id="fill" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#3a1d0c"/><stop offset="1" stop-color="#140a05"/></radialGradient>
 <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g filter="url(#glow)">
<path d="M500 190 C 440 120, 300 70, 170 95 C 90 110, 45 175, 70 255 C 95 340, 175 420, 280 430 C 380 440, 450 380, 500 330 C 550 380, 620 440, 720 430 C 825 420, 905 340, 930 255 C 955 175, 910 110, 830 95 C 700 70, 560 120, 500 190 Z" fill="url(#fill)" stroke="#c4a582" stroke-width="7"/>
<path d="M215 245 C 250 195, 345 185, 400 230 C 375 290, 280 310, 225 285 Z" fill="#0b0706" stroke="#efe4d0" stroke-width="5"/>
<path d="M785 245 C 750 195, 655 185, 600 230 C 625 290, 720 310, 775 285 Z" fill="#0b0706" stroke="#efe4d0" stroke-width="5"/>
<path d="M500 205 C 495 150, 520 90, 560 55" fill="none" stroke="#c4a582" stroke-width="4" opacity=".8"/>
<path d="M120 150 C 160 120, 230 115, 290 130" fill="none" stroke="#c4a582" stroke-width="3" opacity=".6"/>
<path d="M880 150 C 840 120, 770 115, 710 130" fill="none" stroke="#c4a582" stroke-width="3" opacity=".6"/>
<path d="M150 330 C 200 380, 260 400, 320 400" fill="none" stroke="#c4a582" stroke-width="3" opacity=".5"/>
<path d="M850 330 C 800 380, 740 400, 680 400" fill="none" stroke="#c4a582" stroke-width="3" opacity=".5"/>
<circle cx="500" cy="265" r="9" fill="#c4a582"/>
</g>
<path d="M70 255 C 20 250, -10 300, 10 360" fill="none" stroke="#c4a582" stroke-width="3" opacity=".7"/>
<path d="M930 255 C 980 250, 1010 300, 990 360" fill="none" stroke="#c4a582" stroke-width="3" opacity=".7"/>
</svg>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1600,'height':896})
    pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>"); pg.wait_for_timeout(200)
    pg.screenshot(path=S+'/mask_draw.png',omit_background=True); b.close()
print('ok')
