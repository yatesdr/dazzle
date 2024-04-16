# Dazzle Player
A simple, self-contained audio sample player consisting of a LaunchPad Mini and a Raspberry Pi 4b.

## About
There are lots of great utilities to play samples and triggers from a laptop or PC using MIDI triggers or a Streamdeck - Ableton, reaper, or other DAWs can easily do this.   Even a VLC playlist.   But I wasn't able to find something that met my needs for a durable, self-contained, configurable and self-contained portable music player which requires no screen and let the kids easily run their sound from a dugout or other location.

This project was created for that purpose - to allow for self-service playing of "walk-on" music for Softball games from the dugout.   The basic idea is that each player gets a button, and when they're going up to bat it's easy to start and stop their song with minimal distraction from the game or having to mess with phones and playlists and bluetooth connections.  

Dazzle is designed to directly drive a single powered PA speaker with a mono mix, but could be patched into a local stadium sound board just as easily.

## BOM
You need the following:
1.  XLR panel-mount pass through
2.  USB-c panel-mount pass thorugh
3.  RJ-45 Panel-mount pass through
4.  40mm x 10mm fan
5.  Two 470 ohm resistors
6.  One 22k ohm resistor
7.  One TRS 1/8 audio plug
8.  Various wire, heat-shrink, solder, and hot glue.
9.  Cables to connect everything

## Building it
1.  Print the files from STL's - modify if desired.
2.  Install the panel mounts in the print for XLR, USB-C, and RJ-45 jacks. Wire them into the Pi4 as appropriate.   The USB-C passthrough is intended for powering the Pi. 
3.  Build the output circuit.   The Pi4 has a TRRS output built in, and we want to sum that to mono at the XLR output.   I used a headphone jack cable to plug into the Pi4 (TRS 1/8) together with two 470 ohm resistors to sum L/R, and a 22k ground impedance resistor, all installed right at the XLR patch point.   If you skip this step and try to wire it directly you'll probably get hum and a poor audio output.
4.  Power the board - Its' meant to be powered over usb-c, so you can use a power bank or just plug it in like normal using the passthrough. 


## How to use
1.  Once the physical build is complete, flash Raspbian 64-bit server and boot the pi.  Set up credentials and ssh, no monitor is needed.
2.  Install Docker (sudo apt install docker.io)
3.  Build the docker image (cd dazzle && docker build .) - This may take a while.  Soon I'll push a pre-built image to dockerhub for the Pi4, but for now you have to build it on the Pi.
4.  Download your Media to the Pi using scp or rsync.   WAV files work the best and are what you should use.   If you have MP3's there is a utility provided to convert them to WAV.  MP3's can also work, but are a bit slow to load on a Pi4, so only use them if you're using this on a laptop or n100 type machine.  For testing with media you already own, some utilities are provided to pull in WAV's from Youtube, but if you're using this in public you should of course contact the license holders and do this officially and legally.
5.  Edit app.py and modify the config area to reflect the board layout and songs you want.   To start in the middle of a song, set the enter time in seconds.   To play for a specified duration, set the duration time in seconds, or it will play until stopped or the song ends if you leave it at 0.
6.  Run the docker file at boot using restart=always.  You will need to pass in --device=/dev/snd and --mount flags to get your media directory set up (see shell scripts for details).
```
sudo docker container create --device=/dev/snd --mount type=bind,src=/home/<user>/dazzle/media,target=/<your_media_folder_on_pi4> --restart always --name dazzler dazzle
sudo docker run dazzler --restart always 
```

7. After re-booting, you'll see the board start working and should be able to play your samples.

## Basic Actions:
1. Buttons with a song programmed turn white.
2. Push a white button to start playback, the button turns green for the active song.
3. Push the green button to stop playback, or use the mute button (red)
4. Push any other white button to change songs.


## Road-Map & Future improvements
These are the things I want to work on when I have time, but may never get to.   
1.  Move configuration to a separate file.
2.  Use the Wifi chip to create a local network, with web application to modify the board config.
3.  A small pop can sometimes be heard when stopping media, I'd like to fix this.
4.  Improve latency between press and play for MP3's.   This probably requires using something other than pydub, but it's unclear why mp3's lag so much (5-6 seconds).   For now, just use WAV's and the latency is acceptable at about 0.5 seconds for a Pi4.

