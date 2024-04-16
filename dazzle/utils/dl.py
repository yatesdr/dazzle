import os

links = [
'https://www.youtube.com/watch?v=OF04pKp-r9o&pp=ygUUa2VzaGEgdGlrIHRvayBseXJpY3M%3D',
]

for link in links:
    os.system(f"yt-dlp -x --audio-format wav {link}")
