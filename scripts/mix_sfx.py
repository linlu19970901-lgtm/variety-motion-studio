#!/usr/bin/env python3
"""将用户授权音效按时间码混入已有 MP4，需 ffmpeg。"""
import argparse,json,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('events');p.add_argument('--out',default='outputs/with-sfx.mp4');a=p.parse_args()
 ep=Path(a.events).resolve();events=json.loads(ep.read_text(encoding='utf-8'))
 if not events:p.error('音效事件为空')
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',a.video]
 for e in events:
  sound=Path(e['file']);sound=(sound if sound.is_absolute() else ep.parent.parent/sound).resolve()
  if not sound.is_file():raise FileNotFoundError(str(sound))
  cmd+=['-i',str(sound)]
 filters=['[0:a]volume=1[base]'];labels=['[base]']
 for i,e in enumerate(events,1):
  offset=max(0,round(float(e['at'])*1000));vol=float(e.get('volume',.4))
  if not 0<=vol<=2:raise ValueError('volume must be 0-2')
  filters.append(f'[{i}:a]aresample=48000,volume={vol},adelay={offset}|{offset}[fx{i}]')
  labels.append(f'[fx{i}]')
 filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=first:normalize=0[outa]')
 cmd+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[outa]','-c:v','copy','-c:a','aac','-b:a','192k',str(out)]
 r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-2000:])
 print('Created',out)
if __name__=='__main__':main()
