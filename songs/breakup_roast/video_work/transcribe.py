from pathlib import Path
import json,time
from faster_whisper import WhisperModel
ROOT=Path(__file__).resolve().parent
MODEL_DIR=next((p/'shared/models/whisper-small' for p in ROOT.parents if (p/'shared/models/whisper-small/model.bin').is_file()), ROOT/'models/whisper-small')
print('Loading Whisper small multilingual CPU int8',flush=True)
model=WhisperModel(str(MODEL_DIR),device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
prompt=(ROOT.parent/'lyrics.txt').read_text(encoding='utf-8')
segments,info=model.transcribe(str(ROOT/'song_16k.wav'),language='hi',beam_size=5,word_timestamps=True,vad_filter=False,initial_prompt='हिंदी पंजाबी हास्य गीत। याद, नाम, रस्ते, सपना, वर्ल्ड, गालियां, सारियां।',condition_on_previous_text=False,temperature=0)
out=[]
for s in segments:
    item={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in (s.words or [])]}
    out.append(item)
    print(json.dumps(item,ensure_ascii=False),flush=True)
    (ROOT/'whisper_transcript.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('TRANSCRIPTION COMPLETE',flush=True)





