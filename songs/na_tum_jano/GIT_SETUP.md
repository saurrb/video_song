# Standalone song project

This repository contains the source audio, supplied lyrics, five generated scene images, prompts, timeline, renderer, final video and verification report for “ना तुम जानो ना हम”.

Install Python dependencies with `python -m pip install -r requirements.txt` and install FFmpeg with libass support. Run commands from this repository directory:

```powershell
python -X utf8 video_work/build_timeline.py
python -X utf8 video_work/render_video.py --name na_tum_jano_1080x1920.mp4
```

The Windows font is not distributed in Git. On a licensed Windows installation, copy Nirmala UI Bold from `C:/Windows/Fonts/NirmalaB.ttf` into `video_work/fonts/NirmalaUI-Bold.ttf` before rendering.

Rendering uses the retained timeline and does not require Whisper weights. Re-running alignment requires the original song library's shared Whisper-small model or adapting the model path in the transcription/alignment scripts. To regenerate the local analysis WAV:

```powershell
ffmpeg -i song.mp3 -ac 1 -ar 16000 video_work/song_16k.wav
python -X utf8 video_work/verify_video.py
```

Preview renders, analysis frames, duplicate image ZIP, decoded audio, and the local font are excluded from Git. They remain available in the original workspace. README links to excluded local artifacts are usable there.
