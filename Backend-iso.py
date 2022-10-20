#Esta es la versión a utilizar, no hay que usar cloud function
#This script is going to obtain the model and labels for the client
import sys
import os
import subprocess
import shutil
from importlib.resources import path
from google.cloud import storage
from google.cloud import firestore
from firebase_admin import credentials, initialize_app, storage
import glob

creds = credentials.Certificate("/home/mario3/arinapin/python/api-key-dracones02.json")
initialize_app(creds, {'storageBucket':'mvp-arin'})
 
#export PROJECT_PATH="clients/q6FvDq3pIxV4sVjE7qZfCTSn9Wx2/URirWG09ZYWzRwqdA9vm"
#export GOOGLE_APPLICATION_CREDENTIALS=/home/mario/arinapin/api-key-dracones02.json

files = glob.glob('/home/mario3/')


if __name__ == "__main__":
    #Argument count
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Arguments {i:>6}: {arg}")

    if len(sys.argv)!=4:
        print("We requiere 3 arguments, client_id, model and label for the client \n We dont have the correct amount")
        exit()

    else:
        print("Proceding to generate iso image")


    #Store the arguments.
    #arg1 = clienteID
    #Arg2 = Model trained for client
    #Arg3 = labels
    ID = sys.argv[1]
    modelo = sys.argv[2]
    labels = sys.argv[3]

    #We create a folder for the corresponding client
    #Note: Only one image per client, this will be changed in the future
    dir = os.path.join("/home","mario3","arinapin", "coral-flash","script_despliegue","cliente"+str(ID))
    print(dir)
    if not os.path.exists(dir):
        #os.makedirs(dir)
        os.mkdir(dir)
        #print('directory created)

    #Save in folder the files
    #Pregnuntar a pablo si hay que copiar los ficheros, descargarlos o como es eso. 

    #model_path= os.path.join 
    #path del modelo y label

    #Once created copy file to folder, with script. 

    #val = subprocess.check_call("./script-load-image.sh '%s'" % (str(arg1),str(arg2),str(arg3)), shell=True)
    
    #Important to separate arguments correctly, or removel shell=True so it works with only comma separation
    #shell=True not really needed with script defined with path to shell (#!/bin/bash)
    
    os.system("./script-load-image2.sh {} {} {}".format(str(ID),str(modelo),str(labels)))    
    #val = subprocess.check_call("./script-load-image2.sh %s  %s  %s" % (str(ID),str(modelo),str(labels)), shell=True)



