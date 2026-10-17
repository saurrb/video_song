from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent.parent
files=sorted((root/'portrait_images').glob('*.png'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for start in range(0,len(files),8):
    sheet=Image.new('RGB',(4*235,2*450),(30,30,40));draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(files[start:start+8]):
        im=Image.open(p).convert('RGB');im.thumbnail((235,418))
        x=i%4*235;y=i//4*450;sheet.paste(im,(x,y))
        draw.text((x+5,y+422),p.stem,font=font,fill='white')
    sheet.save(root/f'scene_contact_{start//8+1:02d}.jpg',quality=94)
print(len(files),'images')
