from pathlib import Path
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
groups=[[w for w in words if w['line']==i] for i in range(4)]
# Full free transcription identifies the isolated final vocal after an instrumental pause.
gali=next(w for w in groups[3] if w['text']=='गालियां')
gali['start']=20.82
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
bas=next(i for i,w in enumerate(groups[2]) if w['text']=='बस')
parts=[groups[0][:4],groups[0][4:7],groups[0][7:],groups[1][:4],groups[1][4:8],groups[1][8:],groups[2][:bas],groups[2][bas:],groups[3][:4],groups[3][4:6],groups[3][6:]]
phrases=[]
for i,ws in enumerate(parts):
    end=min(parts[i+1][0]['start'] if i+1<len(parts) else duration,ws[-1]['end']+.12)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
prompts=json.loads((ROOT.parent/'scene_prompts.json').read_text(encoding='utf8'))
onsets=[0,groups[0][7]['start'],groups[1][0]['start'],groups[1][6]['start'],groups[2][0]['start'],groups[2][bas]['start'],groups[3][0]['start'],groups[3][6]['start']]
scenes=[{'scene':i+1,'image':p['file'],'start':onsets[i],'end':onsets[i+1] if i<7 else duration} for i,p in enumerate(prompts)]
data={'title':'याद आ जाए — Breakup Roast','artist':'','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small Hindi canonical-word DTW with original wording preserved and independent final-phrase pause correction; word timing remains estimated','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved timeline:',duration,'seconds,',len(words),'words,',len(phrases),'phrases')
