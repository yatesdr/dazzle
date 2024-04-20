from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import time, os, json
import lpmini_toolkit as lptk
import threading

# Define a few colors to use with LP Mini Mk3.
X=0; W=1; R=5; B=51; G=25


# Set the volume to -12dB reference and mute it
os.system("amixer -- sset PCM -3dB mute")

# Media directory - This is usually a bind mount on the system.  Absolute path.
mdir = "/media"


def mute():
    os.system("amixer sset PCM mute")

def unmute():
    os.system("amixer -- sset PCM -3dB unmute")


# Configuration for the application
def load_config():
    file = "/config/config.json"
    with open(file,'r') as f_in:
        config = json.load(f_in)
    
    return config 
            

def lp_handle_event(evt,mtx,config,players,lp):

    X=0; W=1; R=5; B=51; G=25
    # Handle button press - actions on release, not on press.
    if evt and evt.type=="release":
        command = [ item for item in config if item["row"]==evt.button.y and item["col"]==evt.button.x ]
        if (len(command)):
            fc = command[0]
            print("Release command: ", fc)
            t = time.time()

            # Handle play commands.
            if fc['action']=="play":
                songfile = f"{mdir}/{fc['file']}"
                extension = songfile.split(".")[-1]

                start_ms = fc['start']*1000
                end_ms = 1000*(fc['duration']+fc['start'])

                # See if this song was playing (to stop only, skips starting)
                is_playing = (mtx[fc['row']][fc['col']]==G)

                mute()

                # Stop all players
                for p in players:
                    p.stop()

                # Reset the matrix display to base config with nothign playing.
                mtx = lptk.init_matrix(config)

                # If nothing was playing, start this song.
                if not is_playing:
                    # Start this song and place the player stream in config.
                    if extension.upper()=="WAV":
                        sound = AudioSegment.from_wav(songfile) #, format="mp3")

                    elif extension.upper()=="MP3":
                        sound = AudioSegment.from_mp3(songfile)

                    else:
                        print("Error - songfile extension not recognized or supported: ",extension)
                        sound=None

                    if fc['duration']>0: 
                        splice = sound[start_ms:end_ms].fade_in(50).fade_out(500)

                    else:
                        splice = sound[start_ms:].fade_in(50)

                    unmute()

                    # Custom volume is specified, apply it.
                    if fc.get("vol"):
                        os.system(f"amixer -- sset PCM {fc.get('vol')}")

                    playback = play(splice)
                    players.append(playback)
               
                    # Mark the current playing song green on the board.
                    mtx[fc['row']][fc['col']]=G

            if fc['action']=="stop":
                mute()
                for p in players:
                    p.stop()
                mtx = lptk.init_matrix(config)

            if fc['action']=="playlist":
                mute()
                for p in players:
                    p.stop()
            
                is_playing = mtx[fc['row']][fc['col']]==B or mtx[fc['row']][fc['col']]==G

                if not is_playing:
                    playlist = AudioSegment.empty()

                    # Give instant feedback while loading a large playlist
                    mtx[fc['row']][fc['col']]=B
                    lptk.write_colors(lp,mtx)

                    files = fc['files']
                    isfirst=True
                    for item in files:
                        print("item: ",item)
                        f = item['file']

                        in_ms=0
                        out_ms=0
                        if item.get('in'):
                            in_ms = item['in']*1000
                        if item.get('out'):
                            out_ms = item['out']*1000
                        
                        toplay = AudioSegment.from_wav(f"{mdir}/{f}")

                        if out_ms>0:
                            toplay = toplay[in_ms:out_ms]
                        else:
                            toplay = toplay[in_ms:]

                        if isfirst:
                            playlist=toplay
                            isfirst=False
                        else:
                            playlist = playlist.append(toplay,crossfade=3000)
                    
                    unmute()
                    playback = play(playlist)
                    players.append(playback)

                    mtx[fc['row']][fc['col']]=G
                else:
                    mtx = lptk.init_matrix(config)
    return mtx


def lp_handler():
    config=load_config()
    lp = lptk.init_launchpad()
    if (not lp):
        print("Launchpad not detected, exiting.")
        return 0

    players = []
    lptk.clear_panel(lp)
    mtx=lptk.init_matrix(config)
    lptk.write_colors(lp,mtx)

    while True:
            lptk.write_colors(lp,mtx)    
            config = load_config()
            mtx = lp_handle_event(lp.panel.buttons().poll_for_event(),mtx,config,players,lp)  # Wait for a button press/release  # noqa

            # Prune old plays when stopped to avoid memory filling up.
            is_playing=False
            for p in players:
                if p.is_playing():
                    is_playing=True

            if not is_playing:
                players=list()


lp_handler()


