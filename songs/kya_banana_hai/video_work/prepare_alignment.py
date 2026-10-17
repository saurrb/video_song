from pathlib import Path
import json
R=Path('songs/kya_banana_hai/video_work');p=R/'align_lyrics.py';s=p.read_text(encoding='utf8')
spoken='सबसे मुश्किल तो ये बताना है\nआज खाने में क्या बनाना है\nइस मुश्किल में ये जमाना है\nआज खाने में क्या बनाना है\nहम सोचते कुछ और हैं\nऔर पकता घर में कुछ और है'
lines=[x for x in (R.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()];subs={}
for a,b in zip(lines,spoken.splitlines()):
 assert len(a.split())==len(b.split()),(a,b)
 subs.update(zip(a.split(),b.split()))
s=s.replace("subs={'world':'वर्ल्ड'}",'subs='+repr(subs)).replace("encoding='utf-8').splitlines()","encoding='utf-8-sig').splitlines()")
p.write_text(s,encoding='utf8');(R/'alignment_blocks.json').write_text(json.dumps([[0,8.3,0,1],[8.1,16.6,2,3],[16.3,27.245675,4,5]]),encoding='utf8')
s=(R/'transcribe.py').read_text(encoding='utf-8-sig').replace('[(0,13.8),(13.8,27.245675)]','[(12.1,21.5)]').replace('whisper_chunks.json','whisper_middle.json');(R/'transcribe_middle.py').write_text(s,encoding='utf8')
