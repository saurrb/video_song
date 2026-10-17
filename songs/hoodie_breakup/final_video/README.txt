MERI HOODIE WAPAS KAR DE - PORTRAIT MUSIC VIDEO

Main export: hoodie_kinetic_song_1080x1920.mp4
Format: 1080 x 1920, 30 fps, H.264 video, AAC stereo audio, fast-start MP4.
Audio: complete original song.mp3, approximately 68.44 seconds.
Visuals: all 32 supplied portrait illustrations, timed to their corresponding lyrics; short instrumental ending with visual callbacks.
Typography: 165 Hindi/English lyric words from lyrics.txt, word-by-word pop and slide entrances, blur-to-sharp transition, cyan glow and gold emphasis.
Animation: smooth camera zooms and drift, quick dissolves and small twinkling particles.

lyrics_timed.srt is an editable phrase-level subtitle file. Word-level timing and scene cues are preserved in ../video_work/timeline.json. The animated typography is in ../video_work/kinetic_lyrics.ass.

Timing method: faster-whisper small multilingual transcription, followed by Whisper cross-attention/DTW alignment against the supplied lyrics. Original spellings are preserved. Model timing estimates are on a 20 ms grid, displayed at 30 fps. verification.json records output integrity and source-versus-export audio alignment checks. Automatic word timing is not a human listening certification.

The typography reference was decoded and reviewed across all 513 frames. Details: ../../../shared/kinetic_reference/reference_analysis.md.

To rebuild from this project folder:
python video_work/render_video.py

Dependencies used: FFmpeg with libass, Python, OpenCV, NumPy, Pillow, uharfbuzz, fontTools, faster-whisper. Hindi text is shaped by HarfBuzz/libass using Nirmala UI Bold.
