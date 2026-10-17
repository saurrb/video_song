from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;P=R.parent
words=json.loads((R/'aligned_lyrics.json').read_text(encoding='utf8'))
# Resolve leading silence absorbed by forced alignment, using independent transcription onsets.
corrections={(3,0):15.26,(4,0):20.6,(4,1):22.24,(6,0):28.0}
lines=[x.split() for x in (P/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
phrases=[]
for li in range(7):
 ww=[w for w in words if w['line']==li]
 for wi,w in enumerate(ww):
  w['text']=lines[li][wi]
  if (li,wi) in corrections:w['start']=corrections[(li,wi)]
 if li==5:ww[-1]['end']=26.98
 if li==6:ww[-1]['end']=31.96
 split={0:4,1:4,2:4,3:3,5:3,6:3}.get(li)
 groups=[ww[:split],ww[split:]] if split else [ww]
 for g in groups:phrases.append({'start':g[0]['start'],'end':g[-1]['end'],'words':[{'text':w['text'],'start':w['start'],'end':w['end']} for w in g]})
for i,p in enumerate(phrases):
 nxt=phrases[i+1]['start'] if i+1<len(phrases) else 32.2
 p['end']=min(nxt,p['end']+.12)
files=sorted((P/'portrait_images').glob('*.png'))
cues=[(0,0),(4.58,1),(9.5,2),(15.26,3),(20.6,4),(23.78,5),(28.0,6)]
scenes=[{'scene':i+1,'image':files[k].name,'start':a,'end':cues[i+1][0] if i+1<len(cues) else 34.089775} for i,(a,k) in enumerate(cues)]
data={'title':'Mushkil Zindagi — मुश्किल ज़िंदगी','artist':'Hansi Ki Dhun','duration':34.089775,'scenes':scenes,'phrases':phrases,'timing_note':'Fresh Whisper-small forced alignment. Several silence-absorbing starts corrected using independent transcription; original wording and punctuation preserved. Word times are model estimates.'}
(R/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
assert [w['text'] for p in phrases for w in p['words']]==(P/'lyrics.txt').read_text(encoding='utf-8-sig').split()
for p in phrases:assert all(p['start']<=w['start']<w['end']<=p['end']+.001 for w in p['words'])
for a,b in zip(phrases,phrases[1:]):assert a['end']<=b['start']
canvas=Image.new('RGB',(960,900),'#eee6df');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=i%4*240;y=i//4*450;canvas.paste(im,(x,y));d.text((x+5,y+414),f.stem,fill='black')
canvas.save(P/'contact_sheet.jpg')
print(len(words),'words;',len(phrases),'phrases;',len(scenes),'scenes')
