# फिर भी मैं हंसता जाता

Girl-led Hansi Ki Dhun comedy music video, 24.71 seconds, eight newly generated portrait illustrations, Hindi–English kinetic lyrics and a laughing finish.

- [Final video](final_video/phir_bhi_hansta_1080x1920.mp4)
- [Eight separate images](portrait_images_8.zip)
- [Storyboard](storyboard.md)
- [Caption and hashtags](caption_hashtags.txt)
- [Exact built-in imagegen prompts](scene_prompts.json)
- [Original lyrics](lyrics.txt)
- [Editable timeline](video_work/timeline.json)
- [Timed subtitles](final_video/lyrics_timed.srt)
- [Export checks](final_video/verification.json)

## Production notes

1080×1920, 30 fps, H.264 with AAC audio. Original MP3 copied from the supplied Downloads path and retained unchanged. The export re-encodes audio without changing speed or placement. All eight images use the saved girl reference; scenes 2–8 also use the opening image to stabilize appearance. Still-image motion, sparkles, dissolves and small laughter pulses are added in the renderer.

Whisper small canonical alignment and independent free-transcription anchors estimate word timing. Musical pauses are respected. Repeated laughter was aligned separately; the supplied six हा syllables are retained, merging an 80 ms initial free-ASR fragment with its neighbor. Word times remain model estimates, not a human listening certification. All supplied lyric wording is preserved, including मुझे पे ले and हंसता जाता. Girl character used as requested.

From the library root, re-render with `python -X utf8 songs/phir_bhi_hansta/video_work/render_video.py --name phir_bhi_hansta_1080x1920.mp4`. Alignment scripts discover `shared/models/whisper-small/` automatically. Refresh the library index with `python -X utf8 tools/song_library.py index` after changes.
