from pathlib import Path
import json
R=Path('songs/karzdar/video_work'); d=json.loads((R/'timeline.json').read_text(encoding='utf8'))
manifest=json.loads((R/'layout_manifest.json').read_text(encoding='utf8'))
for p in d['phrases']:
 assert p['start'] < p['end']
 assert all(p['start']<=w['start']<w['end']<=p['end']+.001 for w in p['words'])
for a,b in zip(d['phrases'],d['phrases'][1:]): assert a['end']<=b['start']+.001
print('All words match supplied lyrics; phrase boundaries are positive and non-overlapping.')
print('Font sizes:', min(p['render_font_size'] for p in manifest['phrases']), 'to',max(p['render_font_size'] for p in manifest['phrases']))
print('Rows:', max(len(p['render_rows']) for p in manifest['phrases']))
print('Duration:', d['duration'], 'Last lyric:', d['phrases'][-1]['end'])
