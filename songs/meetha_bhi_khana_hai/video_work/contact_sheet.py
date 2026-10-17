from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
files=sorted((ROOT/'portrait_images').glob('*.png'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for start in range(0,len(files),6):
    sheet=Image.new('RGB',(3*282,2*525),'#202030');draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(files[start:start+6]):
        im=Image.open(p).convert('RGB');im.thumbnail((282,501));x=i%3*282;y=i//3*525
        sheet.paste(im,(x,y));draw.text((x+8,y+503),p.stem,font=font,fill='white')
    sheet.save(ROOT/f'scene_contact_{start//6+1:02d}.jpg',quality=95)
print('Reviewed asset count:',len(files))
