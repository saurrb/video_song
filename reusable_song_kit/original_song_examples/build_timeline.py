from pathlib import Path
import json,wave
from itertools import groupby
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf-8'))
groups={k:list(v) for k,v in groupby(words,key=lambda w:w['line'])}
# Resolve overlap caused by the 120 ms context included around each alignment block.
# These anchors are independently recovered by the free Whisper transcription.
for li,start in [(9,19.22),(21,34.44),(33,48.46),(37,54.54)]:
    groups[li][0]['start']=start
    if li-1 in groups:groups[li-1][-1]['end']=min(groups[li-1][-1]['end'],start)
# Preserve final sung/reverberant repetition of 'tu' on screen.
groups[37][-1]['end']=57.02
phrases=[]
for li,ws in groups.items():
    end=ws[-1]['end']
    if li+1 in groups:end=min(max(end,groups[li+1][0]['start']),groups[li+1][0]['start'])
    else:end=57.22
    for w in ws:
        w['end']=max(w['start']+.04,min(w['end'],end))
    phrases.append({'line':li,'start':ws[0]['start'],'end':end,'words':ws})
# Every scene is cued from the onset of its corresponding lyric, not equal durations.
mapping=[(1,0),(2,1),(3,2),(4,3),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,23),(22,24),(23,25),(24,26),(25,27),(26,28),(27,29),(28,31),(29,33),(30,35),(31,36),(32,37)]
images={int(p.name.split('_')[0]):p.name for p in (ROOT.parent/'portrait_images').glob('*.png')}
scenes=[{'scene':n,'image':images[n],'start':groups[li][0]['start'],'lyric_line':li} for n,li in mapping]
scenes[0]['start']=0
# Musical coda: callbacks and final hoodie tableau, without inventing sung lyrics.
scenes.extend([{'scene':31,'image':images[31],'start':58.2,'outro':True},{'scene':26,'image':images[26],'start':60.6,'outro':True},{'scene':20,'image':images[20],'start':63.0,'outro':True},{'scene':32,'image':images[32],'start':65.4,'outro':True}])
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
for i,s in enumerate(scenes):s['end']=scenes[i+1]['start'] if i+1<len(scenes) else duration
assert set(s['scene'] for s in scenes)==set(range(1,33))
assert all(s['end']>s['start'] for s in scenes)
assert all(p['end']>p['start'] for p in phrases)
timeline={'duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'faster-whisper small multilingual: free transcription plus DTW alignment to supplied lyrics; 20 ms alignment grid','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
for s in scenes:print(f"{s['start']:6.2f} - {s['end']:6.2f}   {s['image']}")
print('Words:',sum(len(p['words']) for p in phrases),'Duration:',duration)
