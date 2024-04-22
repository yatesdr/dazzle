import simpleaudio as sa, threading as t, os
from queue import Queue

def playlistplayer(playlist, in_q):
    index=0
    po = None
    inhibit_autoplay=False
    playing=False

    while True:

        try:
            message = in_q.get(False) # non-blocking
        except:
            message=dict()
        
        if message.get('play'):
            sa.stop_all()
            if index<len(playlist) and index>=0:
                song = playlist[index]
                wav_obj = sa.WaveObject.from_wave_file(song)
                po = wav_obj.play()
                playing=True
            os.system("amixer -- sset PCM -3dB unmute")

        if message.get('stop'):
            sa.stop_all()
            po=None
            playing=False

        # Play next song
        if message.get('next'):
            sa.stop_all()
            was_playing=playing
            playing=False
            index+=1
            if index>=len(playlist): # Wrap if playlist is at the end.
                index=0
            if was_playing:
                in_q.put({"play": True})

        # Set index to previous song in list, and play if was playing already.
        if message.get('prev'):
            sa.stop_all()
            was_playing=playing
            playing=False
            index-=1
            if index<0:
                index=len(playlist)-1
            if was_playing:
                in_q.put({"play": True})

        # Autoplay the next song in the list, if it exists
        if playing==True and po and not po.is_playing():
            index+=1
            if index>=len(playlist): # Loop if we're past the end of the playlist
                index=0

            in_q.put({"play": True})


if __name__=="__main__":
    q = Queue()
    playlist = ["media/wav/Here Comes The Boom - Nelly.wav", "media/wav/Eminem - My Name Is.wav"]
    playerthread = t.Thread(target=player, args=[playlist,q], daemon=True)
    playerthread.start()

    while (True):
        cmd = input("(p) play, (s) stop, (f) next, (b) back - What now? : ")

        if (cmd=="p"):
            q.put({'play': True})

        if (cmd=="s"):
            q.put({'stop': True})

        if (cmd=="f"):
            q.put({'next': True})

        if (cmd=="b"):
            q.put({'prev': True})

