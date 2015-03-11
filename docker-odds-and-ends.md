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