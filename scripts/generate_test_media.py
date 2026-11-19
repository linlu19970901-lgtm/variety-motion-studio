#!/usr/bin/env python3
"""无版权测试素材：彩色测试视频、透明 PNG 与原创提示音。需要 ffmpeg、Pillow。"""
import math,struct,subprocess,wave
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent.parent
ex=root/'examples';ex.mkdir(parents=True,exist_ok=True)
p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=30','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','6','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(ex/'sample.mp4')],capture_output=True,text=True)
if p.returncode:raise RuntimeError(p.stderr)
im=Image.new('RGBA',(520,130),(0,0,0,0));d=ImageDraw.Draw(im)
d.rounded_rectangle((8,8,510,123),radius=40,fill=(245,188,96,230),outline=(30,42,64,255),width=5)
im.save(ex/'caption.png')
with wave.open(str(ex/'original-pop.wav'),'wb') as f:
 rate=48000;duration=.18
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
 frames=[]
 for i in range(round(rate*duration)):
  t=i/rate;env=(1-t/duration)**2
  frames.append(struct.pack('<h',int(12000*env*math.sin(2*math.pi*(620-360*t/duration)*t))))
 f.writeframes(b''.join(frames))
print('Generated sample media in examples/')
