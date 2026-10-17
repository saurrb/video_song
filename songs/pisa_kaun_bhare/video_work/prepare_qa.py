from pathlib import Path
p=Path('songs/pisa_kaun_bhare/video_work/verify_video.py')
s=p.read_text(encoding='utf8').replace('karzdar_1080x1920.mp4','pisa_kaun_bhare_1080x1920.mp4').replace('for t in [1,12,24,35,42]:','for t in [1,8,16,24,32]:')
p.write_text(s,encoding='utf8')
