sudo docker build . -t dazzle
sudo docker run --device=/dev/snd --mount type=bind,src=/home/derek/dazzle/media,target=/media dazzle --restart always
