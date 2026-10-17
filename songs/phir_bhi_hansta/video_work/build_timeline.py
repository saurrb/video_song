from pathlib import Path
import json,wave
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'aligned_lyrics.json').read_text(encoding='utf8'))
groups=[[w for w in words if w['line']==i] for i in range(8)]
# Independent transcription prevents DTW stretching words across musical pauses.
for li,t in [(1,3.46),(2,6.4),(3,9.22),(4,12.54),(5,15.54),(6,18.58)]:groups[li][0]['start']=t
for li,t in [(0,2.72),(1,5.8),(2,8.5),(3,11.58),(4,15.18),(5,18.26),(6,21.1)]:groups[li][-1]['end']=t
# Free ASR split the first laugh into two adjacent fragments (one only 80 ms).
# Merge those fragments and retain the supplied six laughs with model-estimated cues.
laugh_onsets=[21.58,21.86,22.44,22.62,22.92,23.08]
for i,w in enumerate(groups[7]):
    w['start']=laugh_onsets[i];w['end']=laugh_onsets[i+1] if i<5 else 23.66
with wave.open(str(ROOT/'song_16k.wav')) as w:duration=w.getnframes()/w.getframerate()
parts=groups[:7]+[groups[7][:3],groups[7][3:]]
phrases=[]
for i,ws in enumerate(parts):
    end=min(parts[i+1][0]['start'] if i+1<len(parts) else duration,ws[-1]['end']+.14)
    phrases.append({'line':i,'start':ws[0]['start'],'end':end,'words':ws})
prompts=json.loads((ROOT.parent/'scene_prompts.json').read_text(encoding='utf8'))
onsets=[0]+[groups[i][0]['start'] for i in range(1,8)]
scenes=[{'scene':i+1,'image':p['file'],'start':onsets[i],'end':onsets[i+1] if i<7 else duration} for i,p in enumerate(prompts)]
data={'title':'फिर भी मैं हंसता जाता','artist':'','duration':duration,'fps':30,'width':1080,'height':1920,'alignment':'Whisper small canonical Hindi alignment with independent ASR pause anchors; six supplied laughter syllables retained by merging initial short ASR fragment','phrases':phrases,'scenes':scenes}
(ROOT/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved timeline',duration,'seconds;',len(words),'words;',len(phrases),'phrases')
