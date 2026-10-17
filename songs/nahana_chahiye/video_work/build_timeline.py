from pathlib import Path
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
groups=[[w for w in words if w['line']==i] for i in range(4)]
# Independent free ASR onsets remove DTW stretching over comic pauses.
for i,t in [(1,4.52),(2,7.70),(3,11.68)]:groups[i][0]['start']=t
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=[groups[0],groups[1],groups[2][:4],groups[2][4:],groups[3]]
phrases=[]
for i,ws in enumerate(parts):
    next_start=parts[i+1][0]['start'] if i+1<len(parts) else duration
    end=min(next_start,ws[-1]['end']+.16)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
onsets=[0,4.52,7.70,8.70,13.40,14.30]
images=sorted((ROOT.parent/'portrait_images').glob('*.png'));assert len(images)==6
scenes=[{'scene':i+1,'image':p.name,'start':onsets[i],'end':onsets[i+1] if i<5 else duration} for i,p in enumerate(images)]
data={'title':'नहाना चाहिए','artist':'','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small Hindi transcription and canonical-word DTW; independent onset corrections for pauses','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(data,ensure_ascii=False,indent=2))
