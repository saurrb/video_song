from pathlib import Path
import json
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
R=Path(__file__).resolve().parent
m=WhisperModel(str(R.parents[2]/'shared/models/whisper-small'),device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
a=decode_audio(str(R/'song_16k.wav')); out=[]
for lo,hi in [(0,12),(12,24),(24,34.2465)]:
 ss,_=m.transcribe(a[int(lo*16000):int(hi*16000)],language='hi',beam_size=5,word_timestamps=True,condition_on_previous_text=False,temperature=0)
 for s in ss:
  d={'start':lo+s.start,'end':lo+s.end,'text':s.text,'words':[{'start':lo+w.start,'end':lo+w.end,'word':w.word,'probability':w.probability} for w in s.words]};out.append(d);print(json.dumps(d,ensure_ascii=False),flush=True)
(R/'whisper_chunks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')

