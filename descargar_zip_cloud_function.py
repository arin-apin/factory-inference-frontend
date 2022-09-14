import fnmatch
from genericpath import isfile
from google.cloud import storage
import os
import tensorflow as tf
import json
import zipfile
#from google.cloud import firestore
#from google.oauth2 import service_account
import fnmatch
import os
import imghdr
import cv2


JOB = os.getenv('JOB')
PROJECT_PATH = os.getenv('PROJECT_PATH')
imgs_dir = '/tmp/'+PROJECT_PATH

def list_blobs(path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("mvp-arin.appspot.com")
    #blob = bucket.blob(bucketFolder + file)
    #blob.upload_from_filename(localFile)
    return bucket.list_blobs(prefix=path)

def folder_check(path):
###Cuenta el numero de carpetas, si hay 2 o mas categorias para ML

    print(os.listdir(path))
    file=os.listdir(path)
    if len(file) >= 2: 
        print("2 o más ficheros")

    else:
        print("Faltan categorías, error")
       

def check_images(s_dir, ext_list):
#Comprobación de las imágenes en el directorio
    bad_images = []
    bad_ext = []
    s_list = os.listdir(s_dir)
    for cate in s_list:
        klass_path = os.path.join(s_dir, cate)
        print('processing class directory ', cate)
        #Klass_path debe ser un directorio
        if os.path.isdir(klass_path):
            file_list = os.listdir(klass_path)
            #Recorremos el listado de ficheros en el klass_path
            for f in file_list:
                f_path = os.path.join(klass_path,f)
                tip = imghdr.what(f_path)
                if ext_list.count(tip) == 0:
                    bad_images.append(f_path)

                #Comprobamos que sea un archivo
                if os.path.isfile(f_path):
                    try:
                        img = cv2.imread(f_path)
                        shape = img.shape

                    except:
                        print('file ', f_path, 'is not a valid image file')
                        bad_images.append(f_path)

                else:
                    print('*** Error, you have a subdirectory ', f ,'in class directory', cate)
        else:
            pass
            #Si s_dir tiene archivos se cumple este else
            #print("*** Error you have files in ", s_dir , "should only contain directories")
    return bad_images, bad_ext


def contar_imagenes(path):
    n_files=0
    min_files =20
    res = 0
    for file in os.listdir(path):
        f_path = os.path.join(path,file)
        if os.path.isfile(f_path):
            n_files +=1

    if n_files >= min_files:
        print("We have enough files to continue ", min_files)
        res=1
    else:
        print("Error we need at least ", min_files, "files")
    return res


#Main

print('---------------------> Abriendo:', PROJECT_PATH)
os.makedirs('/tmp/'+PROJECT_PATH, exist_ok=True)
for blob in list_blobs(PROJECT_PATH):
    if blob.name.endswith("zip"):
        print('---------------------> Descargando:', blob.name)
        blob.download_to_filename('/tmp/'+blob.name)
        
        with zipfile.ZipFile('/tmp/'+blob.name, 'r') as zip_ref:
            print('---------------------> Descomprimiendo:', blob.name)
            zip_ref.extractall('/tmp/'+PROJECT_PATH)


#Comprobación de que hay 2 o mas carpetas
res = folder_check(imgs_dir)

#Si da el ok, comprobar que la extensión es correcta de los ficheros en las carpetas extraidas y que hay  > 20 imágenes
dirlist = [item for item in os.listdir(imgs_dir) if os.path.isdir(os.path.join(imgs_dir,item))]
print(dirlist)

#list of acceptable extensions
good_exts = ['jpg', 'png', 'jpeg', 'gif', 'bmp']


bad_file_list, bad_ext_list = check_images('/tmp/'+PROJECT_PATH, good_exts)
if len(bad_file_list) != 0:
    print('improper image files are listed below')
    for i in range(len(bad_file_list)):
        print(bad_file_list[i])
else:
    print(' no improper image files were found')


#ELiminar lo de arriba no nos sirve. 

#Contar que haya >= 20 imágenes por categoría.

for folder in dirlist:
    valor = contar_imagenes(folder)

#una vez comprobadas poner imgs_processed_nok
#Modificar esto en el futuro.
if valor == 1: 
    print('Todo ok')
    doc_ref.update({u'status': u'imgs_processed_nok'})

else: 
    print('Error, numero de ficheros por debajo')
    doc_ref.update({u'status': u'imgs_processed_nok'})

