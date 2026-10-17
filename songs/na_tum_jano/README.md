# ना तुम जानो ना हम

25.65-second Hansi Ki Dhun portrait lyric video with five newly generated illustrations of the approved couple and Hindi kinetic typography. Source audio and supplied lyrics are retained as song.mp3 and lyrics.txt.

- [Final video](final_video/na_tum_jano_1080x1920.mp4)
- [Captions and hashtags](caption_hashtags.txt)
- [Contact sheet](contact_sheet.jpg), [five portraits ZIP](portrait_images_na_tum_jano.zip)
- [Storyboard](storyboard.md), [built-in imagegen prompts](image_prompts.md)
- [Timed subtitles](final_video/lyrics_timed.srt), [verification](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18, AAC 256 kbps. Nine phrases include all 23 supplied words. The local maintained starter adds camera motion, crossfades, glowing word reveals and edge sparkles. Question marks are omitted from animated text; the original supplied text is preserved in lyrics.txt.

Fresh Whisper-small transcription, independent short-line transcription and forced alignment use shared local weights. Recognition is imperfect on the sung roast words, so the supplied wording controls display. Word timing, especially phrase starts across musical pauses, remains model-estimated and has not been certified by a human listening review.

Re-render from workspace root:

```powershell
python -X utf8 songs/na_tum_jano/video_work/build_timeline.py
python -X utf8 songs/na_tum_jano/video_work/render_video.py --name na_tum_jano_1080x1920.mp4
python -X utf8 songs/na_tum_jano/video_work/verify_video.py
```
