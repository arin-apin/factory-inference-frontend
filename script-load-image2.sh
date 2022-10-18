#!/bin/bash

#TBD: FIRST CREATE A COPY OF THE IMAGE! Otherwise the changes are applied to the image 
#Change to losetup-f
#Change model and labels.
#Add copy progress
#Python create client directory

echo "script bash started execution..."
#directory for client

dira="cliente"${1}
echo "${dira}"

#show progress bar copy to client folder
if sudo rsync -ah --progress /home/mario3/arinapin/coral-flash/script_despliegue/pru1 /home/mario3/arinapin/coral-flash/script_despliegue/cliente$1; then
   echo "copied successfully"
else
   echo "error"
  exit 1
fi

#This scripts will create the image for the user, using the models they have obtained. 
#The obtained image is ready to be used when flashed on any google coral dev board.


