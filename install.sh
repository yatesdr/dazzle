# Media folder - best to use WAV's
MEDIA_DIR=~/dazzle/media

# Board config file - maps songs to buttons.
CONFIG_DIR=~/dazzle/config

# Do the install, start the container, and always restart it.
sudo docker build . -t dazzle
sudo docker container create --device=/dev/snd --mount type=bind,src=$MEDIA_DIR,target=/media --mount type=bind,src=$CONFIG_DIR,target=/config --restart always --name dazzler dazzle 
sudo docker container start dazzler
