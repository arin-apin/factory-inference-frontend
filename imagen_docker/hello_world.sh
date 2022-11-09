#!/bin/bash

#TBD: FIRST CREATE A COPY OF THE IMAGE! Otherwise the changes are applied to the image 
#Change to losetup-f
#Change model and labels.
#Add copy progress
#Python create client directory

#directory for client (take to python?)
mkdir cliente2

echo "script bash started execution..."
#directory for client

dira="cliente"${1}
echo "${dira}"

#show progress bar copy to client folder
if sudo rsync -ah --progress /Despliegue /cliente_test; then
   echo "copied successfully"
else
   echo "error"
   exit 1
fi

#This scripts will create the image for the user, using the models they have obtained. 
#The obtained image is ready to be used when flashed on any google coral dev board.

#First, we create the partition from our image. 
#-f asigns a free device, but we dont know which one without checking
sudo losetup -fo 142606336 --sizelimit=7440695296 cliente2/modelo-coral.img
losetup -a 

#To be added 
#losetup -f gives the next free device

#To see which position loop is at 
if losetup | grep -q 'modelo-coral'; then
   echo "matched with loop "
else
   echo "Doesn't exist matching dev/loop, losetup failed"
   exit 1   
fi

output1=$(sudo losetup | grep modelo-coral | awk {'print'} | cut -d ' ' -f1)
echo $output1

#findmnt $output1

#Create directory for mount
sudo mkdir /media/image-coral

#mount the image
if sudo mount $output1 /media/image-coral; then
   echo "montada"
else
   echo "Doesn't exist, losetup failed"
fi

#Now we can copy the files, python script, labels and models. 

#This should be deleted, that folder is a wip 
#sudo cp -i /home/mario3/arinapin/python/git/factory-inference-frontend/interfaz_coral.py /home/mario3/arinapin/python/git/factory-inference-frontend/ImageNetLabels.txt /home/#mario3/arinapin/python/git/factory-inference-frontend/lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_default_1\ \(1\).tflite /media/image-coral/home/mendel/

#The images and assets for the interface
sudo rsync -aP /home/mario3/arinapin/python/git/interfaz-ok /media/image-coral/home/mendel/

#The service to run the interface
#sudo cp /home/mario3/arinapin/coral-flash/script_despliegue/interface.service /media/image-coral/lib/systemd/system/

#Activate service
#sudo systemctl enable interface.service

#Create symbolic link equivalent to enable
#sudo ln -s /media/image-coral/lib/systemd/system/interface.service /etc/systemd/system/multi-user.target.wants

#Once we have finished moving files, end the mount and remove the loop 
# -d: deletes loop 

sudo umount -d /media/image-coral/


#DESCARGAR
echo "image ready for clients..."

#Once it is completed, we delete the copy
#sudo rm -r /cliente1


#to delete the block file
#rm ~/TO_BLOCK 
