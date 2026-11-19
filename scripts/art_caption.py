#!/usr/bin/env python3
"""V0.2 original Chinese variety caption art cards; exports transparent PNG + editable JSON."""
import argparse, math, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONTS=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/System/Library/Fonts/PingFang.ttc','C:/Windows/Fonts/msyhbd.ttc','C:/Windows/Fonts/msyh.ttc']
PRESETS={'comic-punch':{'label':'反差爆点','ink':'#25233D','fill':'#FFD46A','accent':'#FF758A','paper':'#FFF5E0'},'field-notes':{'label':'手作生活','ink':'#345D51','fill':'#FFF8E8','accent':'#D76C4D','paper':'#E6ECCF'},'type-clash':{'label':'观点碰撞','ink':'#122C40','fill':'#FFF1C8','accent':'#FF6654','paper':'#8FC9CC'}}

def get_font(size,custom=None):
    for path in ([custom] if custom else [])+FONTS:
        if path and Path(path).is_file():
            try: return ImageFont.truetype(path,size)
            except OSError: pass
    raise SystemExit('没有中文字体。请安装 Noto Sans CJK，或传入 --font。')

def width(draw,line,font):
    box=draw.textbbox((0,0),line,font=font,stroke_width=0)
    return box[2]-box[0]

def wrap(draw,text,font,maxwidth):
    result=[]
    for paragraph in text.split('\n'):
        line=''
        for char in paragraph:
            if line and width(draw,line+char,font)>maxwidth:
                result.append(line);line=char
            else: line+=char
        result.append(line or ' ')
    return result

def draw_text(img,text,frame,fontsize,fill,custom=None,outline=None,stroke=0):
    draw=ImageDraw.Draw(img)
    x0,y0,x1,y1=frame
    while True:
        font=get_font(fontsize,custom)
        lines=wrap(draw,text,font,x1-x0)
        lineheight=int(fontsize*1.18)
        if (len(lines)<=4 and len(lines)*lineheight<=y1-y0) or fontsize<=24: break
        fontsize-=3
    y=y0+((y1-y0)-lineheight*len(lines))//2
    for line in lines:
        x=x0+((x1-x0)-width(draw,line,font))//2
        draw.text((x,y),line,font=font,fill=fill,stroke_width=stroke,stroke_fill=outline)
        y+=lineheight
    return {'font_size':fontsize,'lines':lines}

def render(text,preset,dimensions,subtitle='',fontfile=None):
    W,H=dimensions; c=PRESETS[preset]
    s=min(W/1600,H/900)
    q=lambda n:max(1,round(n*s))
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(img)
    cx,cy=W//2,H//2
    pw,ph=round(min(W*.78,1180*s)),round(min(H*.54,460*s))
    L,T,R,B=cx-pw//2,cy-ph//2,cx+pw//2,cy+ph//2
    if preset=='comic-punch':
        points=[]
        for j in range(40):
            a=-math.pi/2+j*math.pi/20
            scale=1 if j%2 else 1.13
            points.append((cx+int(pw*.57*scale*math.cos(a)),cy+int(ph*.62*scale*math.sin(a))))
        d.polygon(points,fill=c['accent'])
        d.rounded_rectangle((L,T,R,B),radius=q(38),fill=c['paper'],outline=c['ink'],width=q(9))
        d.rounded_rectangle((L+q(15),T+q(15),R-q(15),B-q(15)),radius=q(28),outline=c['fill'],width=q(6))
        info=draw_text(img,text,(L+q(65),T+q(45),R-q(65),B-q(55)),q(120),c['ink'],fontfile,c['fill'],q(3))
        d.arc((R-q(80),T-q(70),R+q(110),T+q(110)),190,340,fill=c['ink'],width=q(9))
    elif preset=='field-notes':
        d.rounded_rectangle((L-q(9),T+q(18),R+q(9),B+q(18)),radius=q(35),fill=c['paper'])
        d.rounded_rectangle((L,T,R,B),radius=q(35),fill=c['fill'],outline=c['ink'],width=q(5))
        d.polygon([(cx-q(150),T-q(18)),(cx+q(120),T-q(30)),(cx+q(135),T+q(34)),(cx-q(140),T+q(42))],fill='#E9D1A4')
        for sign in [-1,1]:
            x=cx+sign*(pw//2-q(35)); y=cy+q(55)
            d.arc((x-q(85),y-q(105),x+q(85),y+q(105)),50 if sign==1 else 130,255 if sign==1 else 320,fill=c['ink'],width=q(4))
            for k in range(3):
                ox=sign*q(15+k*10); oy=q(k*34-35)
                d.ellipse((x+ox-q(19),y+oy-q(11),x+ox+q(19),y+oy+q(11)),fill=c['paper'],outline=c['ink'],width=q(2))
        info=draw_text(img,text,(L+q(80),T+q(55),R-q(80),B-q(55)),q(112),c['ink'],fontfile)
    else:
        d.polygon([(L,T),(R-q(24),T-q(34)),(R,B),(L+q(24),B+q(32))],fill=c['ink'])
        d.rectangle((L+q(28),T+q(32),R-q(28),B-q(32)),outline=c['paper'],width=q(6))
        d.rectangle((L-q(60),T-q(49),L+q(250),T-q(16)),fill=c['accent'])
        d.rectangle((R-q(250),B+q(15),R+q(55),B+q(45)),fill=c['paper'])
        info=draw_text(img,text,(L+q(65),T+q(50),R-q(65),B-q(55)),q(122),c['fill'],fontfile)
    if subtitle:
        f=get_font(q(31),fontfile)
        sw=width(d,subtitle,f); tx=cx-sw//2;ty=min(H-q(43),B+q(77))
        d.rounded_rectangle((tx-q(20),ty-q(7),tx+sw+q(20),ty+q(39)),radius=q(12),fill=c['ink'])
        d.text((tx,ty),subtitle,font=f,fill='#FFFFFF')
    return img,{'preset':preset,'label':c['label'],'text':text,'subtitle':subtitle,'canvas':[W,H],'palette':c,'caption':info,'transparent':True}

def main():
    p=argparse.ArgumentParser(description='原创中文综艺艺术花字：透明 PNG + JSON')
    p.add_argument('--text')
    p.add_argument('--subtitle',default='')
    p.add_argument('--preset',choices=PRESETS,default='comic-punch')
    p.add_argument('--out',default='outputs/caption.png')
    p.add_argument('--size',default='1600x900')
    p.add_argument('--font')
    p.add_argument('--list-presets',action='store_true')
    a=p.parse_args()
    if a.list_presets:
        for key,value in PRESETS.items(): print(key,value['label'])
        return
    if not a.text:p.error('请指定 --text')
    try:
        dims=tuple(map(int,a.size.lower().split('x')))
        if len(dims)!=2 or min(dims)<300 or max(dims)>4096:raise ValueError
    except ValueError:p.error('--size 必须是 1600x900 这样的格式')
    img,meta=render(a.text,a.preset,dims,a.subtitle,a.font)
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    img.save(target)
    target.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Created',target)

if __name__=='__main__':main()
