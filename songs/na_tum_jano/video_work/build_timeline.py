from pathlib import Path
import json,re
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;P=R.parent
words=json.loads((R/'aligned_lyrics.json').read_text(encoding='utf8'))
phrases=[]
for li in range(5):
 ww=[w for w in words if w['line']==li]
 groups=[ww] if li==2 else [ww[:3],ww[3:]]
 for g in groups:
  phrases.append({'start':g[0]['start'],'end':g[-1]['end']+.18,'words':[{'text':w['text'],'start':w['start'],'end':w['end']} for w in g]})
for i,p in enumerate(phrases):
 if i+1<len(phrases):p['end']=min(p['end'],phrases[i+1]['start'])
files=sorted((P/'portrait_images').glob('*.png'))
cues=[0]+[next(w['start'] for w in words if w['line']==li) for li in range(1,5)]+[25.6522]
scenes=[{'scene':i+1,'image':f.name,'start':cues[i],'end':cues[i+1]} for i,f in enumerate(files)]
data={'title':'ना तुम जानो ना हम','artist':'Hansi Ki Dhun','duration':25.6522,'scenes':scenes,'phrases':phrases,'timing_note':'Fresh Whisper-small transcription and line-level forced alignment to supplied Hindi lyrics. Independent line transcriptions retained. Timestamps are model estimates, including phrase starts across musical pauses.'}
(R/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
expected=re.sub(r'[^\u0900-\u097fA-Za-z0-9\s-]','',(P/'lyrics.txt').read_text(encoding='utf-8-sig')).split()
assert [w['text'] for p in phrases for w in p['words']]==expected
assert all(w['start']<w['end'] for w in words)
canvas=Image.new('RGB',(720,900),'#eee6df');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=i%3*240;y=i//3*450;canvas.paste(im,(x,y));d.text((x+5,y+414),f.stem,fill='black')
canvas.save(P/'contact_sheet.jpg')
print(len(words),'words;',len(phrases),'phrases;',len(scenes),'scenes')
