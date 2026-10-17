# Ho Gaya Hu Main Besharam

31.90-second Hansi Ki Dhun portrait lyric video. The approved boy leads the story; the girl appears in the final comic reaction. Original audio and exact Roman-script lyrics are retained as song.mp3 and lyrics.txt.

- [Final video](final_video/besharam_paisa_1080x1920.mp4)
- [Captions and hashtags](caption_hashtags.txt)
- [Contact sheet](contact_sheet.jpg), [six portraits ZIP](portrait_images_besharam_paisa.zip)
- [Storyboard](storyboard.md), [exact image prompts](image_prompts.md)
- [Timed subtitles](final_video/lyrics_timed.srt), [verification report](final_video/verification.json)

1080×1920, 30 fps, H.264 CRF18 and AAC 256 kbps. Six new illustrations and twelve short kinetic phrases include all 36 supplied words. A local copy of the maintained starter provides gentle camera motion, crossfades, glowing word reveals and edge sparkles. Previous songs remain unchanged.

Built-in imagegen generated each portrait separately using the approved couple reference. Fresh Whisper-small transcription and forced alignment use the shared local weights and Hindi spoken tokens mapped onto the exact supplied words. The inflation line missed in the first transcription was checked separately in whisper_inflation.json. Three starts that absorbed pauses were adjusted using independent transcription. Word timings remain model estimates, not a human listening certification.

Re-render from the library root:

```powershell
python -X utf8 songs/besharam_paisa/video_work/build_timeline.py
python -X utf8 songs/besharam_paisa/video_work/render_video.py --name besharam_paisa_1080x1920.mp4
python -X utf8 songs/besharam_paisa/video_work/verify_video.py
```
