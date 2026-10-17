from pathlib import Path
import json
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
ROOT=Path(__file__).resolve().parent
MODEL_DIR=next((p/'shared/models/whisper-small' for p in ROOT.parents if (p/'shared/models/whisper-small/model.bin').is_file()), ROOT/'models/whisper-small')
model=WhisperModel(str(MODEL_DIR),device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
audio=decode_audio(str(ROOT/'song_16k.wav'))
segments,info=model.transcribe(audio[int(18.5*16000):],language='hi',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,temperature=0)
result=[]
for s in segments:
    result.append({'text':s.text,'words':[{'text':w.word,'start':round(w.start+18.5,3),'end':round(w.end+18.5,3),'probability':w.probability} for w in s.words]})
(ROOT/'final_phrase_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
