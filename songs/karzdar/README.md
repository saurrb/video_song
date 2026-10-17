# Karzdar — कर्ज़दार

44.8-second Hansi Ki Dhun portrait lyric video using the supplied audio and exact Roman-script lyrics.

- Final: [karzdar_1080x1920.mp4](final_video/karzdar_1080x1920.mp4)
- Eight new illustrations: [contact sheet](contact_sheet.jpg), [images](portrait_images/)
- [Storyboard](storyboard.md), [image prompts](image_prompts.md), [posting caption](caption_hashtags.txt)
- [Timed subtitles](final_video/lyrics_timed.srt), [verification](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18, AAC 256 kbps. Eleven lyric-cued shots, gentle camera motion, short crossfades, word-by-word gold-to-white text and edge sparkles. Original audio retained as song.mp3.

Images were generated separately with the built-in imagegen tool using the retained approved couple reference. The maintained starter renderer was copied into this project. Previous songs were preserved.

Alignment uses shared Whisper-small weights, fresh short-section transcription and forced alignment with Hindi spoken tokens mapped to the supplied Roman-script words. The initial whole-track transcript repeated the hook incorrectly; whisper_chunks.json is the corrected short-section transcription. Timeline construction trims two overlapping block boundaries. Word timings remain model estimates, not a human listening certification.

Re-render from the library root:

```powershell
python -X utf8 songs/karzdar/video_work/build_timeline.py
python -X utf8 songs/karzdar/video_work/render_video.py --name karzdar_1080x1920.mp4
python -X utf8 songs/karzdar/video_work/verify_video.py
```
