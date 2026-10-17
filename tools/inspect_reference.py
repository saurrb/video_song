from pathlib import Path
import cv2, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]/'shared/kinetic_reference'
(ROOT/'reference_frames').mkdir(exist_ok=True)
(ROOT/'reference_sheets').mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(ROOT/'text_kinetic_motion.mp4'))
fps=cap.get(cv2.CAP_PROP_FPS)
frames=[]; metrics=[]; prev=None
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
i=0
while True:
    ok,frame=cap.read()
    if not ok: break
    cv2.imwrite(str(ROOT/'reference_frames'/f'{i:04d}.jpg'),frame,[cv2.IMWRITE_JPEG_QUALITY,85])
    small=cv2.resize(frame,(320,180))
    diff=0 if prev is None else float(np.abs(small.astype(float)-prev).mean())
    metrics.append({'frame':i,'time':i/fps,'difference':diff})
    frames.append(Image.fromarray(cv2.cvtColor(small,cv2.COLOR_BGR2RGB)))
    prev=small.astype(float);i+=1
for start in range(0,len(frames),48):
    sheet=Image.new('RGB',(1920,8*204),(30,30,35)); d=ImageDraw.Draw(sheet)
    for j,img in enumerate(frames[start:start+48]):
        x=(j%6)*320;y=(j//6)*204
        sheet.paste(img,(x,y)); d.text((x+5,y+182),f'Frame {start+j:03d} | {(start+j)/fps:.3f}s',font=font,fill='white')
    sheet.save(ROOT/'reference_sheets'/f'sheet_{start//48+1:02d}.jpg',quality=92)
(ROOT/'reference_frames.json').write_text(json.dumps({'fps':fps,'count':i,'frames':metrics},indent=2))
print(json.dumps({'fps':fps,'frames':i,'sheets':(i+47)//48}),flush=True)
