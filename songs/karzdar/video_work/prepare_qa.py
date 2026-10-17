from pathlib import Path
p=Path('songs/karzdar/video_work/verify_video.py')
s=p.read_text(encoding='utf8').replace('breakup_roast_1080x1920.mp4','karzdar_1080x1920.mp4').replace("assert len({s['scene'] for s in data['scenes']})==8","assert len({s['image'] for s in data['scenes']})==8").replace('for t in [1,6,12,18,25]:','for t in [1,12,24,35,42]:')
p.write_text(s,encoding='utf8')
