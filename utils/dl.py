import os

links = [
'https://www.youtube.com/watch?v=kWjOE4Gf8sc&pp=ygUWbGlsIGRvdWJsZSBvIDAwNyBjbGVhbg%3D%3D',
        ]

for link in links:
    os.system(f"yt-dlp -x --audio-format wav {link}")
