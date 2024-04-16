# Media folder - best to use WAV's
MEDIA_DIR=~/dazzle/dazzle/media/wav

# Board config file - maps songs to buttons.
CONFIG=~/dazzle/dazzle/config.json

# Do the install, start the container, and always restart it.
sudo docker build . -t dazzle
sudo docker container create --device=/dev/snd --mount type=bind,src=$MEDIA_DIR,target=/media --type=bind,src=$CONFIG,target=/app/dazzle_config.json --restart always --name dazzler dazzle 
sudo docker container run --restart=always dazzler
