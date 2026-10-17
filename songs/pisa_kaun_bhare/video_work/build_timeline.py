from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;P=R.parent
words=json.loads((R/'aligned_lyrics.json').read_text(encoding='utf8'))
for w in words:
 if w['line']==3 and w['text']=='aati':w['end']=13.4
phrases=[]
for li in range(10):
 ww=[w for w in words if w['line']==li]
 groups=[ww] if len(ww)<=4 else [ww[:3],ww[3:]]
 for g in groups:phrases.append({'start':g[0]['start'],'end':g[-1]['end'],'words':[{'text':w['text'],'start':w['start'],'end':w['end']} for w in g]})
for i,p in enumerate(phrases):
 nxt=phrases[i+1]['start'] if i+1<len(phrases) else 33.75
 p['end']=min(nxt,p['end']+.1)
files=sorted((P/'portrait_images').glob('*.png'))
cues=[(0,0),(3.22,1),(6.64,2),(10.12,2),(13.4,3),(17.5,4),(20.54,5),(23.9,6),(27.16,7),(30.2,7)]
scenes=[{'scene':i+1,'image':files[k].name,'start':a,'end':cues[i+1][0] if i+1<len(cues) else 34.2465} for i,(a,k) in enumerate(cues)]
data={'title':'Pisa Kaun Bhare — Food Date Roast','artist':'Hansi Ki Dhun','duration':34.2465,'scenes':scenes,'phrases':phrases,'timing_note':'Fresh Whisper small forced alignment against supplied Roman-script lyrics via Hindi spoken tokens. Trimmed 20ms overlap at 13.4 seconds. Word times remain model estimates.'}
(R/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
assert [w['text'] for p in phrases for w in p['words']]==(P/'lyrics.txt').read_text(encoding='utf-8-sig').split()
for p in phrases:assert all(p['start']<=w['start']<w['end']<=p['end']+.001 for w in p['words'])
canvas=Image.new('RGB',(960,900),'#eee6df');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=i%4*240;y=i//4*450;canvas.paste(im,(x,y));d.text((x+5,y+414),f.stem,fill='black')
canvas.save(P/'contact_sheet.jpg')
print(len(words),'words;',len(phrases),'phrases;',len(scenes),'shots')
