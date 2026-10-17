# Pisa Kaun Bhare — Food Date Roast

34.2465-second Hansi Ki Dhun portrait music video. Original source audio and the user's exact Roman-script lyrics are retained as song.mp3 and lyrics.txt.

- [Final video](final_video/pisa_kaun_bhare_1080x1920.mp4)
- [Three captions and hashtags](caption_hashtags.txt)
- [Illustration contact sheet](contact_sheet.jpg) and [eight images ZIP](portrait_images_pisa_kaun_bhare.zip)
- [Storyboard](storyboard.md) and [exact image prompts](image_prompts.md)
- [Timed subtitles](final_video/lyrics_timed.srt) and [verification report](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18 and AAC 256 kbps. Eight fresh illustrations, ten lyric-cued shots, twelve kinetic lyric phrases and all 41 supplied words. Gentle zoom/pan, short crossfades, glowing gold-to-white word reveals and edge sparkles use the maintained starter renderer copied into this song folder.

Images were generated individually with built-in imagegen and the retained Hansi Ki Dhun couple reference. Previous song projects were preserved.

Fresh Whisper-small transcription and forced alignment use shared model weights and Hindi spoken tokens mapped onto the supplied Roman text. Both repeated lines are independently timed. A 20ms overlap at 13.4 seconds was trimmed. Word timestamps are model estimates, not a human listening certification.

Re-render from the library root:

```powershell
python -X utf8 songs/pisa_kaun_bhare/video_work/build_timeline.py
python -X utf8 songs/pisa_kaun_bhare/video_work/render_video.py --name pisa_kaun_bhare_1080x1920.mp4
python -X utf8 songs/pisa_kaun_bhare/video_work/verify_video.py
```
