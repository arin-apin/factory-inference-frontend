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
import shutil

#Defined in requirements the packages. 
#This works for labelling, update for segmentation

storage_client = storage.Client()
#folder where we will save the blob from firebase

def hello_firestore(event, context):
    
    #Is it possible to store files in the cloud function memory inside the tmp folder
    GCLOUD_PATH = '/tmp/'
    db = firestore.Client(project='mvp-arin')
    doc=str(event['value']['name'].rsplit('/',1)[1])
    doc_ref = db.collection(u'projects').document(doc)
    #print("\n\n --", str(event['value']['fields']))

    
    #We check if the field zip exists in the json file from the event and if it has been created from the last oldValue. We have an example in git
    if 'zip' in event['value']['fields'] and not 'zip' in event['oldValue']['fields']:
        print('Campo zip actualizado')
        #Update the status to imgs_processing in the collection projects
        doc_ref.update({u'status': u'imgs_processing'})
        storage_client = storage.Client()
        #We get the bucket with the zipfile
        bucket = storage_client.get_bucket("mvp-arin.appspot.com")
        blob = bucket.blob(event['value']['fields']['path']['stringValue']+'/'+event['value']['fields']['zip']['stringValue'])
        if blob.exists():
            print('Zip encontrado')

            #We take the path from the blob.name 
            #si se pone el blob.name te va a crear un directorio, entonces no te deja descargar
            print(os.path.dirname(blob.name))
            path_file = os.path.dirname(blob.name)
            #We need to create the directory, in the tmp folder. 
            os.makedirs('/tmp/'+path_file, exist_ok=True)


            zipbytes = io.BytesIO(blob.download_as_string())
            #if the file is a zip 
            if is_zipfile(zipbytes):
                print('Es fichero zip')
                print("blob:", blob.name)
                print('---------------------> Descargando:', blob.name)
                blob.download_to_filename('/tmp/'+blob.name)

                RUTA_OFF= GCLOUD_PATH+path_file
        
                with ZipFile('/tmp/'+blob.name, 'r') as zip_ref:
                    print('---------------------> Descomprimiendo:', blob.name)
                    zip_ref.extractall(RUTA_OFF)

                #Count the number of directories
                res = folder_check(RUTA_OFF)

                #Create route for every file in GCLOUD_PATH, make sure they are folder 
                dirlist = [item for item in os.listdir(
                    RUTA_OFF) if os.path.isdir(os.path.join(RUTA_OFF, item))]
                

                #We want the path to every image category
                path_folders_img = [RUTA_OFF+'/'+item for item in dirlist]
                print("FULL PATH: ", path_folders_img)

                #Count the number of images per directory it should be at least >8
                for folder in path_folders_img:
                    valor = contar_imagenes(folder)

                #Upload files to firebase from google clound tmp folder, for each category. 
                for folder in path_folders_img:
                    print(os.path.basename(os.path.normpath(folder)))
                    upload_from_directory(folder, "mvp-arin.appspot.com",
                                    os.path.basename(os.path.normpath(folder)))
                    print("1 carpeta subida")
                
                #We have to update the status to ok in the project->status collection (database)
                doc_ref.update({u'status': u'imgs_processed_ok'})
                
                #Once uploaded, delete from tmp directory
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
    #Count the number of directories, if there are 2 or more categories for categorisation
    file = os.listdir(path)
    if len(file) >= 2:
        print("2 o más directorios")
    else:
        print("Faltan categorías, error")


def contar_imagenes(path):
    #Function for counting the number of images inside the directory which is equivalent to a category

    n_files=0
    min_files = 8
    res = 0
    for file in os.listdir(path):
        f_path = os.path.join(path,file)
        if os.path.isfile(f_path):
            n_files +=1

    if n_files > min_files:
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
        if os.path.isfile(local_file) == 1:
            blob = bucket.blob(str(remote_path))
            blob.upload_from_filename(local_file)