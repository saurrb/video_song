from pathlib import Path
import shutil, subprocess
root=Path(__file__).resolve().parent.parent
p=root/'songs/middle_class_life'
p.mkdir(exist_ok=False)
shutil.copytree(root/'reusable_song_kit/starter',p,dirs_exist_ok=True)
audio=next(Path('C:/Users/Saurabh/Downloads').glob('*cut_22sec*usesuno.com*bpm_61.mp3'))
shutil.copy2(audio,p/'song.mp3')
lyrics='''Middle class life meri
Khud ka room nahi
Privacy milti nahi
Din ho chahe raat
Mere har call message pe hai बवाल
Mujhe jana ho kahin
Permission milti nahi
Main yeh kaise karun
Paiso pe hai बवाल
Compromise karte karte thak gaye hain yaar
'''
(p/'lyrics.txt').write_text(lyrics,encoding='utf8')
(p/'references').mkdir(exist_ok=True)
shutil.copy2(root/'shared/characters/approved_reference.png',p/'references/couple_reference.png')
prev=root/'songs/phir_bhi_hansta/video_work'
for name in ['transcribe.py','align_lyrics.py','verify_video.py','contact_sheet.py']:
    shutil.copy2(prev/name,p/'video_work'/name)
t=p/'video_work/transcribe.py'
s=t.read_text(encoding='utf8');a=s.index("initial_prompt=");b=s.index(',condition_on_previous_text',a)
s=s[:a]+"initial_prompt='मिडिल क्लास लाइफ मेरी, खुद का रूम नहीं, प्राइवेसी, कॉल मैसेज, परमिशन, पैसों, कॉम्प्रोमाइज।'"+s[b:];t.write_text(s,encoding='utf8')
t=p/'video_work/align_lyrics.py';s=t.read_text(encoding='utf8')
a=s.index('subs=');b=s.index('\n',a)
eng='Middle class life meri Khud ka room nahi Privacy milti Din ho chahe raat Mere har call message pe hai Mujhe jana kahin Permission Main yeh kaise karun Paiso Compromise karte thak gaye hain yaar'.split()
hin='मिडिल क्लास लाइफ मेरी खुद का रूम नहीं प्राइवेसी मिलती दिन हो चाहे रात मेरे हर कॉल मैसेज पे है मुझे जाना कहीं परमिशन मैं ये कैसे करूं पैसों कॉम्प्रोमाइज करते थक गए हैं यार'.split()
assert len(eng)==len(hin)
s=s[:a]+'subs='+repr(dict(zip(eng,hin)))+s[b:];t.write_text(s,encoding='utf8')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'song.mp3'),'-ac','1','-ar','16000',str(p/'video_work/song_16k.wav')],check=True)
print(p)
