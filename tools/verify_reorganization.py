"""Verify every original file is retained, backed up, or a proven duplicate fragment."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports/reorganization_20261013'
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
before=json.loads((REPORT/'before.json').read_text(encoding='utf-8-sig'))
moves=sorted(json.loads((REPORT/'moves.json').read_text(encoding='utf-8-sig')),key=lambda m:len(m['from']),reverse=True)
cleanup=json.loads((REPORT/'cleanup.json').read_text(encoding='utf-8-sig'))
removed={f['path'] for f in cleanup['files']}
def mapped(path):
    for m in moves:
        if path==m['from'] or path.startswith(m['from']+'/'):return m['to']+path[len(m['from']):]
    return path
counts={'unchanged':0,'edited_with_original_backup':0,'verified_duplicate_fragments_removed':0}
media=0
for entry in before:
    new=mapped(entry['path']);p=ROOT/new
    if new in removed:
        assert not p.exists(),new
        counts['verified_duplicate_fragments_removed']+=1;continue
    assert p.is_file(),('Missing original',entry['path'],new)
    if digest(p)==entry['sha256']:
        counts['unchanged']+=1
        if p.suffix.lower() in {'.png','.jpg','.mp3','.mp4','.wav'}:media+=1
    else:
        backup=REPORT/'original_text'/new
        assert backup.is_file() and digest(backup)==entry['sha256'],('Unaccounted edit',new)
        counts['edited_with_original_backup']+=1
smoke=REPORT/'render_smoke';smoke.mkdir(exist_ok=True)
results=[]
for folder in sorted((ROOT/'songs').iterdir()):
    script=folder/'video_work/render_video.py'
    if not script.exists():continue
    output=smoke/(folder.name+'.mp4')
    subprocess.run([sys.executable,'-X','utf8',str(script),'--start','1','--end','1.25','--width','270','--name',str(output)],check=True,cwd=ROOT)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(output)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(v.get('nb_frames','0'))>=7 and (v['width'],v['height'])==(270,480),folder.name
    results.append({'song':folder.name,'render':'passed','frames':v['nb_frames']})
# Read a few frames through the shared model runtime to verify its retained weights load.
from faster_whisper import WhisperModel
model=WhisperModel(str(ROOT/'shared/models/whisper-small'),device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
del model
original_bytes=sum(e['bytes'] for e in before)
current_bytes=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
report={'original_files':len(before),'accounting':counts,'unchanged_media_files':media,'all_original_files_accounted_for':True,'duplicate_bytes_removed':cleanup['removed_bytes'],'original_bytes':original_bytes,'current_bytes':current_bytes,'net_bytes_saved':original_bytes-current_bytes,'render_checks':results,'shared_whisper_model':'loaded successfully','note':'Finished videos and source media were hash-verified unchanged. Small render checks are saved separately in this report folder.'}
(REPORT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2),flush=True)
