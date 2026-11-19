#!/usr/bin/env python3
"""Convert transparent grid spritesheet into APNG/GIF, optional VP9-alpha WebM."""
import argparse,json,subprocess,shutil
from pathlib import Path
from PIL import Image
def main():
 p=argparse.ArgumentParser()
 p.add_argument('spritesheet',type=Path)
 p.add_argument('--rows',type=int,required=True)
 p.add_argument('--columns',type=int,required=True)
 p.add_argument('--frames',type=int)
 p.add_argument('--duration-ms',type=int,default=150)
 p.add_argument('--out',type=Path,default=Path('outputs/overlay'))
 p.add_argument('--webm',action='store_true')
 a=p.parse_args()
 if a.rows<=0 or a.columns<=0 or not 50<=a.duration_ms<=3000:p.error('invalid grid or frame duration')
 im=Image.open(a.spritesheet).convert('RGBA');w,h=im.size
 if w%a.columns or h%a.rows:p.error('image dimensions must be divisible by grid')
 cw,ch=w//a.columns,h//a.rows;n=a.frames or a.rows*a.columns
 if n<2 or n>a.rows*a.columns:p.error('invalid number of frames')
 frames=[im.crop(((i%a.columns)*cw,(i//a.columns)*ch,((i%a.columns)+1)*cw,((i//a.columns)+1)*ch)) for i in range(n)]
 if not any(f.getchannel('A').getextrema()[0]<255 for f in frames):p.error('No alpha detected; source must be transparent RGBA spritesheet')
 a.out.parent.mkdir(parents=True,exist_ok=True)
 apng=a.out.with_suffix('.png')
 frames[0].save(apng,save_all=True,append_images=frames[1:],duration=a.duration_ms,loop=0,disposal=2,blend=0)
 gif=a.out.with_suffix('.gif')
 frames[0].save(gif,save_all=True,append_images=frames[1:],duration=a.duration_ms,loop=0,disposal=2,transparency=0,optimize=False)
 outputs={'apng':str(apng),'gif':str(gif)}
 if a.webm:
  if not shutil.which('ffmpeg'):p.error('ffmpeg required for WebM')
  seq=a.out.parent/(a.out.name+'_frames');seq.mkdir(parents=True,exist_ok=True)
  for i,frame in enumerate(frames):frame.save(seq/f'{i:04d}.png')
  dest=a.out.with_suffix('.webm')
  c=['ffmpeg','-y','-loglevel','error','-framerate',str(1000/a.duration_ms),'-i',str(seq/'%04d.png'),'-c:v','libvpx-vp9','-pix_fmt','yuva420p','-auto-alt-ref','0',str(dest)]
  r=subprocess.run(c,capture_output=True,text=True)
  if r.returncode:raise RuntimeError(r.stderr)
  outputs['webm']=str(dest)
 meta={'source':str(a.spritesheet),'frames':n,'frame_size':[cw,ch],'duration_ms':a.duration_ms,'has_alpha':True,'outputs':outputs,'compatibility':'Test animated formats in target Jianying; PNG frames are the fallback'}
 a.out.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
