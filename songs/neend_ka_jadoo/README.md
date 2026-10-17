# नींद का जादू — finished song project

- Final video: final_video/neend_ka_jadoo_1080x1920.mp4
- Six separate portrait illustrations: portrait_images/ and portrait_images_6.zip
- Script: storyboard.md
- Original supplied lyrics: lyrics.txt
- Posting text: caption_hashtags.txt
- Exact generation prompts: scene_prompts.json (built-in imagegen)
- Editable scene/word timing: video_work/timeline.json
- Subtitle export: final_video/lyrics_timed.srt
- Validation report: final_video/verification.json

Source audio copied unchanged from the user's Downloads file. Video export uses AAC audio encoding without speed changes. 1080×1920, 30 fps, H.264, soft image motion, crossfades, animated Hindi words and sparkles. Images were generated using the retained Hansi Ki Dhun boy reference; images 3–6 additionally use the opening bedroom illustration as a style reference.

Whisper small Hindi transcription and canonical-word forced alignment estimate lyric timing. Independent transcription onsets correct pauses at 3.04, 5.86, 8.00, 14.88 and 18.32 seconds. Supplied wording is preserved, including यह. Automated audio comparison checks that encoding introduces no drift; word timing is not a human listening certification.

Re-render from the parent workspace with Python: `python songs/neend_ka_jadoo/video_work/render_video.py --name neend_ka_jadoo_1080x1920.mp4`.
