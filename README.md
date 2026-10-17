# Hansi Ki Dhun — Song Library

Open **[library.html](library.html)** to browse and play completed songs, or use the links below.

| Song | Duration | Images | Open |
|---|---:|---:|---|
| Ho Gaya Hu Main Besharam | 31.9s | 6 | [Video](songs/besharam_paisa/final_video/besharam_paisa_1080x1920.mp4) · [Project](songs/besharam_paisa/README.md) |
| याद आ जाए — Breakup Roast | 26.9s | 8 | [Video](songs/breakup_roast/final_video/breakup_roast_1080x1920.mp4) · [Project](songs/breakup_roast/README.md) |
| मेरी hoodie वापस कर दे | 68.4s | 32 | [Video](songs/hoodie_breakup/final_video/hoodie_kinetic_song_1080x1920.mp4) · [Project](songs/hoodie_breakup/README.md) |
| Karzdar — कर्ज़दार | 44.8s | 8 | [Video](songs/karzdar/final_video/karzdar_1080x1920.mp4) · [Project](songs/karzdar/README.md) |
| Aaj Khane Mein Kya Banana Hai | 27.2s | 6 | [Video](songs/kya_banana_hai/final_video/kya_banana_hai_1080x1920.mp4) · [Project](songs/kya_banana_hai/README.md) |
| Mann Mera - Reels vs Work | 54.4s | 16 | [Video](songs/mann_mera_reels/final_video/mann_mera_reels_1080x1920.mp4) · [Project](songs/mann_mera_reels/README.md) |
| मीठा भी खाना है | 27.1s | 12 | [Video](songs/meetha_bhi_khana_hai/final_video/meetha_bhi_khana_hai_1080x1920.mp4) · [Project](songs/meetha_bhi_khana_hai/README.md) |
| Middle Class Life Meri | 23.4s | 8 | [Video](songs/middle_class_life/final_video/middle_class_life_1080x1920.mp4) · [Project](songs/middle_class_life/README.md) |
| Mushkil Zindagi — मुश्किल ज़िंदगी | 34.1s | 7 | [Video](songs/mushkil_zindagi/final_video/mushkil_zindagi_1080x1920.mp4) · [Project](songs/mushkil_zindagi/README.md) |
| ना तुम जानो ना हम | 25.7s | 5 | [Video](songs/na_tum_jano/final_video/na_tum_jano_1080x1920.mp4) · [Project](songs/na_tum_jano/README.md) |
| नहाना चाहिए | 15.0s | 6 | [Video](songs/nahana_chahiye/final_video/nahana_chahiye_1080x1920.mp4) · [Project](songs/nahana_chahiye/README.md) |
| नींद का जादू | 23.6s | 6 | [Video](songs/neend_ka_jadoo/final_video/neend_ka_jadoo_1080x1920.mp4) · [Project](songs/neend_ka_jadoo/README.md) |
| पलंग के अंदर योद्धा | 38.6s | 16 | [Video](songs/palang_ke_andar_yoddha/final_video/palang_ke_andar_yoddha_1080x1920.mp4) · [Project](songs/palang_ke_andar_yoddha/README.md) |
| फिर भी मैं हंसता जाता | 24.7s | 8 | [Video](songs/phir_bhi_hansta/final_video/phir_bhi_hansta_1080x1920.mp4) · [Project](songs/phir_bhi_hansta/README.md) |
| Pisa Kaun Bhare — Food Date Roast | 34.2s | 8 | [Video](songs/pisa_kaun_bhare/final_video/pisa_kaun_bhare_1080x1920.mp4) · [Project](songs/pisa_kaun_bhare/README.md) |

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
