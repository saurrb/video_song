from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;P=R.parent
words=json.loads((R/'aligned_lyrics.json').read_text(encoding='utf8'))
for w in words:
 if w['line']==2 and w['text']=='Is':w['start']=8.12
 if w['line']==4 and w['text']=='Ham':w['start']=16.42
phrases=[]
for li in range(6):
 ww=[w for w in words if w['line']==li]
 k=4 if li==5 else 3
 for g in [ww[:k],ww[k:]]:
  phrases.append({'start':g[0]['start'],'end':g[-1]['end'],'words':[{'text':w['text'],'start':w['start'],'end':w['end']} for w in g]})
for i,p in enumerate(phrases):
 nxt=phrases[i+1]['start'] if i+1<len(phrases) else 27.245675
 p['end']=min(nxt,p['end']+.12)
files=sorted((P/'portrait_images').glob('*.png'))
cues=[(0,0),(4.04,1),(8.12,2),(12.3,3),(16.42,4),(21.28,5)]
scenes=[{'scene':i+1,'image':files[k].name,'start':a,'end':cues[i+1][0] if i+1<len(cues) else 27.245675} for i,(a,k) in enumerate(cues)]
data={'title':'Aaj Khane Mein Kya Banana Hai','artist':'Hansi Ki Dhun','duration':27.245675,'scenes':scenes,'phrases':phrases,'timing_note':'Fresh Whisper-small forced alignment with supplied lyrics. Repeated hook independently transcribed; overlapping line starts corrected. Word times remain model estimates.'}
(R/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
assert [w['text'] for p in phrases for w in p['words']]==(P/'lyrics.txt').read_text(encoding='utf-8-sig').split()
for p in phrases:assert all(p['start']<=w['start']<w['end']<=p['end']+.001 for w in p['words'])
canvas=Image.new('RGB',(720,900),'#eee6df');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=i%3*240;y=i//3*450;canvas.paste(im,(x,y));d.text((x+5,y+414),f.stem,fill='black')
canvas.save(P/'contact_sheet.jpg');print(len(words),'words;',len(phrases),'phrases;',len(scenes),'scenes')
