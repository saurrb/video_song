from pathlib import Path
import json,re
R=Path('songs/mushkil_zindagi/video_work');p=R/'align_lyrics.py';s=p.read_text(encoding='utf8')
spoken='साथ प्रॉब्लम से बंधा जन्मों का ये बंधन\nहै यहाँ पर रोज एक ना एक नई टेंशन\nदुख सहना तो है सुख ये मेरा तो दुश्मन\nमिलता ना कोई समस्याओं का सॉल्यूशन\nमुश्किल मुश्किल मुश्किल\nजीवन को बचाना लगता है\nजिंदगी को अच्छा रुलाना लगता है'
lines=[x for x in (R.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()];subs={}
for a,b in zip(lines,spoken.splitlines()):
 a=re.sub(r'[^A-Za-z0-9\s-]','',a)
 assert len(a.split())==len(b.split()),(a,b)
 subs.update(zip(a.split(),b.split()))
s=s.replace("subs={'world':'वर्ल्ड'}",'subs='+repr(subs)).replace("encoding='utf-8').splitlines()","encoding='utf-8-sig').splitlines()")
p.write_text(s,encoding='utf8')
(R/'alignment_blocks.json').write_text(json.dumps([[0,9.8,0,1],[9.5,20.1,2,3],[20.1,27.7,4,5],[27.7,34.089775,6,6]]),encoding='utf8')
