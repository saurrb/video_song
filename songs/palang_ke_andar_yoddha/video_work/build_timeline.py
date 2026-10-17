from pathlib import Path
from itertools import groupby
import json,wave,re
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf-8'))
groups={k:list(v) for k,v in groupby(words,key=lambda w:w['line'])}
# Free-transcription onsets resolve DTW stretching across breaths/instrumental gaps.
anchors={0:.90,1:3.22,2:5.30,4:9.44,5:11.48,6:13.52,8:17.46,10:21.60,12:27.82,14:32.20}
for line,start in anchors.items():
    groups[line][0]['start']=start
    if line:groups[line-1][-1]['end']=min(groups[line-1][-1]['end'],start)
with wave.open(str(ROOT/'song_16k.wav')) as wav:duration=wav.getnframes()/wav.getframerate()
assert list(groups)==list(range(16)),list(groups)
phrases=[]
for line,ws in groups.items():
    next_start=groups[line+1][0]['start'] if line<15 else duration
    end=min(next_start,max(w['end'] for w in ws)+.16)
    for w in ws:
        w['end']=min(end,max(w['end'],w['start']+.04))
        assert 0<=w['start']<w['end']<=duration,w
    phrases.append({'line':line,'start':ws[0]['start'],'end':end,'words':ws})
images=sorted((ROOT.parent/'portrait_images').glob('*.png'))
assert len(images)==16,len(images)
scenes=[{'scene':i+1,'image':im.name,'start':0 if i==0 else phrases[i]['start'],'end':phrases[i+1]['start'] if i<15 else duration,'lyric_line':i} for i,im in enumerate(images)]
assert all(s['end']>s['start'] for s in scenes)
data={'title':'पलंग के अंदर योद्धा','artist':'Hansi Ki Dhun','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small Hindi transcription and canonical-lyric cross-attention DTW word alignment','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for p in phrases:print(f"{p['start']:.2f}-{p['end']:.2f}: "+' '.join(w['text'] for w in p['words']))
print('Duration',duration,'Scenes',len(scenes),'Words',len(words))
