from pathlib import Path
import json
R=Path('songs/karzdar/video_work')
p=R/'align_lyrics.py'
s=p.read_text(encoding='utf8')
spoken='चारो तरफ का मुझपे है करजा\nकरजो की डायरी में मेरा नाम\nकरजो से भरी सुबह मेरी\nकरजो में डूबी है मेरी शाम\nये जिंदगानी अच्छी लगे\nकरजो से मुझको डरना लगे\nकरजे उठाना फिर ना चुकाना\nबस यही मेरा कुसूर\nकरजो से मैं कभी डरता नहीं\nवापस मैं करजे कभी करता नहीं\nकरजदार मैं करजदार\nकरजदार मैं करजदार\nकरजदार मैं करजदार करजदार'
lines=[x for x in (R.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
subs={}
for a,b in zip(lines,spoken.splitlines()):
 assert len(a.split())==len(b.split()),(a,b)
 subs.update(zip(a.split(),b.split()))
s=s.replace("subs={'world':'वर्ल्ड'}",'subs='+repr(subs)).replace("encoding='utf-8').splitlines()","encoding='utf-8-sig').splitlines()")
p.write_text(s,encoding='utf8')
(R/'alignment_blocks.json').write_text(json.dumps([[0,15.15,0,3],[15.0,29.9,4,7],[29.8,36.72,8,9],[36.5,44.799,10,12]]),encoding='utf8')
