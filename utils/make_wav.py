import os

files = [f for f in os.listdir() if os.path.isfile(f)]

for f in files:
    print("Working on ... ",f)

    ext = f.split(".")[-1]
    fname = f.split(".")[0]

    if ext=="mp3":
        os.system(f"""ffmpeg -i "{f}" "{fname}.wav" """)

