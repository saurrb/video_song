# याद आ जाए — Breakup Roast

## Files

- `final_video/breakup_roast_1080x1920.mp4`: full 26.85-second portrait music video.
- `portrait_images/` and `portrait_images_8.zip`: eight separate scene illustrations.
- `storyboard.md`: script and timed scene plan.
- `lyrics.txt`: supplied text, preserved verbatim apart from line breaks.
- `caption_hashtags.txt`: ready-to-post caption and hashtags.
- `scene_prompts.json`: complete built-in imagegen prompts and reference paths.
- `references/couple_reference.png`: retained Hansi Ki Dhun character reference.
- `video_work/timeline.json`: editable scene and word timing.
- `final_video/lyrics_timed.srt`: timed phrase subtitles.
- `final_video/verification.json`: automated export checks.

## Production

1080×1920, 30 fps, H.264 with AAC audio. Original MP3 copied unchanged from the supplied Downloads path; video audio is re-encoded without speed changes. Images were created with built-in imagegen, using the retained couple reference and opening scene to maintain character/style consistency. Gentle image motion, quick crossfades, word reveals, edge sparkles and small comic camera accents are added by the renderer.

Whisper small Hindi transcription and canonical-word alignment provide estimated timestamps. The English display word `world` is aligned using its Hindi pronunciation. Independent transcription identified the 20.82-second start of गालियां after a pause; a cropped final-phrase check supported the timing of the last words. Supplied third-line wording is retained pending any user correction. These timestamps are model estimates, not a human listening certification. Audio sample comparisons check export placement and drift separately from word recognition.

Run from the parent workspace: `python songs/breakup_roast/video_work/render_video.py --name breakup_roast_1080x1920.mp4`. Run `python songs/breakup_roast/video_work/verify_video.py` to inspect export integrity, lyrics coverage, frame count, durations and audio alignment. Alignment scripts reuse the existing library shared/models/whisper-small model.
