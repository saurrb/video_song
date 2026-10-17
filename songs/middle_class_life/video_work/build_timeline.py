from pathlib import Path
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
groups=[[w for w in words if w['line']==i] for i in range(10)]
# Independent free transcription supplies pause boundaries; canonical alignment supplies within-line timing.
for li,t in [(1,2.34),(2,4.28),(3,5.96),(4,8.22),(5,12.12),(6,14.04),(7,15.98),(8,17.30),(9,19.82)]:
    groups[li][0]['start']=t
for li,t in [(0,1.94),(1,4.12),(2,5.9),(3,7.92),(5,13.66),(6,15.88),(9,22.8)]:
    groups[li][-1]['end']=t
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=groups[:4]+[groups[4][:3],groups[4][3:]]+groups[5:9]+[groups[9][:3],groups[9][3:]]
phrases=[]
for i,ws in enumerate(parts):
    end=min(parts[i+1][0]['start'] if i+1<len(parts) else duration,ws[-1]['end']+.12)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
prompts=json.loads((ROOT.parent/'scene_prompts.json').read_text(encoding='utf8'))
onsets=[0,4.28,5.96,8.22,12.12,15.98,19.82,21.4]
scenes=[{'scene':i+1,'image':p['file'],'start':onsets[i],'end':onsets[i+1] if i+1<len(onsets) else duration} for i,p in enumerate(prompts)]
data={'title':'Middle Class Life Meri','artist':'Hansi Ki Dhun','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Fresh Whisper small Hindi phonetic canonical alignment with independent ASR pause anchors. Romanized and Hindi display words preserved. Word cues remain model estimates.','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved',duration,'seconds,',len(words),'words,',len(phrases),'phrases')
