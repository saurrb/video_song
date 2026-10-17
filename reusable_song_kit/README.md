# Hansi Ki Dhun: reusable song production kit

## Use next time
Tell Codex: "Use the Hansi Ki Dhun song kit at C:/Users/Saurabh/Documents/video_song/reusable_song_kit. My new audio is [path] and lyrics are [path]. Keep the same couple and kinetic typography. Make a complete portrait music video."

Create new projects under songs/<song_name>/, or use `python tools/song_library.py new <song_name> --audio <path> --lyrics <lyrics_file>`. This copies starter/ into a new song folder. Put song.mp3 and lyrics.txt there. Keep the completed original project unchanged. Every song needs newly generated story images, fresh transcription/alignment, and a fresh timeline. The example timeline is documentation, not real song timing.

## Character and visual identity
Use references/couple_reference.png as the image-generation reference every time. Boy: tousled brown hair, round glasses, navy hoodie, beige trousers. Girl: long wavy brown hair, peach side bow and sweater, lilac skirt. Cute chibi proportions, blush cheeks, warm brown outlines, soft flat 2D shading, sky blue/peach/pink accents. Expressive comedy, consistent faces and clothing. Generate separate 9:16 images; keep faces and key story action above the lower lyric area. No baked-in lyric text. Built-in imagegen skill/tool is the default. Do not silently substitute hand-drawn placeholders.

Prompt scaffold: "Create scene [N] of a Hindi comedy song: [lyric/story beat]. Use the attached couple reference to preserve exact character identity and illustration style. Portrait 9:16. [action, expression, visual joke, setting]. Keep important action above the bottom quarter for animated lyrics. No lyric text, watermark, or collage."

## Production workflow
1. Read the new lyrics, probe the new audio duration, plan one story beat per lyric section. 32 scenes was the original song's count, not a requirement for every song.
2. Generate/save numbered PNG images under portrait_images. Review a contact sheet for consistency.
3. Decode audio: ffmpeg -i song.mp3 -ac 1 -ar 16000 video_work/song_16k.wav
4. Run multilingual Whisper with Hindi language and word timestamps; align provided canonical lyrics to vocals. Use transcription to choose short alignment blocks, then forced alignment for exact display words. Preserve Latin-script Hindi/English words in display; use spoken Hindi substitutions only for alignment. Review low-confidence words, repeats, missing/extra vocals, and transitions. Do not reuse old time anchors or word substitutions blindly.
5. Write video_work/timeline.json using timeline.example.json as the schema. Each phrase contains word start/end seconds and exact display text. Each scene has an image basename, numeric scene ID, start/end seconds. Scene coverage must be continuous from zero through the full audio duration. No lyrics in instrumental sections. Cue pictures from lyric events rather than equal durations.
6. Install Python requirements in an appropriate environment. FFmpeg/ffprobe must be on PATH and FFmpeg must include libass/complex shaping. Windows Nirmala UI Bold is retained for this personal local workflow; verify font rights before distributing it elsewhere.
7. Preview: python video_work/render_video.py --end 10 --width 540 --name preview.mp4
8. Full render: python video_work/render_video.py
9. Inspect word/phrase screenshots for Hindi shaping, clipped text, faces and timing. Decode the whole output to check corruption/black frames; compare audio duration and sample alignment near beginning/middle/end. Listen for lyric synchronization and correct any drift. Word timestamps remain model estimates until reviewed.

## Saved motion/style
1080x1920, 30 fps, H.264 CRF18, AAC256kbps, faststart. Smooth 1.02–1.09 zoom/pan, 0.13s crossfades, edge sparkles. Nirmala UI Bold at base116 with measured one/two-line layout, y1517–1658. Words slide up24px and pop116%->100%, blur settles, gold active word fades to white with cyan glow. Lower gradient protects legibility. Scrim fades after the new final lyric; no fixed old timestamp. Renderer accepts arbitrary scene count. Timeline title/artist control export metadata.

## What is saved where
references/: approved character master.
branding/: Facebook DP, cover, bio, prompts.
starter/: reusable renderer, dependencies, font, example timeline and empty output folders.
original_song_examples/: original alignment/transcription/timeline scripts, prompts and data as worked examples only. Those scripts contain song-specific words, timing blocks, filenames and 32-scene checks: adapt before using on a new song.

The original hoodie video, audio and 32 PNGs are in songs/hoodie_breakup/. Shared character samples and branding are in shared/characters/ and shared/branding/. The kinetic reference and its analysis are in shared/kinetic_reference/. Large audio/video files and Whisper weights are not duplicated in this compact kit. The existing local model can be reused from C:/Users/Saurabh/Documents/video_song/shared/models/whisper-small; another computer needs its own model and dependencies.

## Posting style
Short Hinglish/Hindi joke from the hook, 2–3 emojis, one relatable question. Brand hashtag #HansiKiDhun plus 4–7 relevant Hindi/music/comedy/topic tags. Do not promise virality. Suggested page name Hansi Ki Dhun; username availability not checked.
