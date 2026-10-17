"""Local song catalogue, project scaffold and integrity checks. No network needed."""
from pathlib import Path
import argparse,ast,html,json,re,shutil,subprocess
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]

def rel(path):return Path(path).relative_to(ROOT).as_posix()
def catalogue():
    records=[]
    for folder in sorted((ROOT/'songs').iterdir()):
        timeline=folder/'video_work/timeline.json'
        if not timeline.exists():continue
        data=json.loads(timeline.read_text(encoding='utf-8-sig'))
        report=folder/'final_video/verification.json'
        verification=json.loads(report.read_text(encoding='utf-8-sig')) if report.exists() else {}
        video=Path(verification['video']) if verification.get('video') else next((folder/'final_video').glob('*1080x1920.mp4'),None)
        images=sorted((folder/'portrait_images').glob('*.png'))
        title=data.get('title') or ('मेरी hoodie वापस कर दे' if folder.name=='hoodie_breakup' else folder.name)
        record={'slug':folder.name,'title':title,'folder':rel(folder),'duration':data['duration'],'images':len(images),'video':rel(video) if video else None,'poster':rel(images[0]) if images else None,'zip':next((rel(p) for p in folder.glob('portrait_images_*.zip')),None),'caption':rel(folder/'caption_hashtags.txt') if (folder/'caption_hashtags.txt').exists() else None,'storyboard':rel(folder/'storyboard.md') if (folder/'storyboard.md').exists() else None}
        records.append(record)
    return records

def index():
    records=catalogue()
    (ROOT/'library.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    rows=[];cards=[]
    for r in records:
        title=html.escape(r['title']);path=quote(r['video'] or r['folder'])
        rows.append(f"| {r['title']} | {r['duration']:.1f}s | {r['images']} | [Video]({r['video']}) · [Project]({r['folder']}/README.md) |")
        links=[f'<a href="{path}">Play video ↗</a>']
        for key,label in [('zip','Images ZIP'),('caption','Caption'),('storyboard','Storyboard')]:
            if r[key]:links.append(f'<a href="{quote(r[key])}">{label}</a>')
        cards.append(f'<article data-search="{html.escape(r["title"]+" "+r["slug"],quote=True)}"><video controls preload="none" poster="{quote(r["poster"] or "")}" src="{path}" aria-label="{title}"></video><div class="info"><h2>{title}</h2><p>{r["duration"]:.1f} seconds · {r["images"]} scenes · Portrait HD</p><nav>{"".join(links)}</nav></div></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hansi Ki Dhun · Song Library</title><style>
    *{box-sizing:border-box}body{margin:0;background:#161821;color:#f8f2eb;font-family:Segoe UI,Nirmala UI,sans-serif}main{max-width:1280px;margin:auto;padding:40px 26px}header{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap}small{color:#eab895;letter-spacing:.15em}h1{font-size:38px;margin:10px 0}header p{color:#bdbdc9;margin:0 0 22px}input{padding:13px 18px;border:1px solid #52505e;border-radius:12px;background:#232631;color:white;font:inherit;width:280px;margin-bottom:22px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px}article{background:#242631;border:1px solid #3a3b48;border-radius:18px;overflow:hidden}video{display:block;width:100%;height:350px;object-fit:contain;background:#10121a}.info{padding:18px}h2{font-size:20px;margin:0 0 10px}.info p{font-size:13px;color:#bbbcca}nav{display:flex;gap:8px;flex-wrap:wrap}a{color:#ffcfb2;text-decoration:none;border:1px solid #61504a;border-radius:8px;padding:7px 10px;font-size:13px}a:hover{background:#443d41}footer{color:#aaa;margin-top:28px;font-size:13px}[hidden]{display:none}body>main>p a{border:0;padding:0}</style><main><header><div><small>HANSI KI DHUN</small><h1>Your song library</h1><p>__COUNT__ finished songs · __IMAGES__ separate illustrations</p></div><input type="search" placeholder="Find a song…" aria-label="Find a song"></header><section>__CARDS__</section><footer>Local library · original audio, images and finished videos retained. Open README.md for folder navigation and production instructions.</footer></main><script>document.querySelector('input').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('article').forEach(c=>c.hidden=!c.dataset.search.toLowerCase().includes(q))});</script></html>'''
    page=page.replace('__COUNT__',str(len(records))).replace('__IMAGES__',str(sum(r['images'] for r in records))).replace('__CARDS__',''.join(cards))
    (ROOT/'library.html').write_text(page,encoding='utf8')
    readme='''# Hansi Ki Dhun — Song Library

Open **[library.html](library.html)** to browse and play completed songs, or use the links below.

| Song | Duration | Images | Open |
|---|---:|---:|---|
'''+ '\n'.join(rows)+'''

## Folder layout

- `songs/` — one self-contained production folder per song, including source audio, lyrics, images, render scripts and final video.
- `shared/characters/` — approved character reference and original sample variants.
- `shared/branding/` — Facebook display picture, cover and page notes.
- `shared/models/whisper-small/` — the single shared speech-alignment model.
- `shared/kinetic_reference/` — original typography reference video, all inspected frames and analysis.
- `reusable_song_kit/` — maintained starter and worked examples for future songs.
- `tools/` — library, packaging, model-download and reference-inspection helpers.
- `archives/` — previous reusable-kit ZIP and current portable kit ZIP.
- `reports/reorganization_20261013/` — old-to-new paths, original checksums, cleanup proof, edited-file backups and validation results.

Each song retains `song.mp3`, `lyrics.txt`, `portrait_images/`, `video_work/` and `final_video/`. Some songs also have a storyboard, caption, contact sheets, and an image ZIP. Existing finished media has not been re-encoded.

## Start the next song

From this folder, run:

```powershell
python -X utf8 tools/song_library.py new my_new_song --audio "C:/path/song.mp3" --lyrics "C:/path/lyrics.txt"
```

This creates `songs/my_new_song/` from the starter without overwriting an existing song. Then plan scenes, generate new images, align the new lyrics and create a fresh timeline. Do not reuse old song timestamps.

Useful commands:

```powershell
python -X utf8 tools/song_library.py index
python -X utf8 tools/song_library.py check
python -X utf8 tools/package_reusable.py
```

To re-render a song, use its existing script, for example:

```powershell
python -X utf8 songs/breakup_roast/video_work/render_video.py --name breakup_roast_1080x1920.mp4
```

Python dependencies are listed in `reusable_song_kit/starter/requirements.txt`; FFmpeg must be on PATH. Alignment scripts locate the shared model by walking up to this library. Each song keeps its local font copy so its renderer remains portable. Keep the full library when transferring projects that need speech alignment, or supply the Whisper model on the other machine.

The reorganization removed only verified duplicate model-download fragments. All original song audio, final videos, images, previews, and reference frames were retained. Old chat links may point to the previous locations; `library.html` and `library.json` contain the current locations.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf8')
    print('Indexed',len(records),'songs and',sum(r['images'] for r in records),'images')

def check():
    from PIL import Image
    records=catalogue();checked=[]
    for r in records:
        folder=ROOT/r['folder'];data=json.loads((folder/'video_work/timeline.json').read_text(encoding='utf8'))
        assert (folder/'song.mp3').is_file(),r['slug']
        assert (folder/'video_work/fonts/NirmalaUI-Bold.ttf').is_file(),r['slug']
        assert data['scenes'][0]['start']==0,r['slug']
        assert abs(data['scenes'][-1]['end']-data['duration'])<.01,r['slug']
        for a,b in zip(data['scenes'],data['scenes'][1:]):assert abs(a['end']-b['start'])<.01,r['slug']
        for s in data['scenes']:
            with Image.open(folder/'portrait_images'/s['image']) as im:im.verify()
        for p in data['phrases']:
            assert 0<=p['start']<p['end']<=data['duration']+.01,(r['slug'],p)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(ROOT/r['video'])]))
        v=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert (v['width'],v['height'])==(1080,1920),r['slug']
        assert abs(float(v['duration'])-data['duration'])<.1,r['slug']
        checked.append({'song':r['slug'],'images':r['images'],'video':r['video'],'status':'passed'})
    for top in ['songs','tools','reusable_song_kit']:
        for p in (ROOT/top).rglob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
    assert (ROOT/'shared/models/whisper-small/model.bin').stat().st_size==483546902
    dest=ROOT/'reports/library_check.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(checked,indent=2),encoding='utf8')
    print(json.dumps(checked,indent=2))

def new_song(args):
    if not re.fullmatch(r'[a-z][a-z0-9_\-]{0,63}',args.name):raise ValueError('Use a lowercase name with letters, digits, underscores or hyphens.')
    if args.name.upper() in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}:raise ValueError('Reserved Windows name')
    audio=Path(args.audio).resolve();lyrics=Path(args.lyrics).resolve()
    if not audio.is_file() or not lyrics.is_file():raise FileNotFoundError('Audio and lyrics must both exist.')
    if audio.suffix.lower()!='.mp3':raise ValueError('Use an MP3 source for this starter.')
    dest=ROOT/'songs'/args.name
    if dest.exists():raise FileExistsError(dest)
    shutil.copytree(ROOT/'reusable_song_kit/starter',dest)
    shutil.copy2(audio,dest/'song.mp3');shutil.copy2(lyrics,dest/'lyrics.txt')
    (dest/'references').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'shared/characters/approved_reference.png',dest/'references/couple_reference.png')
    (dest/'README.md').write_text('# '+args.name+'\n\nNew project. Add a storyboard, newly generated portraits and a new aligned timeline before rendering. See ../../README.md.\n',encoding='utf8')
    print('Created',dest)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('index');sub.add_parser('check')
    p=sub.add_parser('new');p.add_argument('name');p.add_argument('--audio',required=True);p.add_argument('--lyrics',required=True)
    args=parser.parse_args()
    {'index':index,'check':check,'new':lambda:new_song(args)}[args.command]()
