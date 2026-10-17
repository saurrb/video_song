from pathlib import Path
p=Path('songs/besharam_paisa/video_work/verify_video.py');s=p.read_text(encoding='utf8').replace('pisa_kaun_bhare_1080x1920.mp4','besharam_paisa_1080x1920.mp4').replace('==8','==6').replace("'scenes':8","'scenes':6").replace('[1,8,16,24,32]','[1,8,15,23,30]');p.write_text(s,encoding='utf8')
