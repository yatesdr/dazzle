from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import os

trim_leading_silence = lambda x: x[detect_leading_silence(x) :]
trim_trailing_silence = lambda x: trim_leading_silence(x.reverse()).reverse()
strip_silence = lambda x: trim_trailing_silence(trim_leading_silence(x))

path = "~/dazzle/media/wav/playlist2"
for item in os.listdir(path):
    print("Processing ",item)
    if os.path.isfile(item) and item.split(".").upper()=="WAV":
        sound: AudioSegment = AudioSegment.from_file(item)
        stripped: AudioSegment = strip_silence(sound)
        sound.export(item,format="wav")
    print("Done.")

