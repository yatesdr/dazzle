# Dazzle Player
A simple, self-contained audio sample player consisting of a LaunchPad Mini and a Raspberry Pi 4b.

## About
There are lots of great utilities to play samples and triggers from a laptop or PC using MIDI triggers or a Streamdeck - Ableton, reaper, or other DAWs can easily do this.   Even a VLC playlist.   But I wasn't able to find something that met my needs for a durable, self-contained, configurable and portable music player which requires no screen and let the kids easily run their sound from a dugout or other location.

This project was created for that purpose - to allow for self-service playing of "walk-on" music for Softball games from the dugout.   The basic idea is that each player gets a button, and when they're going up to bat it's easy to start and stop their song with minimal distraction from the game or having to mess with phones and playlists and bluetooth connections.  

Dazzle is designed to directly drive a single powered PA speaker with a mono mix, but could also be patched into a local stadium sound board or other sound system for sound effects and sample playback.

## BOM
You need the following:
1.  Raspberry Pi 4b (4GB) and a Novation Launchpad Mini mk3.
1.  XLR panel-mount pass through
2.  USB-c panel-mount pass thorugh
3.  RJ-45 Panel-mount pass through
4.  40mm x 10mm fan
5.  Two 470 ohm resistors
6.  One 22k ohm resistor
7.  One TRS 1/8 audio plug
8.  m3 and m4 socket head screws for assembling the case.
9.  Various wire, heat-shrink, solder, and hot glue.
10.  Cables to connect everything - in particular a right-angle USB-c to USB-a cable for the Launchpad Mini MK3.

## Building it
1.  Print the files from STL's - modify if desired in the Fusion 360 files provided.  Install the Pi4.
2.  Install the panel mounts in the print for XLR, USB-C, and RJ-45 jacks. Wire them into the Pi4 as appropriate.   The USB-C passthrough is intended for powering the Pi. 
3.  Build the audio output mono mix circuit.   The Pi4 has a TRRS output built in, and we want to sum that to mono at the XLR output so we can use normal WAV files in stereo or mono.   I used an inexpensive headphone cable to plug into the Pi4 (TRS 1/8) together with two 470 ohm resistors to sum L/R, and a 22k ground impedance resistor, all installed right at the XLR patch point.   If you skip this step and try to wire it directly you'll probably get hum and a poor audio output, but you can experiment with other output strategies if you want.
4.  Install the LaunchPad Mini and clamp it down - There are two 4mm bolts to hold the launchpad in the case.
5.  Power it up - It's designed to be powered over usb-c, so you can use a power bank or just plug it into 120v power using a Pi4 power addapter and the passthrough. 

## Install Dazzle
Dazzle is intended to be used with a vanilla raspberry pi 4b / 4GB, but may work on other systems also if you're adventurous.  It should also run on a 2GB Pi-4B but is untested.

1.  Use Raspberry Pi Imager to burn a basic installation of Raspbian 64-bit server.   Set up your credentials and SSH access here so you don't need to mess with a monitor.
2.  Boot and login to the pi via ssh.
3.  Install Git and Docker: ```sudo apt install git docker.io```
4.  Clone the project into your home folder
```
cd ~/
git clone https://github.com/yatesdr/dazzle
```
5. Install it  
```
cd ~/dazzle/dazzle
./install.sh
```

Install will build the local docker image, map the drive and config, and then start it with a restart policy of always.  By default, the media directory is set to ~/dazzle/dazzle/media/wav, and the config file is ~/dazzle/dazzle/config/config.json.

If you want to see the running container, try  ```sudo docker ps```

If you need to change things, a cleaning script is provided:  ```./clean.sh```

## How to use
1.  Upload your Media to the Pi's media folder using scp, rsync, or some other method.  By default install this folder is in ```~/dazzle/dazzle/media/wav/``` but you can move it before running install.sh if you prefer.  

Media Notes: WAV files work the best and are what you should use with a Pi4b.   If you only have MP3's there is a utility provided to convert them to WAV files but you will need ffmpeg and some other dependencies to be installed on the Pi4b.  MP3's can also be made to work, but are a bit slow to load on a Pi4, so only use them if you're using this on a laptop or n100 type machine.  For testing with media you already own, some utilities are provided to pull in WAV's from Youtube, but if you're using this in public you should of course contact the license holders and do this officially and legally.

2.  Edit ~/dazzle/dazzle/config/config.json  - modify to reflect the board layout and songs you want.   To start in the middle of a song, set the enter time in seconds.   To play for a specified duration, set the duration time in seconds, or it will play until stopped or the song ends if you leave it at 0.  If you have a specific volume to set, you can pass this in the config using dB in a key like "volume": "-12dB".

Note:   The config file is reloaded on every keypress, so if you make changes just push the mute button to reload the config.

4. If you have a valid config, you'll see the board start working and should be able to play your samples.


## Configuration - config.json
The board configuration is done by editing config.json.   It is loaded at every keypress, so if you make changes they will be reflected if they're valid.

If config.json is not valid JSON, the container will crash and go into reload loop, so just fix it and wait a bit and it will start working again.

Parameters:
- row:  from 1 to 8 for the white keys on LP Mini.   1 is top row, 8 is bottom row.
- col:  from 0 to 7 for the white keys.   0 is far left, 7 is far right.
- action:  "play" - used for playing a file (requires "file" key) or "stop" 
- file: The file name.   File must exist in the media directory.
- start: The time in seconds of where you want the file to start playing (in point).
- duration: How long you want the file to play for.   Set to 0 if you want it to play the whole file or until stopped.
- vol (optional): set a custom volume in the format of "-24dB" or "50%".   This is passed to amixer, so any valid arguments to amixer will also work here.

Note:  By default the output will be set to -12dB level.   So if you need the song volumes to match you should specify them in the config file.   If no volume is specified, it will be played at -12dB.


## Basic Actions:
1. Buttons with a song programmed turn white.
2. Push a white button to start playback, the button turns green for the active song.
3. Push the green button to stop playback, or use the mute button (red)
4. Push any other white button to change songs.


## Road-Map & Future improvements
These are the things I want to work on when I have time, but may never get to.   
1.  Use the Wifi chip to create a local network, with web application to modify the board config from your phone.
2.  A small pop can sometimes be heard when stopping media, I'd like to fix this.
3.  Improve latency between press and play for MP3's.   This probably requires using something other than pydub, but it's unclear why mp3's lag so much (5-6 seconds).   For now, just use WAV's and the latency is acceptable at about 0.5 seconds for a Pi4.

