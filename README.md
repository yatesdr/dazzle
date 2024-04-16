# Dazzle Player
A simple, self-contained audio sample player consisting of a LaunchPad Mini, a Raspberry Pi 4.

## About
This project was originally designed for playing "walk-on" music for Softball games.   The idea is each player gets a button, and when they're going up to bat it's easy to start and stop their song.

Dazzle is designed to directly drive a single powered PA speaker, but could be patched into a local sound board just as easily.

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
1.  Print the STL's, wire up your system, and install Raspbian x64 server
2.  Install Docker (sudo apt install docker.io)
3.  Build the docker image, or use the public one (cd dazzle && docker build .) - This may take a while.
4.  Download your Media.   WAV files work the best.  MP3's are a bit slow to load on a Pi4, but work fine on laptops and such. 
5.  Edit app.py and modify the config area to reflect the board layout and songs you want.   To start in the middle of a song, set the enter time in seconds.   To play for a specified duration, set the duration time in seconds.
6.  Run the docker file at boot using restart=always.  You will need to pass in --device=/dev/snd and --mount flags to get your media directory set up (see shell scripts for details).
7. After re-booting, you'll see the board start working and should be able to play your samples.

## Basic Actions:
1. Buttons with a song programmed turn white.
2. Push a white button to start playback, the button turns green for the active song.
3. Push the green button to stop playback, or use the mute button (red)
4. Push any other white button to change songs.



