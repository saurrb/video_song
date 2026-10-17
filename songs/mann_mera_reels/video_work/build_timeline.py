from pathlib import Path
from itertools import groupby
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
g={k:list(v) for k,v in groupby(words,key=lambda w:w['line'])}
# Silero voice activity identifies the opening vocal onset at 0.96 seconds.
g[0][0]['start']=.96
# Free-transcription onsets resolve DTW stretching across musical pauses.
for li,t in {2:6.56,3:10.18,4:13.36,5:15.80,6:18.70,7:23.86,8:27.50,9:33.28,10:37.84,11:42.40,12:46.80}.items():
    g[li][0]['start']=t
    if li:g[li-1][-1]['end']=min(g[li-1][-1]['end'],t)
g[12][3]['start']=50.06
# The recording omits 'ko' in 'phone dekha'; ASR omits it and forced token probability is .0116.
assert g[8][2]['text']=='ko'
g[8].pop(2)
g[8][2]['start']=29.80
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=[g[i] for i in range(8)]+[g[8][:4],g[8][4:],g[9][:5],g[9][5:],g[10][:3],g[10][3:],g[11][:4],g[11][4:],g[12][:3],g[12][3:]]
phrases=[]
for i,ws in enumerate(parts):
    next_start=parts[i+1][0]['start'] if i+1<len(parts) else duration
    end=min(next_start,max(w['end'] for w in ws)+.16)
    for w in ws:
        w['end']=min(end,max(w['end'],w['start']+.04))
        assert 0<=w['start']<w['end']<=duration,w
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
starts=[0]+[g[i][0]['start'] for i in range(1,8)]+[g[8][0]['start'],g[8][4]['start'],g[9][0]['start'],g[10][0]['start'],g[10][3]['start'],g[11][0]['start'],g[12][0]['start'],g[12][3]['start']]
images=sorted((ROOT.parent/'portrait_images').glob('*.png'));assert len(images)==16,len(images)
scenes=[{'scene':i+1,'image':p.name,'start':starts[i],'end':starts[i+1] if i<15 else duration} for i,p in enumerate(images)]
assert all(s['end']>s['start'] for s in scenes)
data={'title':'Mann Mera - Reels vs Work','artist':'Hansi Ki Dhun','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small free Hindi ASR and canonical transliterated-word DTW; pauses corrected against independent ASR','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
for p in phrases:print(f"{p['start']:.2f}-{p['end']:.2f}: "+' '.join(w['text'] for w in p['words']))
print('Duration',duration,'Scenes',len(scenes),'Words',sum(len(p['words']) for p in phrases))
