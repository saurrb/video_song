from pathlib import Path
import json,re,time
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio,pad_or_trim
from faster_whisper.tokenizer import Tokenizer
ROOT=Path(__file__).resolve().parent
MODEL_DIR=next((p/'shared/models/whisper-small' for p in ROOT.parents if (p/'shared/models/whisper-small/model.bin').is_file()), ROOT/'models/whisper-small')
lines=[s.strip() for s in (ROOT.parent/'lyrics.txt').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
subs={'Saath': 'साथ', 'problem': 'प्रॉब्लम', 'se': 'से', 'bandha': 'बंधा', 'janmo': 'जन्मों', 'ka': 'का', 'ye': 'ये', 'bandhan': 'बंधन', 'Hai': 'है', 'yahan': 'यहाँ', 'par': 'पर', 'roz': 'रोज', 'ek': 'एक', 'na': 'ना', 'nayi': 'नई', 'tension': 'टेंशन', 'Dukh': 'दुख', 'sehna': 'सहना', 'toh': 'तो', 'hai': 'है', 'sukh': 'सुख', 'mera': 'मेरा', 'dushman': 'दुश्मन', 'Milta': 'मिलता', 'koi': 'कोई', 'samasyaon': 'समस्याओं', 'solution': 'सॉल्यूशन', 'Mushkil': 'मुश्किल', 'mushkil': 'मुश्किल', 'Jeevan': 'जीवन', 'ko': 'को', 'bachana': 'बचाना', 'lagta': 'लगता', 'Zindagi': 'जिंदगी', 'achha': 'अच्छा', 'rulana': 'रुलाना'}

canonical=[]
for li,line in enumerate(lines):
    line=re.sub(r'[^\u0900-\u097fA-Za-z0-9\s-]','',line)
    for word in line.split():
        # Treat hyphenated sung nicknames individually, preserving all words.
        for part in word.split('-'):
            if part:canonical.append({'line':li,'text':part,'spoken':subs.get(part,part)})
model=WhisperModel(str(MODEL_DIR),device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
tokenizer=Tokenizer(model.hf_tokenizer,True,task='transcribe',language='hi')
audio=decode_audio(str(ROOT/'song_16k.wav'))
blocks=json.loads((ROOT/'alignment_blocks.json').read_text(encoding='utf-8'))
results=[]
for a,b,first,last in blocks:
    words=[w.copy() for w in canonical if first<=w['line']<=last]
    text=' '+' '.join(w['spoken'] for w in words)
    tokens=tokenizer.encode(text)
    features=model.feature_extractor(audio[int(a*16000):int(b*16000)])
    n=features.shape[-1]
    print('Aligning',first,last,'tokens',len(tokens),'frames',n,flush=True)
    enc=model.encode(pad_or_trim(features))
    aligned=model.find_alignment(tokenizer,[tokens],enc,n)[0]
    # Map decoder tokens back onto exact original word boundaries, including multi-token Hindi words.
    token_cursor=0
    boundaries=[]
    for w in words:
        wt=tokenizer.encode(' '+w['spoken'])
        boundaries.append((token_cursor,token_cursor+len(wt)))
        token_cursor+=len(wt)
    assert token_cursor==len(tokens),(token_cursor,len(tokens))
    token_times=[]
    for item in aligned:
        for _ in item['tokens']:
            token_times.append((float(item['start'])+a,float(item['end'])+a,float(item['probability'])))
    for w,(lo,hi) in zip(words,boundaries):
        span=token_times[lo:hi]
        w.update(start=round(min(v[0] for v in span),3),end=round(max(v[1] for v in span),3),probability=round(float(np.mean([v[2] for v in span])),4))
        results.append(w)
    (ROOT/'aligned_lyrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Completed block',first,last,flush=True)
print('ALIGNMENT COMPLETE',flush=True)




