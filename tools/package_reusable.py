"""Package the maintained starter without regenerating or overwriting its content."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
kit=ROOT/'reusable_song_kit'
dest=ROOT/'archives/Hansi_Ki_Dhun_Reusable_Song_Kit.zip'
dest.parent.mkdir(exist_ok=True)
files=[p for p in kit.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in files:archive.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(dest) as archive:
    assert archive.testzip() is None
    assert len(archive.infolist())==len(files)
print('Saved',dest,'with',len(files),'files')
