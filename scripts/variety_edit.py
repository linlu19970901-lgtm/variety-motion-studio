#!/usr/bin/env python3
"""剪辑 JSON → MP4：正常、变速、定格、重复回放、PNG 贴片。需要 ffmpeg/ffprobe。"""
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-2200:])
    return p.stdout

def probe(p):
    d=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    return float(d['format']['duration']),v['width']//2*2,v['height']//2*2,any(s['codec_type']=='audio' for s in d['streams'])

def atempo(s):
    out=[]
    while s>2:out.append('atempo=2');s/=2
    while s<.5:out.append('atempo=0.5');s/=.5
    out.append('atempo='+str(s))
    return ','.join(out)

def export(plan,output,root):
    source=Path(plan['source']).expanduser()
    source=(source if source.is_absolute() else root/source).resolve()
    duration,w,h,audio=probe(source)
    fps=int(plan.get('fps',30)); clips=plan['clips']
    if not 10<=fps<=60 or not clips:raise ValueError('fps or clips invalid')
    output=Path(output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    cursor=0.;edl=[]
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);parts=[]
        for i,c in enumerate(clips):
            kind=c['type'];start=float(c['start']);speed=float(c.get('speed',1))
            if start<0 or start>=duration:raise ValueError('Invalid start')
            if kind=='freeze':
                d=float(c.get('hold',.6))
                if not .1<=d<=5:raise ValueError('hold out of range')
                vf=f'trim=start={start}:duration={1/fps},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d},trim=duration={d},fps={fps},scale={w}:{h}'
                useaudio=False
            elif kind in ('normal','speed','replay'):
                end=float(c['end'])
                if end<=start or end>duration+.03 or not .25<=speed<=8:raise ValueError('Invalid end/speed')
                d=(end-start)/speed
                vf=f'trim=start={start}:end={end},setpts=(PTS-STARTPTS)/{speed},fps={fps},scale={w}:{h}'
                useaudio=audio
            else:raise ValueError('Unknown clip type')
            path=tmp/f'{i:03d}.mp4'
            cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
            if useaudio:
                af=f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,{atempo(speed)}'
                cmd+=['-filter_complex',f'[0:v]{vf}[v];[0:a]{af}[a]','-map','[v]','-map','[a]']
            else:
                cmd+=['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-filter_complex',f'[0:v]{vf}[v]','-map','[v]','-map','1:a','-shortest']
            cmd+=['-t',str(d),'-r',str(fps),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','20','-c:a','aac','-ar','48000','-ac','2',str(path)]
            run(cmd);parts.append(path)
            edl.append({'type':kind,'source_start':start,'source_end':c.get('end',start),'timeline_start':round(cursor,3),'timeline_end':round(cursor+d,3),'note':c.get('note','')})
            cursor+=d
        listfile=tmp/'concat.txt'
        listfile.write_text(''.join("file '"+str(x)+"'\n" for x in parts),encoding='utf-8')
        base=tmp/'joined.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listfile),'-c','copy',str(base)])
        overlays=plan.get('overlays',[])
        if overlays:
            cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base)];filters=[];prev='[0:v]'
            for j,o in enumerate(overlays):
                asset=Path(o['file']);asset=(asset if asset.is_absolute() else root/asset).resolve()
                if not asset.is_file():raise FileNotFoundError(asset)
                st,ed=float(o['start']),float(o['end'])
                if st<0 or ed<=st or ed>cursor+.1:raise ValueError('Overlay time invalid')
                scale,x,y=float(o.get('scale',.5)),float(o.get('x',.5)),float(o.get('y',.7))
                if not .05<=scale<=1 or not 0<=x<=1 or not 0<=y<=1:raise ValueError('Overlay geometry invalid')
                cmd+=['-loop','1','-framerate',str(fps),'-i',str(asset)]
                filters.append(f'[{j+1}:v]format=rgba,scale={int(w*scale)}:-1[p{j}]')
                filters.append(f"{prev}[p{j}]overlay=x=(W-w)*{x}:y=(H-h)*{y}:enable='between(t,{st},{ed})':format=auto[v{j}]")
                prev=f'[v{j}]'
            cmd+=['-filter_complex',';'.join(filters),'-map',prev,'-map','0:a?','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-t',str(cursor),str(output)]
            run(cmd)
        else:shutil.copyfile(base,output)
    meta={'source':str(source),'duration':round(cursor,3),'fps':fps,'clips':edl,'overlays':overlays,'limitation':'Timecodes and overlays are manually specified. No automated video understanding.'}
    output.with_suffix('.edit.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Created',output)
    return meta

def main():
    p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--out',default='outputs/variety_edit.mp4');a=p.parse_args()
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):p.error('Please install ffmpeg and ffprobe')
    plan_path=Path(a.plan).resolve()
    export(json.loads(plan_path.read_text(encoding='utf-8')),a.out,plan_path.parent.parent)
if __name__=='__main__':main()
