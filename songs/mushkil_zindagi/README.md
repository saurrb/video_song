# Mushkil Zindagi — मुश्किल ज़िंदगी

34.09-second Hansi Ki Dhun portrait music video starring only the approved girl character, as requested. Source audio and original lyrics are retained in song.mp3 and lyrics.txt.

- [Final video](final_video/mushkil_zindagi_1080x1920.mp4)
- [Three captions and hashtags](caption_hashtags.txt)
- [Contact sheet](contact_sheet.jpg), [seven portraits ZIP](portrait_images_mushkil_zindagi.zip)
- [Storyboard](storyboard.md), [image prompts](image_prompts.md)
- [Timed subtitles](final_video/lyrics_timed.srt), [verification report](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18, AAC 256 kbps. Seven new girl-only illustrations, thirteen kinetic phrases and all 46 supplied words, including original punctuation. Soft camera motion, short crossfades and gold-to-white word reveals use a local copy of the maintained starter renderer.

Built-in imagegen generated each illustration separately from the retained Hansi Ki Dhun character reference. Earlier songs remain unchanged.

Fresh Whisper-small transcription and forced alignment use the shared local model. Hindi spoken tokens align the exact Roman-script display words. The first transcription had a cut-boundary repetition artifact; forced alignment follows new verse boundaries. A few onsets that absorbed silence were corrected against independent transcription, and final word holds were checked against it. Word timings remain model estimates, not a human listening certification.

Re-render from library root:

```powershell
python -X utf8 songs/mushkil_zindagi/video_work/build_timeline.py
python -X utf8 songs/mushkil_zindagi/video_work/render_video.py --name mushkil_zindagi_1080x1920.mp4
python -X utf8 songs/mushkil_zindagi/video_work/verify_video.py
```
