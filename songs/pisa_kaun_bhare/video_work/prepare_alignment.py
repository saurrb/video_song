from pathlib import Path
import json
R=Path('songs/pisa_kaun_bhare/video_work');p=R/'align_lyrics.py'
s=p.read_text(encoding='utf8')
spoken='ना तू सावल फूल कस्तूरी\nतू तो होरी भैंसिया पूरी\nजहाँ जाती चर आती\nजहाँ जाती चर आती\nऊपर से लेवे डकार\nसूते सारा माल\nतेरी टेढ़ी मेढ़ी चाल\nखाने को करे बवाल\nतेरा पीसा कौन भरे\nइतना पीसा कौन भरे'
lines=[x for x in (R.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
subs={}
for a,b in zip(lines,spoken.splitlines()):
 assert len(a.split())==len(b.split()),(a,b)
 subs.update(zip(a.split(),b.split()))
s=s.replace("subs={'world':'वर्ल्ड'}",'subs='+repr(subs)).replace("encoding='utf-8').splitlines()","encoding='utf-8-sig').splitlines()")
p.write_text(s,encoding='utf8')
(R/'alignment_blocks.json').write_text(json.dumps([[0,13.6,0,3],[13.4,24,4,6],[23.9,34.2465,7,9]]),encoding='utf8')
