# Aaj Khane Mein Kya Banana Hai

27.25-second Hansi Ki Dhun portrait lyric video starring the approved couple in a kitchen comedy. Original audio and exact Roman-script lyrics are retained as song.mp3 and lyrics.txt.

- [Final video](final_video/kya_banana_hai_1080x1920.mp4)
- [Captions and hashtags](caption_hashtags.txt)
- [Contact sheet](contact_sheet.jpg), [six portraits ZIP](portrait_images_kya_banana_hai.zip)
- [Storyboard](storyboard.md), [exact image prompts](image_prompts.md)
- [Timed subtitles](final_video/lyrics_timed.srt), [verification report](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18 and AAC 256 kbps. Six new illustrations and twelve short kinetic phrases include all 36 supplied words. A local copy of the maintained starter provides gentle camera motion, crossfades, glowing word reveals and edge sparkles.

Built-in imagegen generated each portrait separately using the approved couple reference. Fresh Whisper-small transcription and forced alignment use the shared local weights and Hindi spoken tokens mapped onto the exact supplied words. The repeated hook and following line were separately transcribed in whisper_middle.json, and overlapping line starts corrected. Word timings remain model estimates, not a human listening certification.

Re-render from the library root:

```powershell
python -X utf8 songs/kya_banana_hai/video_work/build_timeline.py
python -X utf8 songs/kya_banana_hai/video_work/render_video.py --name kya_banana_hai_1080x1920.mp4
python -X utf8 songs/kya_banana_hai/video_work/verify_video.py
```
