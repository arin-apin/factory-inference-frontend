#Dockerfile step 2 of learing docker. Do a volume and store the image of sd card 
FROM alpine:latest
LABEL version="1.0"
LABEL description="A simple image creating a volume and directory"


#Alpine no tiene bash 
RUN apk add --no-cache bash
#tampoco losetup, mirar esto https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git

RUN apk add util-linux
#WORKDIR /Despliegue
RUN mkdir /Despliegue
#Context (=Working directory) of docker is the same as the one where the Dockerfile is located. Therefore we need to place it there.
#We need to have in our docker image the script, sd image and the interface
WORKDIR /Despliegue

#dot means
COPY script_despliegue.sh .
COPY modelo-coral.img .
COPY interfaz_coral.py .
ADD assets ./assets

RUN chmod +x script_despliegue.sh

#RUN touch /Despliegue/creacion.sh
ENTRYPOINT ["sh", "script_despliegue.sh"]


#When we call it, we need to specify the path of the volume in the host (our machine). 
#It is possible to run the image from any directory, but you have to built it in imagen_docker
#IMPORTANT: It cant be the same as the volume, it will delete the files. 

