#Esta es la versión a utilizar, no hay que usar cloud functin
#Este script va a obtener el modelo y las labels del cliente. 
import sys
import os

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

    #U
    if client_id  no tiene carpeta -> crear carpeta.callable    
            otherwise meter en carpeta
#Create client
#def client_number():


