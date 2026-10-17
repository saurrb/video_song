from pathlib import Path
import json,wave
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
# Independent free-transcription onsets correct forced-alignment pauses.
for i,t in [(3,3.04),(6,5.86),(9,8.0),(15,14.88),(18,18.32)]:words[i]['start']=t
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=[words[:3],words[3:6],words[6:9],words[9:12],words[12:15],words[15:18],words[18:21],words[21:]]
phrases=[]
for i,ws in enumerate(parts):
    end=min(parts[i+1][0]['start'] if i+1<len(parts) else duration,ws[-1]['end']+.15)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
onsets=[0,3.04,8.0,12.14,18.32,22.48]
images=sorted((ROOT.parent/'portrait_images').glob('*.png'));assert len(images)==6
scenes=[{'scene':i+1,'image':p.name,'start':onsets[i],'end':onsets[i+1] if i<5 else duration} for i,p in enumerate(images)]
data={'title':'नींद का जादू','artist':'','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small Hindi canonical word DTW with independent ASR pause corrections; estimated word times','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
sheet=Image.new('RGB',(3*282,2*525),'#202030');draw=ImageDraw.Draw(sheet)
for i,p in enumerate(images):
    im=Image.open(p).convert('RGB');im.thumbnail((282,501));x=i%3*282;y=i//3*525
    sheet.paste(im,(x,y));draw.text((x+8,y+503),p.stem,fill='white')
sheet.save(ROOT.parent/'scene_contact.jpg',quality=95)
print('Timeline and contact sheet ready',duration)
