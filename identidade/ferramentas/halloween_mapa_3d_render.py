import numpy as np, math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
S=os.path.dirname(os.path.abspath(__file__))
W,H=1080,1920; SS=2; FPS=30; DUR=15.0
hexc=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
AMB=hexc('#c4a582'); OSSO=hexc('#efe4d0')
# ---------- cena ----------
ground=[]  # (poly xz list, color)
def gq(x0,z0,x1,z1,c): ground.append(([(x0,z0),(x1,z0),(x1,z1),(x0,z1)],hexc(c)))
gq(-400,-600,1200,2300,'#070504')
gq(30,170,780,303,'#1b1613'); gq(30,303,780,430,'#110c09')
for x in range(40,780,60): gq(x,232,x+34,240,'#5a524a')
gq(381,303,465,430,'#2a2018')
gq(30,430,780,612,'#1c130c'); gq(30,612,207,1005,'#1c130c'); gq(207,612,513,1005,'#2c170b')
ground.append(([(30,1005),(513,1005),(513,1092),(780,1092),(780,1715),(30,1715)],hexc('#1c130c')))
gq(30,1715,780,1800,'#110c09')
faces=[]  # (verts Nx3, color, edge, emissive)
def box(x0,z0,x1,z1,h,c,edge=True,top=None,y0=0,em=False):
    c=hexc(c); t=hexc(top) if top else c
    P=lambda x,y,z:(x,y,z)
    faces.append((np.array([P(x0,y0+h,z0),P(x1,y0+h,z0),P(x1,y0+h,z1),P(x0,y0+h,z1)],float),t,edge,em,(0,1,0)))
    faces.append((np.array([P(x0,y0,z0),P(x1,y0,z0),P(x1,y0+h,z0),P(x0,y0+h,z0)],float),c,edge,False,(0,0,-1)))
    faces.append((np.array([P(x1,y0,z1),P(x0,y0,z1),P(x0,y0+h,z1),P(x1,y0+h,z1)],float),c,edge,False,(0,0,1)))
    faces.append((np.array([P(x0,y0,z1),P(x0,y0,z0),P(x0,y0+h,z0),P(x0,y0+h,z1)],float),c,edge,False,(-1,0,0)))
    faces.append((np.array([P(x1,y0,z0),P(x1,y0,z1),P(x1,y0+h,z1),P(x1,y0+h,z0)],float),c,edge,False,(1,0,0)))
def cyl(cx,cz,r,h,c,top=None,n=16,y0=0,em=False,edge=True):
    c=hexc(c); t=hexc(top) if top else c
    pts=[(cx+r*math.cos(2*math.pi*i/n),cz+r*math.sin(2*math.pi*i/n)) for i in range(n)]
    faces.append((np.array([(x,y0+h,z) for x,z in pts],float),t,edge,em,(0,1,0)))
    for i in range(n):
        (xa,za),(xb,zb)=pts[i],pts[(i+1)%n]; nx,nz=math.cos(2*math.pi*(i+.5)/n),math.sin(2*math.pi*(i+.5)/n)
        faces.append((np.array([(xa,y0,za),(xb,y0,zb),(xb,y0+h,zb),(xa,y0+h,za)],float),c,False,False,(nx,0,nz)))
# muros perimetrais
WALL='#2a1d14'
for (x0,z0,x1,z1) in [(24,430,30,1800),(780,430,786,1800),(30,424,361,430),(445,424,780,430),(30,1712,90,1718),(210,1712,780,1718)]:
    box(x0,z0,x1,z1,40,WALL)
# pórtico de entrada (3 arcos)
for z in (322,362,402):
    box(381,z,389,z+8,125,'#0d0b0a'); box(457,z,465,z+8,125,'#0d0b0a'); box(381,z,465,z+8,10,'#0d0b0a',y0=125,top='#c4a582')
# lounges 1-5
h=(1003-617)/5
for i in range(5):
    y=617+i*h
    box(57,y+4,70,y+h-4,55,'#6b4424',top='#8a5a30')          # painel de madeira
    box(70,y+8,110,y+h-8,14,'#3d2c1f',top='#d8ccb4')          # sofá
    box(130,y+h/2-14,175,y+h/2+14,12,'#7a4a24',top='#a06a36')  # mesa
    box(57,y,207,y+2,6,'#c4a582')                               # divisória
# cozinha / banheiros
box(513,612,780,980,95,'#2e241c',top='#3a2e24'); box(518,993,780,1085,72,'#2e241c',top='#3a2e24')
# bistrôs
for x,z in [(290,690),(430,690),(360,800),(290,910),(430,910)]:
    cyl(x,z,4,42,'#2a1a10',n=8,edge=False); cyl(x,z,16,4,'#7a4a24',top='#b07a40',y0=42,n=16)
# palco
box(220,1352,527,1585,32,'#3a2414',top='#8a6238',em=True)
for (cx,cz) in [(222,1354),(519,1354),(222,1577),(519,1577)]: box(cx,cz,cx+6,cz+6,150,'#1a1512',y0=32)
for (x0,z0,x1,z1) in [(222,1354,525,1360),(222,1577,525,1583),(222,1354,228,1583),(519,1354,525,1583)]: box(x0,z0,x1,z1,6,'#1a1512',y0=182,top='#c4a582')
# lounge 6
cyl(110,1075,54,8,'#3d2c1f',top='#2a1d14',n=24); cyl(110,1075,46,16,'#3d2c1f',top='#d8ccb4',n=24,y0=8)
cyl(110,1075,14,22,'#7a4a24',top='#a06a36',n=12)
# palmeiras
palms=[(60,470),(745,470),(745,1680),(60,1650),(740,1300)]
for px,pz in palms:
    cyl(px,pz,5,170,'#3b2a1c',n=6,edge=False)
    for k in range(7):
        a=2*math.pi*k/7; L=70
        tip=(px+L*math.cos(a),150,pz+L*math.sin(a)); l=(px+12*math.cos(a+1.2),172,pz+12*math.sin(a+1.2)); r=(px+12*math.cos(a-1.2),172,pz+12*math.sin(a-1.2))
        faces.append((np.array([(px,175,pz),l,tip,r],float),hexc('#2f3a1c'),False,False,(0,1,0)))
# varais de luz
bulbs=[]
for (a,b) in [((30,1150),(780,1210)),((30,1250),(780,1310)),((30,500),(780,540)),((207,700),(513,700)),((207,900),(513,900))]:
    for k in range(26):
        t=k/25; x=a[0]+(b[0]-a[0])*t; z=a[1]+(b[1]-a[1])*t; y=120-30*math.sin(math.pi*t)
        bulbs.append((x,y,z))
# labels (nome, x,y,z, t_in, t_out, escala base)
LB=[('avenida',405,8,236,0.4,4.0,1.0),('entrada',423,150,365,1.6,5.0,1.0),('externa',405,8,521,2.6,6.0,.9),
    ('pista',360,10,760,4.6,9.0,1.1),('bistros',360,60,965,5.2,9.0,.85),('lounges',132,70,600,5.4,9.0,1.0),
    ('cozinha',646,110,796,5.0,9.0,.9),('banheiros',649,90,1039,6.5,10.5,.9),('lounge6',110,40,1075,8.5,15,1.0),
    ('palco',373,60,1468,8.6,15,1.0),('entrada2',145,8,1745,10.5,15,.9)]
for n in range(1,6): LB.append((f'n{n}',132,70,617+(n-.5)*h,5.0,9.5,.9))
spr={k:Image.open(f'{S}/lbl/{k}.png').convert('RGBA') for k in set([l[0] for l in LB]+['title','logo'])}
# ---------- câmera ----------
K=[(0.0,(405,950,-420),(405,0,560)),(3.0,(423,330,230),(423,0,760)),(6.0,(360,400,520),(360,0,1020)),
   (9.0,(150,900,980),(373,0,1470)),(11.5,(780,980,1220),(373,0,1460)),(14.2,(405,1950,1180),(405,0,960)),(15.0,(405,1960,1185),(405,0,960))]
def ease(u): return u*u*(3-2*u)
def cr(p0,p1,p2,p3,t):
    p0,p1,p2,p3=map(np.array,(p0,p1,p2,p3)); return 0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3)
def cam_at(t):
    for i in range(len(K)-1):
        if K[i][0]<=t<=K[i+1][0]: break
    u=ease((t-K[i][0])/(K[i+1][0]-K[i][0]))
    g=lambda j,idx: K[max(0,min(len(K)-1,j))][idx]
    return cr(g(i-1,1),g(i,1),g(i+1,1),g(i+2,1),u), cr(g(i-1,2),g(i,2),g(i+1,2),g(i+2,2),u)
FOV=math.radians(58); f=(H*SS/2)/math.tan(FOV/2)
def view(pos,tgt):
    fwd=np.array(tgt,float)-pos; fwd/=np.linalg.norm(fwd); up=np.array([0,1,0.0])
    if abs(fwd@up)>0.98: up=np.array([0,0,1.0])
    rt=np.cross(fwd,up); rt/=np.linalg.norm(rt); u2=np.cross(rt,fwd)
    return np.stack([rt,u2,fwd]),pos
NEAR=8
def clip(cs):
    out=[]; n=len(cs)
    for i in range(n):
        a,b=cs[i],cs[(i+1)%n]; ina,inb=a[2]>NEAR,b[2]>NEAR
        if ina: out.append(a)
        if ina!=inb:
            t=(NEAR-a[2])/(b[2]-a[2]); out.append(a+(b-a)*t)
    return out
def proj(c): return (W*SS/2+c[0]/c[2]*f, H*SS/2-c[1]/c[2]*f)
LIGHT=np.array([-0.4,0.8,-0.45]); LIGHT/=np.linalg.norm(LIGHT)
def shade(col,n,em):
    if em: return col
    k=0.55+0.45*max(0,np.dot(n,LIGHT)); return tuple(int(min(255,c*k)) for c in col)
def frame(t):
    pos,tgt=cam_at(t); R,P=view(np.array(pos,float),tgt)
    img=Image.new('RGB',(W*SS,H*SS),(7,5,4)); d=ImageDraw.Draw(img)
    for poly,col in ground:
        cs=[R@(np.array([x,0,z],float)-P) for x,z in poly]; cs=clip(cs)
        if len(cs)>=3: d.polygon([proj(c) for c in cs],fill=col)
    L=[]
    for V,col,edge,em,n in faces:
        ctr=V.mean(0)
        if np.dot(np.array(n),P-ctr)<=0 and n!=(0,1,0) or (n==(0,1,0) and P[1]<ctr[1]): continue
        cs=[R@(v-P) for v in V]; cs=clip(cs)
        if len(cs)<3: continue
        L.append((np.mean([c[2] for c in cs]),[proj(c) for c in cs],shade(col,np.array(n),em),edge))
    L.sort(key=lambda x:-x[0])
    for _,pts,col,edge in L:
        d.polygon(pts,fill=col)
        if edge: d.line(pts+[pts[0]],fill=(150,118,84),width=SS*2)
    # luzes
    glow=Image.new('RGB',(W*SS,H*SS),(0,0,0)); gd=ImageDraw.Draw(glow)
    for b in bulbs:
        c=R@(np.array(b)-P)
        if c[2]>NEAR:
            x,y=proj(c); r=max(2,int(9*SS*300/c[2]))
            gd.ellipse((x-r,y-r,x+r,y+r),fill=(255,190,110))
    pc=R@(np.array([373,40,1468.0])-P)
    if pc[2]>NEAR:
        x,y=proj(pc); r=min(int(130*SS*600/pc[2]),240*SS); gd.ellipse((x-r,y-r*0.6,x+r,y+r*0.6),fill=(110,50,18))
    glow=glow.filter(ImageFilter.GaussianBlur(14*SS)); img=ImageChops.screen(img,glow)
    for b in bulbs:
        c=R@(np.array(b)-P)
        if c[2]>NEAR:
            x,y=proj(c); r=max(1,int(3*SS*300/c[2])); d2=ImageDraw.Draw(img); d2.ellipse((x-r,y-r,x+r,y+r),fill=(255,226,170))
    img=img.resize((W,H),Image.LANCZOS).convert('RGBA')
    # labels
    for k,x,y,z,ti,to,sc in LB:
        a=min(1,(t-ti)/0.5,(to-t)/0.5)
        if a<=0: continue
        c=R@(np.array([x,y,z],float)-P)
        if c[2]<=40: continue
        sx,sy=proj(c); sx/=SS; sy/=SS; s=sc*min(1.1,max(0.28,520/c[2]))*0.5
        sp=spr[k]; im=sp.resize((max(1,int(sp.width*s)),max(1,int(sp.height*s))),Image.LANCZOS)
        al=im.split()[3].point(lambda v:int(v*a)); im.putalpha(al)
        img.alpha_composite(im,(int(sx-im.width/2),int(sy-im.height/2)))
    lg=spr['logo']; img.alpha_composite(lg,((W-lg.width)//2,110))
    a=max(0,min(1,(t-0.3)/0.6,(3.2-t)/0.6))
    if a>0:
        ti=spr['title'].copy(); ti.putalpha(ti.split()[3].point(lambda v:int(v*a))); img.alpha_composite(ti,((W-ti.width)//2,250))
    return img.convert('RGB')
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for i in range(a,b):
        frame(i/FPS).save(f'{S}/frames/f{i:04d}.png')
