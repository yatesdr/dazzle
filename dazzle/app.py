from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import time, os
import lpmini_toolkit as lptk
import threading

# Define a few colors to use with LP Mini Mk3.
X=0; W=1; R=5; B=51; G=25


# Set the volume to -12dB reference and mute it
os.system("amixer -- sset PCM -12dB mute")

# Media directory - This is usually a bind mount on the system.  Absolute path.
mdir = "/media/wav"


def mute():
    os.system("amixer sset PCM mute")

def unmute():
    os.system("amixer -- sset PCM -12dB unmute")


# Configuration for the application
def load_config():
    
    config = [
            {"row": 8, "col": 8, "action": "stop"},
            {"row": 1, "col": 0, "action": "play", "file": "Eminem - My Name Is.wav", "start": 0.0, "duration": 0},
            {"row": 1, "col": 1, "action": "play", "file": "ACDC - Thunderstruck.wav", "start": 5.0, "duration": 0},
            {"row": 1, "col": 2, "action": "play", "file": "David Guetta - Titanium.wav", "start": 43.0, "duration": 0},
    ]
    return config 
            

def lp_handle_event(evt,mtx,config,players):

    
    X=0; W=1; R=5; B=51; G=25
    # Handle button press - actions on release, not on press.
    if evt and evt.type=="release":
        command = [ item for item in config if item["row"]==evt.button.y and item["col"]==evt.button.x ]
        if (len(command)):
            fc = command[0]
            print("Release command: ", fc)
            t = time.time()
            print("[A]: ",time.time()-t)

            # Handle play commands.
            if fc['action']=="play":
                songfile = f"{mdir}/{fc['file']}"
                start_ms = fc['start']*1000
                end_ms = 1000*(fc['duration']+fc['start'])
                print(songfile, start_ms, end_ms)
                print("[B]: ", time.time()-t)

                # See if this song was playing (to stop only, skips starting)
                is_playing = (mtx[fc['row']][fc['col']]==G)

                mute()

                # Stop all players
                for p in players:
                    p.stop()

                # Reset the matrix display to base config with nothign playing.
                mtx = lptk.init_matrix(config)

                print("[C]: ", time.time()-t)

                # If nothing was playing, start this song.
                if not is_playing:
                    # Start this song and place the player stream in config.
                    print("[D]: ", time.time()-t)
                    sound = AudioSegment.from_wav(songfile) #, format="mp3")
                    print("[E]: ", time.time()-t)

                    if fc['duration']>0: 
                        splice = sound[start_ms:end_ms]
                    else:
                        splice = sound[start_ms:].fade_in(50)
                    print("[F]: ", time.time()-t)

                    unmute()
                    playback = play(splice)
                    players.append(playback)
               
                    # Mark the current playing song green on the board.
                    mtx[fc['row']][fc['col']]=G

            if fc['action']=="stop":
                mute()
                for p in players:
                    p.stop()
                mtx = lptk.init_matrix(config)

    return mtx


def lp_handler(config):
    lp = lptk.init_launchpad()
    if (not lp):
        print("Launchpad not detected, exiting.")
        return 0

    players = []
    lptk.clear_panel(lp)
    mtx=lptk.init_matrix(config)
    lptk.write_colors(lp,mtx)

    while True:

        #try:
            mtx = lp_handle_event(lp.panel.buttons().poll_for_event(),mtx,config,players)  # Wait for a button press/release  # noqa
            lptk.write_colors(lp,mtx)    
        #except Exception:
        #    print("Program crash")


config = load_config()
lp_handler(config)


