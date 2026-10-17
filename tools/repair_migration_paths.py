"""One-time, backed-up path repair for the October 2026 library move."""
from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports/reorganization_20261013'
if (REPORT/'edited_files.json').exists():
    raise SystemExit('This one-time path repair has already run. See edited_files.json.')
moves=json.loads((REPORT/'moves.json').read_text(encoding='utf-8-sig'))
moves.sort(key=lambda m:len(m['from']),reverse=True)
changed=[]
def write(path,text):
    old=path.read_text(encoding='utf-8-sig') if path.exists() else None
    if old==text:return
    if old is not None:
        rel=path.relative_to(ROOT) if path.is_relative_to(ROOT) else Path('external_skill')/path.name
        backup=REPORT/'original_text'/rel
        backup.parent.mkdir(parents=True,exist_ok=True)
        if not backup.exists():shutil.copy2(path,backup)
    path.write_text(text,encoding='utf8')
    changed.append(str(path))
def replace_absolute(text):
    # Longest old prefix wins; placeholders prevent remapping newly written prefixes.
    replacements={}
    for i,m in enumerate(moves):
        for j,sep in enumerate(['/','\\']):
            old=str(ROOT/m['from']).replace('\\',sep)
            new=str(ROOT/m['to']).replace('\\',sep)
            marker=f'__LIBRARY_PATH_{i}_{j}__'
            if old in text:
                text=text.replace(old,marker);replacements[marker]=new
    for marker,value in replacements.items():text=text.replace(marker,value)
    return text
def walk(value):
    if isinstance(value,str):return replace_absolute(value)
    if isinstance(value,list):return [walk(v) for v in value]
    if isinstance(value,dict):return {k:walk(v) for k,v in value.items()}
    return value
for top in ['songs','reusable_song_kit','shared/branding','shared/characters','shared/kinetic_reference']:
    for p in (ROOT/top).rglob('*'):
        if p.suffix not in ['.py','.md','.txt','.json'] or not p.is_file():continue
        text=p.read_text(encoding='utf-8-sig')
        if p.suffix=='.json':
            before=json.loads(text);after=walk(before)
            if before!=after:write(p,json.dumps(after,ensure_ascii=False,indent=2)+'\n')
            continue
        text=replace_absolute(text)
        if p.suffix=='.py' and 'WhisperModel(str(' in text:
            text=re.sub(r'WhisperModel\(str\([^\n]+?\),device=', 'WhisperModel(str(MODEL_DIR),device=',text)
            rootline=next(l for l in text.splitlines() if l.startswith('ROOT='))
            text=text.replace(rootline,rootline+"\nMODEL_DIR=next((p/'shared/models/whisper-small' for p in ROOT.parents if (p/'shared/models/whisper-small/model.bin').is_file()), ROOT/'models/whisper-small')",1)
        if p.suffix in ['.md','.txt']:
            text=text.replace("parent project's video_work/models/whisper-small",'library shared/models/whisper-small')
            text=text.replace('parent workspace Whisper small model','library shared/models/whisper-small model')
            text=text.replace("parent workspace's Whisper small model",'library shared/models/whisper-small model')
            for song in (ROOT/'songs').iterdir():
                text=text.replace('python '+song.name+'/','python songs/'+song.name+'/')
            if p==ROOT/'songs/hoodie_breakup/final_video/README.txt':
                text=text.replace('../video_work/reference_analysis.md','../../../shared/kinetic_reference/reference_analysis.md')
        write(p,text)
p=ROOT/'tools/download_whisper.py'
text=p.read_text(encoding='utf8').replace("Path(__file__).resolve().parent/'models'/'whisper-small'","Path(__file__).resolve().parents[1]/'shared/models/whisper-small'")
write(p,text)
p=ROOT/'tools/inspect_reference.py'
text=p.read_text(encoding='utf8').replace("ROOT=Path(__file__).resolve().parent","ROOT=Path(__file__).resolve().parents[1]/'shared/kinetic_reference'\n(ROOT/'reference_frames').mkdir(exist_ok=True)\n(ROOT/'reference_sheets').mkdir(exist_ok=True)").replace("ROOT.parent/'text_kinetic_motion.mp4'","ROOT/'text_kinetic_motion.mp4'")
write(p,text)
p=ROOT/'reusable_song_kit/README.md'
text=p.read_text(encoding='utf8').replace('Copy starter/ into a NEW song folder.','Create new projects under songs/<song_name>/, or use `python tools/song_library.py new <song_name> --audio <path> --lyrics <lyrics_file>`. This copies starter/ into a new song folder.')
text=text.replace('The original full video, audio, 32 PNGs and kinetic reference stay in the parent project.','The original hoodie video, audio and 32 PNGs are in songs/hoodie_breakup/. Shared character samples and branding are in shared/characters/ and shared/branding/. The kinetic reference and its analysis are in shared/kinetic_reference/.')
write(p,text)
# Keep the user's saved personal workflow in sync; no UI metadata or identity changes.
skill=Path.home()/'.codex/skills/artifact-template-hansi-ki-dhun-song-visuals'
p=skill/'SKILL.md'
text=p.read_text(encoding='utf8')
note='\n\nWorkspace layout: create new projects in `C:/Users/Saurabh/Documents/video_song/songs/<song_name>/`. Read the workspace `README.md` for current navigation. Shared Whisper weights are in `shared/models/whisper-small`; character samples are in `shared/characters`; branding is in `shared/branding`. The workspace `reusable_song_kit` remains the maintained starter. The workspace helper `tools/song_library.py new` scaffolds a song without reusing an old timeline.\n'
if 'Workspace layout: create new projects' not in text:write(p,text.rstrip()+note)
p=skill/'assets/song-kit/README.md'
text=p.read_text(encoding='utf8')
text=text.replace('video_song/video_work/models/whisper-small','video_song/shared/models/whisper-small')
text=text.replace('Copy starter/ into a NEW song folder.','Copy starter/ into a NEW songs/<song_name>/ folder in the workspace. Consult the workspace README.md for the current library layout; the maintained workspace kit is reusable_song_kit/.')
write(p,text)
(REPORT/'edited_files.json').write_text(json.dumps(changed,indent=2),encoding='utf8')
print('Updated',len(changed),'files; originals saved in',REPORT/'original_text')
