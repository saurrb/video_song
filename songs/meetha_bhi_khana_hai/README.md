# मीठा भी खाना है

27.06-second girl-led portrait comedy music video using the saved Hansi Ki Dhun visual style.

## Deliverables

- `final_video/meetha_bhi_khana_hai_1080x1920.mp4`: finished video, 1080×1920, 30 fps, H.264 and AAC.
- `portrait_images/`: 12 separate illustrated scenes, also in `portrait_images_12.zip`.
- `storyboard.md`: scene plan with actual timeline cues.
- `lyrics.txt`: supplied lyrics, split into lines for alignment.
- `caption_hashtags.txt`: ready-to-post text.
- `scene_prompts.json`: complete prompts used with built-in imagegen.
- `references/couple_reference.png`: retained character/style master.
- `video_work/timeline.json`: editable scene and word timings.
- `final_video/lyrics_timed.srt`: phrase subtitle export.
- `final_video/verification.json`: export QA report.

## Timing and reproducibility

The source MP3 was copied unchanged from the user's specified Downloads path. Its speed and placement are unchanged; audio is re-encoded to AAC for the video. Whisper small Hindi transcription and canonical-word cross-attention alignment estimate word timings. English words are shown as supplied; Hindi pronunciations are used only by the aligner. Independent ASR onsets correct pauses at key phrase starts. These are model estimates, not a human listening certification.

Each image was generated separately with built-in imagegen, using the retained girl reference. Scenes 2–12 also reference the first scene to stabilize appearance. Motion is added by the renderer to the still illustrations.

From the parent workspace, run `python songs/meetha_bhi_khana_hai/video_work/render_video.py --name meetha_bhi_khana_hai_1080x1920.mp4` to render again. Run `python songs/meetha_bhi_khana_hai/video_work/verify_video.py` to check output frames, text coverage, dimensions, durations and audio lag. This project reuses the library shared/models/whisper-small model and the starter kit's local font/runtime dependencies.
