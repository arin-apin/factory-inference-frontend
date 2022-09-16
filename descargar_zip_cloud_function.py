from distutils.command.build_clib import build_clib
import fnmatch
from genericpath import isfile
from math import radians
from google.cloud import storage
import os
import json
import zipfile
from pathlib import Path
#from google.cloud import firestore
#from google.oauth2 import service_account
import fnmatch
import os
import shutil
import glob
import imghdr

JOB = os.getenv('JOB')
PROJECT_PATH = os.getenv('PROJECT_PATH')

GCLOUD_PATH= '/tmp/'
imgs_dir = GCLOUD_PATH+PROJECT_PATH

print(imgs_dir)

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
       

# def check_images(s_dir, ext_list):
# #Comprobación de las imágenes en el directorio
#     bad_images = []
#     bad_ext = []
#     s_list = os.listdir(s_dir)
#     for cate in s_list:
#         klass_path = os.path.join(s_dir, cate)
#         print('processing class directory ', cate)
#         #Klass_path debe ser un directorio
#         if os.path.isdir(klass_path):
#             file_list = os.listdir(klass_path)
#             #Recorremos el listado de ficheros en el klass_path
#             for f in file_list:
#                 f_path = os.path.join(klass_path,f)
#                 tip = imghdr.what(f_path)
#                 if ext_list.count(tip) == 0:
#                     bad_images.append(f_path)

#                 #Comprobamos que sea un archivo
#                 if os.path.isfile(f_path):
#                     try:
#                         img = cv2.imread(f_path)
#                         shape = img.shape

#                     except:
#                         print('file ', f_path, 'is not a valid image file')
#                         bad_images.append(f_path)

#                 else:
#                     print('*** Error, you have a subdirectory ', f ,'in class directory', cate)
#         else:
#             pass
#             #Si s_dir tiene archivos se cumple este else
#             #print("*** Error you have files in ", s_dir , "should only contain directories")
#     return bad_images, bad_ext



def contar_imagenes(path):
    #Función para contar el número de imágenes en la carpeta.
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


def upload_from_directory(directory_path: str, destination_bucket_name: str, destination_blob_name: str):
   #Directoy path el directorio donde se encuentran los ficheros, (local aqui)
   # #dest_bucket_name es el nombre del bucket creado en el storage online
   # y destination_blob_name es la carpeta o directorio que se va a crear en la nube
    rel_paths = glob.glob(directory_path + '/**', recursive=True)
    print(rel_paths)
    #el nombre de donde
    bucket = storage_client.get_bucket(destination_bucket_name)
    for local_file in rel_paths:
        #EN remote_path se guardan los ficheros en la nube
        #remote_path = f'{destination_blob_name}/{"/".join(local_file.split(os.sep)[2:])}'
        
        p = Path(local_file)
        remote_path = Path(*p.parts[2:])
        print(remote_path)
        print(local_file)
        if os.path.isfile(local_file) == 1:
            blob = bucket.blob(str(remote_path))
            blob.upload_from_filename(local_file)



## --- Main program execution ---##


print('---------------------> Abriendo:', PROJECT_PATH)
os.makedirs('/tmp/'+PROJECT_PATH, exist_ok=True)
for blob in list_blobs(PROJECT_PATH):
    print("blob:",blob.name)
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

#He quitado el de gcloud_PATH de aqui, para trabajar fuera de la nube
path_folders_img = [PROJECT_PATH+'/'+item for item in dirlist ]
print("FULL PATH: ", path_folders_img )


#list of acceptable extensions
good_exts = ['jpg', 'png', 'jpeg', 'gif', 'bmp']


#Comprobación del tipo de imagen.
# bad_file_list, bad_ext_list = check_images('/tmp/'+PROJECT_PATH, good_exts)
# if len(bad_file_list) != 0:
#     print('improper image files are listed below')
#     for i in range(len(bad_file_list)):
#         print(bad_file_list[i])
# else:
#     print(' no improper image files were found')


#ELiminar lo de arriba no nos sirve. 

#Contar que haya >= 20 imágenes por categoría.

for folder in path_folders_img:
    valor = contar_imagenes(GCLOUD_PATH+folder)

#una vez comprobadas poner imgs_processed_nok
#Modificar esto en el futuro.
# if valor == 1: 
#     print('Todo ok')
#     doc_ref.update({u'status': u'imgs_processed_nok'})

# else: 
#     print('Error, numero de ficheros por debajo')
#     doc_ref.update({u'status': u'imgs_processed_nok'})


#copiar contenido a firebase. Se sube desde local, la carpeta del path con etc

storage_client = storage.Client()
#bucket = storage_client.get_bucket("mvp-arin-train-images")




for folder in path_folders_img:
    print(os.path.basename(os.path.normpath(folder)))
    upload_from_directory(GCLOUD_PATH+folder, "mvp-arin.appspot.com", os.path.basename(os.path.normpath(folder)))
    print("carpeta subida")

#Deberían borrarse ficheros de la carpeta tmp
#  const bucket = admin.storage().bucket()
#  const path = "path/to/file.wav"
#  return bucket.file(path).delete()

    for folder in path_folders_img:
        try:
            shutil.rmtree("tmp/"+PROJECT_PATH+folder)

        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
