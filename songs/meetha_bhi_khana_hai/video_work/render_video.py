"""Reproducible portrait music-video renderer: image motion + libass kinetic type."""
from pathlib import Path
import argparse, json, math, subprocess, random, sys, time
import cv2
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
OUT=PROJECT/'final_video'
W,H,FPS=1080,1920,30
FONT=ROOT/'fonts'/'NirmalaUI-Bold.ttf'
face=hb.Face(FONT.read_bytes()); font=hb.Font(face)
font.scale=(face.upem,face.upem); hb.ot_font_set_funcs(font)
# ASS font size describes the typographic cell height, not the EM square.
tt=TTFont(FONT)
font_height=tt['hhea'].ascent-tt['hhea'].descent
font_factor=face.upem/font_height

def text_width(text,size):
    buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf)
    return sum(p.x_advance for p in buf.glyph_positions)/face.upem*size*font_factor

def ts(t):
    c=round(max(0,t)*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'

def srt_ts(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def make_ass(data):
    lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 2','ScaledBorderAndShadow: yes','YCbCr Matrix: TV.709','','[V4+ Styles]',
           'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
           'Style: Lyric,Nirmala UI,108,&H00FFFFFF,&H00FFFFFF,&H00231912,&H00231912,-1,0,0,0,100,100,0,0,1,2,0,5,40,40,60,1',
           'Style: Particle,Arial,30,&H00FFFFFF,&H00FFFFFF,&H00D4EF70,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1',
           '','[Events]','Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
    def event(layer,a,b,style,body):
        if b>a: lines.append(f'Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{body}')
    def color(rgb):return '&H'+rgb[4:6]+rgb[2:4]+rgb[0:2]+'&'
    gold=color('FFE18B');cyan=color('76F3E3');white=color('FFFFFF');navy=color('211932')
    for pi,p in enumerate(data['phrases']):
        words=p['words'];size=116
        # Balanced one/two-line layout, measured after Hindi shaping.
        gap=text_width(' ',size)+9
        widths=[text_width(w['text'],size) for w in words]
        total=sum(widths)+gap*(len(words)-1)
        split=None
        if total>880 and len(words)>1:
            split=min(range(1,len(words)),key=lambda k:max(sum(widths[:k])+gap*(k-1),sum(widths[k:])+gap*(len(words)-k-1)))
        rows=[list(range(len(words)))] if split is None else [list(range(split)),list(range(split,len(words)))]
        maxw=max(sum(widths[k] for k in row)+gap*(len(row)-1) for row in rows)
        if maxw>880:
            scale=880/maxw;size*=scale;gap*=scale;widths=[v*scale for v in widths]
        ys=[1570] if len(rows)==1 else [1517,1658]
        p['render_font_size']=round(size,2)
        p['render_rows']=[[words[k]['text'] for k in row] for row in rows]
        for ri,row in enumerate(rows):
            rw=sum(widths[k] for k in row)+gap*(len(row)-1)
            left=(W-rw)/2
            for k in row:
                w=words[k];x=left+widths[k]/2;left+=widths[k]+gap;y=ys[ri]
                a=w['start'];b=p['end'];hold=min(260,max(90,int((w['end']-a)*1000)))
                # Fast initial reveal; newly sung word lights gold then cools to white.
                direction=1 if pi%2==0 else -1
                motion=f'\\move({x:.1f},{y+24:.1f},{x:.1f},{y:.1f},0,135)'
                anim=f'\\fscx116\\fscy116\\t(0,150,\\fscx100\\fscy100)\\blur2\\t(0,125,\\blur0.45)\\fad(28,80)'
                basic=f'\\an5\\fs{size:.2f}{motion}{anim}'
                glow=f'{{{basic}\\bord5\\blur11\\1c{cyan}\\3c{cyan}\\alpha&H78&}}'+w['text']
                event(2,a,b,'Lyric',glow)
                main=f'{{{basic}\\bord2.6\\shad0\\3c{navy}\\1c{gold}\\t({hold},{hold+170},\\1c{white})}}'+w['text']
                event(3,a,b,'Lyric',main)
    # Small four-point stars, concentrated at sides rather than across faces/words.
    rng=random.Random(527)
    dur=data['duration']
    star='m 0 -16 l 4 -4 16 0 4 4 0 16 -4 4 -16 0 -4 -4'
    for i in range(int(dur*4.5)):
        a=i/4.5+rng.uniform(0,0.08);life=rng.uniform(.7,1.4);b=min(a+life,dur)
        x=rng.choice([rng.uniform(35,170),rng.uniform(910,1045)])
        y=rng.uniform(120,1440);sz=rng.uniform(35,85);c=gold if i%3==0 else cyan
        tag=f'\\an5\\move({x:.1f},{y:.1f},{x+10:.1f},{y-60:.1f})\\p1\\bord0\\shad0\\1c{c}\\alpha&H35&\\fscx{sz}\\fscy{sz}\\fad(180,400)\\t(0,280,\\fscx{sz*1.35:.1f}\\fscy{sz*1.35:.1f})\\t(350,{int(life*1000)},\\fscx10\\fscy10)'
        event(1,a,b,'Particle','{'+tag+'}'+star)
    path=ROOT/'kinetic_lyrics.ass';path.write_text('\n'.join(lines),encoding='utf-8-sig')
    sr=[]
    for i,p in enumerate(data['phrases'],1):
        sr.extend([str(i),srt_ts(p['start'])+' --> '+srt_ts(p['end']),' '.join(w['text'] for w in p['words']),''])
    (OUT/'lyrics_timed.srt').write_text('\n'.join(sr),encoding='utf-8-sig')
    (ROOT/'layout_manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return path

def render(data,start,end,width,output):
    height=round(width*16/9);height+=height%2
    images={s['image']:cv2.imread(str(PROJECT/'portrait_images'/s['image'])) for s in data['scenes']}
    scenes=data['scenes']
    # Subtle lower-third scrim preserves the image while providing contrast for glow.
    yy=np.arange(height,dtype=np.float32)/height
    a=.04+.72*np.clip((yy-.64)/.23,0,1)**1.2
    alpha=a[:,None,None]
    tint=np.array([35,21,29],dtype=np.float32)[None,None,:]
    ass=ROOT/'kinetic_lyrics.ass'
    vf=f"setpts=PTS+{start}/TB,ass=filename='video_work/kinetic_lyrics.ass':fontsdir='video_work/fonts':shaping=complex,setpts=PTS-STARTPTS,format=yuv420p"
    frames=math.ceil((end-start)*FPS)
    cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','bgr24','-s',f'{width}x{height}','-r',str(FPS),'-i','pipe:0','-ss',str(start),'-i',str(PROJECT/'song.mp3'),'-map','0:v:0','-map','1:a:0','-vf',vf,'-t',str(end-start),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-metadata','title='+data.get('title','Hansi Ki Dhun'),'-metadata','artist='+data.get('artist','Hansi Ki Dhun'),str(output)]
    log=open(ROOT/(output.stem+'_ffmpeg.log'),'w',encoding='utf-8')
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log,cwd=PROJECT)
    cv2.setNumThreads(2)
    def get_frame(s,t):
        image=images[s['image']];ih,iw=image.shape[:2]
        d=max(.1,s['end']-s['start']);u=np.clip((t-s['start'])/d,0,1)
        ease=u*u*(3-2*u);sid=s['scene']
        if sid%3==0:z=1.085-.065*ease
        else:z=1.02+.07*ease
        if sid==12:z+=.018*math.exp(-u*9)*math.sin(u*24)
        base=max(width/iw,height/ih);scale=base*z
        dx=(width-iw*scale)/2+math.sin(u*math.pi)*width*.012*((sid%2)*2-1)
        dy=(height-ih*scale)/2+(ease-.5)*height*.012
        # Small 103 BPM party sway, confined to the dancing scene.
        if sid==4:
            dx+=width*.006*math.sin((t-s['start'])*2*math.pi*103/60)
            dy+=height*.003*math.sin((t-s['start'])*2*math.pi*103/60)
        matrix=np.array([[scale,0,dx],[0,scale,dy]],np.float32)
        return cv2.warpAffine(image,matrix,(width,height),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    si=0;started=time.time()
    try:
        for fi in range(frames):
            t=start+fi/FPS
            while si<len(scenes)-1 and t>=scenes[si]['end']:si+=1
            frame=get_frame(scenes[si],t)
            offset=t-scenes[si]['start']
            if si>0 and offset<.13:
                f=offset/.13;old=get_frame(scenes[si-1],t)
                frame=cv2.addWeighted(old,1-f,frame,f,0)
            last_lyric=max((p['end'] for p in data['phrases']),default=0)
            opacity=1 if t<last_lyric else max(0,1-(t-last_lyric)/.8)
            actual_alpha=alpha*opacity
            frame=np.clip(frame.astype(np.float32)*(1-actual_alpha)+tint*actual_alpha,0,255).astype(np.uint8)
            # Tiny cinematic fade only at absolute beginning/end, not between words.
            fade=min(1,t/.12,(data['duration']-t)/.5)
            if fade<1:frame=(frame*max(0,fade)).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
            if fi%150==0:
                print(f'{output.name}: {fi}/{frames} frames; time {t:.2f}s; elapsed {time.time()-started:.1f}s',flush=True)
    finally:
        proc.stdin.close()
        ret=proc.wait();log.close()
    if ret:raise RuntimeError(f'FFmpeg failed {ret}; see log')
    print('SAVED '+str(output),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',type=float,default=0);p.add_argument('--end',type=float);p.add_argument('--width',type=int,default=1080);p.add_argument('--name',default='song_1080x1920.mp4');p.add_argument('--ass-only',action='store_true');args=p.parse_args()
    OUT.mkdir(exist_ok=True)
    data=json.loads((ROOT/'timeline.json').read_text(encoding='utf-8'));make_ass(data)
    if not args.ass_only:render(data,args.start,args.end or data['duration'],args.width,OUT/args.name)
