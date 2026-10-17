# Mann Mera — Reels vs Work

Girl-led Hansi Ki Dhun cartoon music video using the supplied 54.413-second recording. Sixteen separate portrait illustrations, 18 lyric phrases, 82 timed display words.

## Deliverables
- final_video/mann_mera_reels_1080x1920.mp4 — finished 1080x1920, 30fps H.264/AAC video.
- portrait_images/ and portrait_images_16.zip — 16 separate PNGs.
- storyboard.md — scene plan.
- scene_prompts.json — prompts for built-in image generation.
- lyrics.txt — original supplied Roman Hindi lyrics.
- lyrics_display.txt — recording-matched display text.
- final_video/lyrics_timed.srt — timed phrase subtitles.
- video_work/timeline.json — editable scene and word timing.
- final_video/verification.json — export verification.

## Characters and story
Only the girl is the human lead: peach bow, long wavy brown hair, peach sweater and lilac skirt. Consistent peach home office, wooden desk, mint laptop and lavender phone. A pink thought-heart represents distraction. The story progresses from determined work, to a two-minute break, to two lost hours, excuses, scrolling and a final return to the phone while work remains unfinished.

## Audio alignment
Whisper small Hindi transcription, canonical Roman-to-Hindi word mapping for DTW alignment, and independent ASR onset corrections at pauses. Original recording timing is preserved; audio is re-encoded without speed changes. Silero VAD identifies initial vocal activity at0.96s. Two display adjustments follow the recording: 'phir bhi na maanta' replaces 'phir bhi maanta na', and 'phone dekha' omits an unsung 'ko' (free ASR omission and forced-alignment probability .0116). Original supplied text remains retained separately. Word times are model estimates, not a human listening certification.

## Render
Same approved kinetic style: gold-to-white active words, cyan glow, scale/slide entrances, subtle zooms/pans, short crossfades and edge sparkles. Longer chorus lines split into readable phrases. No lyrics are placed over musical gaps.

To rebuild from this folder with Python dependencies and FFmpeg available:
python -X utf8 video_work/build_timeline.py
python -X utf8 video_work/render_video.py --name mann_mera_reels_1080x1920.mp4
python -X utf8 video_work/verify_video.py

Whisper weights are reused from the library shared/models/whisper-small folder. Previous videos remain unchanged.
