from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent; P=R.parent
words=json.loads((R/'aligned_lyrics.json').read_text(encoding='utf8'))
# Short-block boundary artifacts: trim previous word and use repeatable transcription onset.
for w in words:
 if w['line']==3 and w['text']=='sham': w['end']=15.0
 if w['line']==10 and w['text']=='Karzdar': w['start']=36.7
phrases=[]
for li in range(13):
 ww=[w for w in words if w['line']==li]
 groups=[ww] if len(ww)<=4 else [ww[:3],ww[3:]]
 for group in groups:
  phrases.append({'start':group[0]['start'],'end':group[-1]['end'],'words':[{'text':w['text'],'start':w['start'],'end':w['end']} for w in group]})
for i,p in enumerate(phrases):
 nxt=phrases[i+1]['start'] if i+1<len(phrases) else 43.5
 p['end']=min(nxt,max(p['end'],p['words'][-1]['end']+.1))
files=sorted((P/'portrait_images').glob('*.png'))
# Picture cuts follow lyric events; repeat the borrowing setup for the callback.
cues=[(0,0),(3.74,1),(10.7,2),(15,3),(18.48,4),(22.36,5),(29.8,6),(33.62,5),(36.7,7),(38.44,6),(40.24,7)]
scenes=[{'scene':i+1,'image':files[k].name,'start':a,'end':cues[i+1][0] if i+1<len(cues) else 44.799975} for i,(a,k) in enumerate(cues)]
data={'title':'Karzdar — कर्ज़दार','artist':'Hansi Ki Dhun','duration':44.799975,'scenes':scenes,'phrases':phrases,'timing_note':'Fresh Whisper small forced alignment with canonical Roman-script lyrics and Hindi spoken tokens; section-boundary overlaps corrected. Word times remain model estimates.'}
(R/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
canvas=Image.new('RGB',(960,900),'#eee6df');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=(i%4)*240;y=(i//4)*450;canvas.paste(im,(x,y));d.text((x+5,y+414),f.stem,fill='black')
canvas.save(P/'contact_sheet.jpg')
assert [w['text'] for p in phrases for w in p['words']]==(P/'lyrics.txt').read_text(encoding='utf-8-sig').split()
print('Timeline:',len(scenes),'cuts,',len(phrases),'phrases,',len(words),'words')
