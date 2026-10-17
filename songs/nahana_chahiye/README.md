# नहाना चाहिए — Hansi Ki Dhun visual treatment

15.047-second portrait video using the user-supplied comedy-poem recording and lyrics. Six separate images generated with the built-in image generator, matching the saved character reference.

## Files
- final_video/nahana_chahiye_1080x1920.mp4 — finished 1080x1920, 30 fps H.264/AAC video.
- portrait_images_6.zip — all six separate portrait PNGs.
- storyboard.md and scene_prompts.json — story and exact generation prompts.
- lyrics.txt — provided lyrics, including numeral 7.
- final_video/lyrics_timed.srt — phrase subtitles.
- video_work/timeline.json — editable word and scene times.
- final_video/verification.json — output checks.

## Timing and treatment
Whisper small Hindi free transcription and canonical DTW alignment. ASR onsets correct stretched word starts after pauses: मुश्किलों 4.52s, पर 7.70s, आदमी 11.68s. Supplied spelling retained; 7 spoken as सात for alignment. Text splits the long third line for legibility. Bath reveal occurs at नहाना, 13.40s; clean ending starts14.30s. Audio timing is unchanged. Model-estimated lyric timing has not been certified by human listening. This is a cartoon treatment of the supplied recording, not a claim of authorship of its poem or performance.

To rebuild from this folder with Python dependencies and FFmpeg installed:
python -X utf8 video_work/build_timeline.py
python -X utf8 video_work/render_video.py --name nahana_chahiye_1080x1920.mp4
python -X utf8 video_work/verify_video.py

Previous song projects remain unchanged. Shared Whisper weights are read from the library shared/models/whisper-small folder.
