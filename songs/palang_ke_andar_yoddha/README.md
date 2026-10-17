# पलंग के अंदर योद्धा

Hansi Ki Dhun portrait music video, based on the supplied 38.635-second song and 16 lyric lines.

## Deliverables
- final_video/palang_ke_andar_yoddha_1080x1920.mp4: finished 1080x1920, 30 fps music video.
- portrait_images/: 16 separate AI-generated PNG scenes.
- portrait_images_16.zip: all images in one download.
- storyboard.md: scene-by-scene story plan.
- scene_prompts.json: complete prompts used with the built-in image generator.
- lyrics.txt: original user-supplied lyrics.
- final_video/lyrics_timed.srt: timed phrase subtitles.
- video_work/timeline.json: editable scene and word timing.
- final_video/verification.json: export checks, generated after render.

## Story
The sleepy boy calls himself a lion, becomes a kitten when mummy calls, acts like a warrior indoors, gets scared of a bird and mosquito, and cannot find his slippers. The girl tries a confetti pop and dhol, then tells mummy. Mummy's kitchen-prop entrance sends him fleeing with a bedsheet, followed by the ironic hero fantasy and under-bed reveal. All action is playful cartoon comedy.

## Style and timing
Recurring reference characters in soft chibi 2D style; a consistent mint-green-sari mother and peach bedroom with teal bedding. Gold-to-white word entrances, cyan glow, subtle zoom/pan, edge sparkles and two small reaction-motion accents. Original audio timing preserved, AAC re-encoded without time stretching.

Whisper small multilingual supplied a free Hindi transcription. Canonical lyrics were aligned through cross-attention DTW; English Dhurandhar was aligned as धुरंधर while retaining its display spelling. Independent ASR onsets correct stretched word starts across gaps, particularly first vocal at 0.90 seconds and mummy's entrance at 27.82 seconds. No lyrics in the instrumental pause or ending. Word timing is model-estimated rather than a human listening certification.

## Rebuild
With FFmpeg on PATH and the Python dependencies in requirements.txt installed:

python -X utf8 video_work/build_timeline.py
python -X utf8 video_work/render_video.py --name palang_ke_andar_yoddha_1080x1920.mp4
python -X utf8 video_work/verify_video.py

Run from this song folder. The prior song and reusable template remain unchanged. Whisper model weights are reused locally from the library shared/models/whisper-small folder and are not duplicated here.
