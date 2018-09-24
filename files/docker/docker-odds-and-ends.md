# Docker odds and ends

I can never remember the docker syntax, here’s a quick-reference


## (Mac/Windows) – start up boot2docker

    boot2docker up
    (note the export lines, cut+paste them to make them live)
    
## what images are there

    docker images
## what containers are present

    docker ps -a
## running a container in the background

    docker run -d -i -t my_image_name
    optionally:
       add -p 80 to expose port 80 (for example)
       use 'docker ps -a' to see what it was mapped to
## stopping a container

    docker ps -a -q # note the image tag
    docker stop my_tag_number
## delete all containers

    docker rm $(docker ps -a -q)
## delete a image

     similar to 'docker rm' just use 'docker 'rmi'
## (Mac/Windows) – stop boot2docker

    boot2docker stop

# docker RUN vs CMD

    'run' is executed when you 'docker build'
    'cmd' is executed with you 'docker run'

# delete all stopped containers

`docker rm $(docker ps -a -q)`

# name a versioned container
	alias dl=`docker ps -l -q`
	docker commit `dl` mynamehere

# graph dependencies 

```
# generate image dependency diagram via imagemagick
docker images -viz | dot -Tpng -o docker.png

# start a http server
python -m SimpleHTTPServer

# view it
bring up http://foo:8000/docker.png

```

# where does it store everything
```
/var/lib/docker
```

# don't run a daemon in your Dockerfile
RUN is for things that affect the filesystem, not to start daemons

# letting containers talk to each other
```
# run a container and name it
$ docker run -d -name foo fooimage

# run another and link it to the first using an alias
$ docker run -link /foo:whatever foo2image env
(prints out the ports etc)
```

# clean up intermediate images not used by anything
```
docker rmi $(docker images | grep "<none>" | awk '{print $3}')
```	
