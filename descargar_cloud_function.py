from importlib.resources import path
from google.cloud import storage
from google.cloud import firestore
from zipfile import ZipFile
from zipfile import is_zipfile
import io
import os
from pathlib import Path
import fnmatch
import os
import glob
import sys
import shutil
#Esta es la versión a utilizar en cloudfunction

storage_client = storage.Client()
#folder where we will save the blob from the firebase



def hello_firestore(event, context):
    
    GCLOUD_PATH = '/tmp/'
    db = firestore.Client(project='mvp-arin')
    doc=str(event['value']['name'].rsplit('/',1)[1])
    doc_ref = db.collection(u'projects').document(doc)
    if 'zip' in event['value']['fields'] and not 'zip' in event['oldValue']['fields']:
        print('Campo zip actualizado')
        doc_ref.update({u'status': u'imgs_processing'})
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("mvp-arin.appspot.com")
        blob = bucket.blob(event['value']['fields']['path']['stringValue']+'/'+event['value']['fields']['zip']['stringValue'])
        if blob.exists():
            print('Zip encontrado')
            zipbytes = io.BytesIO(blob.download_as_string())
            if is_zipfile(zipbytes):
                print('Es fichero zip')
  
                print('---------------------> Descargando:', blob.name)
                blob.download_to_filename('/tmp/'+blob.name)
        
                with ZipFile('/tmp/'+blob.name, 'r') as zip_ref:
                    print('---------------------> Descomprimiendo:', blob.name)
                    zip_ref.extractall(GCLOUD_PATH)

                #contar el numero de carpetas
                res = folder_check(GCLOUD_PATH)

                #Crear la ruta a cada objeto en GCLOUD_PATH, asegurar que son carpetas 
                dirlist = [item for item in os.listdir(
                    GCLOUD_PATH) if os.path.isdir(os.path.join(GCLOUD_PATH, item))]
                
                #Testear dir_list para ver que pone

                #He quitado el de gcloud_PATH de aqui, para trabajar fuera de la nube
                path_folders_img = [GCLOUD_PATH+'/'+item for item in dirlist]
                print("FULL PATH: ", path_folders_img)

                #Contar el número de imágenes por carpeta debe ser >20
                for folder in path_folders_img:
                    valor = contar_imagenes(GCLOUD_PATH+folder)

                #cambiar en el futuro
                doc_ref.update({u'status': u'imgs_processed_nok'})


                #Subida a firebase desde google cloud tmp

                for folder in path_folders_img:
                    print(os.path.basename(os.path.normpath(folder)))
                    upload_from_directory(GCLOUD_PATH+folder, "mvp-arin.appspot.com",
                                    os.path.basename(os.path.normpath(folder)))
                    print("1 carpeta subida")

                #Una vez subidas, borrar de tmp
                for folder in path_folders_img:
                    try:
                        shutil.rmtree(folder)

                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))


            else:
                print('No parece zip')
                doc_ref.update({u'status': u'imgs_processed_nok'})
        else:
            print('Zip no encontrado')
            doc_ref.update({u'status': u'imgs_processed_nok'})
    else:
        print('Zip no actualizado')


def folder_check(path):
    ###Cuenta el numero de carpetas, si hay 2 o mas categorias para ML

    print(os.listdir(path))
    file = os.listdir(path)
    if len(file) >= 2:
        print("2 o más ficheros")

    else:
        print("Faltan categorías, error")


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
    #el nombre de donde saco los ficheros del storage
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