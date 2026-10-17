from pathlib import Path
import json
R=Path('songs/besharam_paisa/video_work');p=R/'align_lyrics.py';s=p.read_text(encoding='utf8')
spoken='अब जिंदगी में रंग नहीं वैसा\nक्योंकि आता नहीं है ज्यादा पैसा\nमहंगाई दिन पे दिन बढ़ती जा रही\nकर्जे में जिंदगी पिसती जा रही\nकाम नहीं होता दिन रात सोता\nहो गया हूँ मैं बेशरम'
lines=[x for x in (R.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()];subs={}
for a,b in zip(lines,spoken.splitlines()):
 assert len(a.split())==len(b.split()),(a,b)
 subs.update(zip(a.split(),b.split()))
s=s.replace("subs={'world':'वर्ल्ड'}",'subs='+repr(subs)).replace("encoding='utf-8').splitlines()","encoding='utf-8-sig').splitlines()")
p.write_text(s,encoding='utf8')
(R/'alignment_blocks.json').write_text(json.dumps([[0,11.1,0,1],[10.8,22.3,2,3],[22.0,31.895475,4,5]]),encoding='utf8')
p=R/'transcribe_section.py';s=(R/'transcribe.py').read_text(encoding='utf-8-sig').replace('[(0,11),(11,22),(22,31.895475)]','[(10.2,17.0)]').replace('whisper_chunks.json','whisper_inflation.json');p.write_text(s,encoding='utf8')
