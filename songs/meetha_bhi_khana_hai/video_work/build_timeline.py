from pathlib import Path
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
groups=[[w for w in words if w['line']==i] for i in range(12)]
# Free transcription provides onset anchors across short pauses.
for li,t in [(1,1.12),(2,2.32),(3,4.42),(4,6.94),(5,9.12),(6,11.38),(7,13.90),(11,24.06)]:
    groups[li][0]['start']=t
groups[5][4]['start']=11.06
groups[11][3]['start']=25.44
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=[]
for i,ws in enumerate(groups):
    if i==3:parts.extend([ws[:3],ws[3:]])
    elif i==9:parts.extend([ws[:3],ws[3:]])
    elif i==11:parts.extend([ws[:3],ws[3:]])
    else:parts.append(ws)
phrases=[]
for i,ws in enumerate(parts):
    end=min(parts[i+1][0]['start'] if i+1<len(parts) else duration,ws[-1]['end']+.12)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
prompts=json.loads((ROOT.parent/'scene_prompts.json').read_text(encoding='utf8'))
onsets=[0,1.12,2.32,4.42,6.94,9.12,11.38,13.90,16.14,18.16,21.68,24.06]
scenes=[{'scene':i+1,'image':p['file'],'start':onsets[i],'end':onsets[i+1] if i<11 else duration} for i,p in enumerate(prompts)]
data={'title':'मीठा भी खाना है','artist':'','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small canonical Hindi-word DTW; Hindi phonetic substitutions for displayed English words; independent transcription pause corrections','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved timeline',duration,'seconds;',len(words),'words;',len(phrases),'phrases')
