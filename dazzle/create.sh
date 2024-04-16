sudo docker container create --device=/dev/snd --mount type=bind,src=/home/derek/dazzle/media,target=/media --restart always --name dazzler dazzle 
