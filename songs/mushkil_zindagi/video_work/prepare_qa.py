from pathlib import Path
p=Path('songs/mushkil_zindagi/video_work/verify_video.py');s=p.read_text(encoding='utf8').replace('pisa_kaun_bhare_1080x1920.mp4','mushkil_zindagi_1080x1920.mp4').replace("==8","==7").replace("'scenes':8","'scenes':7").replace("actual=[w['text'] for p in data['phrases'] for w in p['words']]","actual=normal_words(' '.join(w['text'] for p in data['phrases'] for w in p['words']))")
p.write_text(s,encoding='utf8')
