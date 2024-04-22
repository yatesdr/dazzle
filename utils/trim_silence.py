from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import os

trim_leading_silence = lambda x: x[detect_leading_silence(x) :]
trim_trailing_silence = lambda x: trim_leading_silence(x.reverse()).reverse()
strip_silence = lambda x: trim_trailing_silence(trim_leading_silence(x))

path = "/Users/derek/Documents/Code/DazzleDizzle/media/wav/playlist2"

for item in os.listdir(path):
    if os.path.isfile(f"{path}/{item}") and item.split(".")[-1].upper()=="WAV":
        print("Processing ",item)
        sound: AudioSegment = AudioSegment.from_file(f"{path}/{item}")
        stripped: AudioSegment = strip_silence(sound)
        stripped.export(f"{path}/{item}",format="wav")
    print("Done.")

