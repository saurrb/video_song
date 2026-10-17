from pathlib import Path
import json,subprocess,wave
import cv2,numpy as np
import re
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
VIDEO=ROOT.parent/'final_video'/'palang_ke_andar_yoddha_1080x1920.mp4'
data=json.loads((ROOT/'timeline.json').read_text(encoding='utf-8'))
def normal_words(text):
    return re.sub(r'[^\u0900-\u097fA-Za-z\s-]','',text).replace('-',' ').split()
expected=normal_words((ROOT.parent/'lyrics.txt').read_text(encoding='utf-8'))
actual=[w['text'] for p in data['phrases'] for w in p['words']]
assert actual==expected,(actual,expected)
assert all(0<=w['start']<w['end']<=data['duration'] for p in data['phrases'] for w in p['words'])
assert data['scenes'][0]['start']==0
assert all(abs(a['end']-b['start'])<.001 for a,b in zip(data['scenes'],data['scenes'][1:]))
qa=ROOT/'final_qa';qa.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(VIDEO)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert v['width']==1080 and v['height']==1920
assert abs(float(v['duration'])-data['duration'])<.1
assert abs(float(a['duration'])-data['duration'])<.1
assert len({s['scene'] for s in data['scenes']})==16
cap=cv2.VideoCapture(str(VIDEO))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
checks=[]
for i,p in enumerate(data['phrases']):
    t=min(p['end']-.09,p['words'][-1]['start']+.20)
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();assert ok
    cv2.imwrite(str(qa/f'phrase_{i+1:02d}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,92])
    checks.append((t,Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))))
for start in range(0,len(checks),12):
    sheet=Image.new('RGB',(4*270,3*512),(20,22,32));draw=ImageDraw.Draw(sheet)
    for j,(t,im) in enumerate(checks[start:start+12]):
        x=j%4*270;y=j//4*512;sheet.paste(im.resize((270,480)),(x,y));draw.text((x+8,y+485),f'Line {start+j+1:02d} | {t:.2f}s',font=font,fill='white')
    sheet.save(qa/f'sheet_{start//12+1:02d}.jpg',quality=94)
# Decode EVERY output frame, checking that the export is complete and not corrupt.
cap.release();cap=cv2.VideoCapture(str(VIDEO));count=0;dark=[]
while True:
    ok,f=cap.read()
    if not ok:break
    if f.mean()<1:dark.append(count)
    count+=1
cap.release()
assert count>=int(data['duration']*30)-1
unexpected=[n for n in dark if 5<n<count-10]
assert not unexpected,unexpected
# Validate original song placement after AAC encoding, not just container durations.
wav=qa/'export_audio.wav'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(VIDEO),'-vn','-ac','1','-ar','16000',str(wav)],check=True)
def read_wav(p):
    with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)/32768
src=read_wav(ROOT/'song_16k.wav');dst=read_wav(wav)
audio_checks=[]
for t in [1,10,20,30,36]:
    lo=int(t*16000);n=16000
    x=src[lo:lo+n];y=dst[lo:lo+n]
    correlation=float(np.corrcoef(x,y)[0,1])
    size=32768
    corr=np.fft.irfft(np.fft.rfft(x,size)*np.conj(np.fft.rfft(y,size)),size)
    lags=np.arange(-800,801);lag=int(lags[np.argmax(corr[lags%size])])
    audio_checks.append({'time_seconds':t,'sample_lag':lag,'lag_ms':lag/16,'correlation':correlation})
    assert abs(lag)<=32,(t,lag)
    assert correlation>.9,(t,correlation)
report={'video':str(VIDEO),'width':v['width'],'height':v['height'],'frame_rate':v['avg_frame_rate'],'decoded_frames':count,'audio_duration':a['duration'],'video_duration':v['duration'],'scenes':16,'timeline_shots':len(data['scenes']),'lyric_phrases':len(data['phrases']),'timed_words':sum(len(p['words']) for p in data['phrases']),'unexpected_black_frames':unexpected,'audio_alignment_checks':audio_checks,'note':'Word timestamps are Whisper model estimates, aligned to supplied lyrics; they are not a human listening certification.'}
(ROOT.parent/'final_video'/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)

