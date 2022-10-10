#Esta es la versión a utilizar, no hay que usar cloud function
#Este script va a obtener el modelo y las labels del cliente. 
import sys
import os
import subprocess
import shutil

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Arguments {i:>6}: {arg}")

    if len(sys.argv)!=3:
        print("We requiere 3 arguments, client_id, model and label for the client \n We dont have the correct amount")
        exit()

    else:
        print("Proceding to generate iso image")


    #We create a folder for the corresponding 
    ID = sys.argv[1]
    modelo = sys.argv[2]
    labels = sys.argv[3]

    #Note: Only one image per client, this will be changed in the future
    dir = os.path.join("C:\\", "home", "coral-flash","cliente"+str(ID))
    if not os.path.exists(dir):
        os.mkdir(dir)

    #Save in folder the files
    #Pregnuntar a pablo si hay que copiar los ficheros, descargarlos o como es eso. 

    model_path= os.path.join 
    #path del modelo y label



    #Once created copy file to folder, with script. 
    #arg1 = clienteID
    #Arg2 = Model trained for client
    #Arg3 = labels
    val = subprocess.check_call("./script-load-image.sh '%s'" % (str(arg1),str(arg2),str(arg3)), shell=True)

    #shell=True not really needed with script defined with path to shell (#!/bin/bash)

