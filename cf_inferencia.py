from google.cloud import firestore
from google.cloud import storage
from numpy import asarray
import tflite_runtime.interpreter as tflite
from PIL import Image as ImagePIL
import io
import os
import numpy as np
import shutil
global size, labels

test_model = 'test_model.tflite'
test_labels = 'test_labels.txt'
test_img = 'car.jpg'
def hello_firestore(event, context):

     """Triggered by a change to a Firestore document.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     resource_string = context.resource
     # print out the resource string that triggered the function
     print(f"Function triggered by change to: {resource_string}.")
     # now print out the entire event object
     print(str(event))

     db = firestore.Client(project='mvp-arin')
     doc=str(event['value']['name'].rsplit('/',1)[1])
     doc_ref = db.collection(u'deployments').document(doc)

     if 'inferencia' in event['updateMask']['fieldPaths']:
          print('Campo inferencia actualizado en el deployment')
          if event['value']['fields']['inferencia']['stringValue']=="hacer":
               print("realizando inferencia...")
               storage_client = storage.Client()
               bucket = storage_client.get_bucket("mvp-arin.appspot.com")
               blob = bucket.blob("modelo_test"+'/'+test_model)
               if blob.exists():
                    print('Modelo encontrado')
               
                    #We take the path from the blob.name 
                    #si se pone el blob.name te va a crear un directorio, entonces no te deja descargar
                    print(os.path.dirname(blob.name))
                    path_file = os.path.dirname(blob.name)
                    #We need to create the directory, in the tmp folder. 
                    os.makedirs('/tmp/test/'+path_file, exist_ok=True)
                    blob.download_to_filename('/tmp/test/'+blob.name)
                    modelo_test = '/tmp/test/'+blob.name
               else: 
                    print("model not found")
               
               blob = bucket.blob("modelo_test"+'/'+test_labels)
               if blob.exists():
                    print('labels encontrado')
                    #blob.download_to_filename('/tmp/test/'+blob.name)
                    with blob.open("r") as f:
                         labels=str(f.read()).splitlines()
                    #labels = '/tmp/test/'+blob.name
               else: 
                    print('label not found')

               blob = bucket.blob("modelo_test"+'/'+test_img)
               if blob.exists():
                    print(blob.name)
                    imagen = blob.download_to_filename('/tmp/test/'+blob.name)
                    imagen = '/tmp/test/'+blob.name
                    
                    print('img found, starting inference')
                    resultado, resultado_max = inferencia(imagen, modelo_test, labels)
                    #print("Resultado de la inferencia a la imagen: ", resultado)
                    print('Resultado más probable: ', resultado_max)
                    print('top 5 results:, resultado')

               else: 
                    print("not found model nor labels")

          else: 
               print("not inferencia hacer")

     else:
          print('inferencia not updated')


def inferencia(img, model, labels):
     print('labels:', labels)
     global interpreter, input_details, output_details
     img_infe = ImagePIL.open(img)
     interpreter = tflite.Interpreter(model)
     #experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
     interpreter.allocate_tensors()
     input_details = interpreter.get_input_details()
     output_details = interpreter.get_output_details()
     _, height, width, _ = interpreter.get_input_details()[0]['shape']
     # print('tensor input', input_details)
     size = [width, height] 
     img= img_infe.convert('RGB').resize(size, ImagePIL.ANTIALIAS)
     input_data = np.array(asarray(img), dtype=np.float32)
     input_data = np.expand_dims(input_data , axis=0)
     interpreter.set_tensor(input_details[0]['index'], input_data)
     interpreter.invoke()
     tensor_resultado= interpreter.get_tensor(output_details[0]['index'])[0]
     top_k = tensor_resultado.argsort()[-5:][::-1]
     #print(top_k)
     # for i in range(len(labels)):
     #     print('{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i]))
    #We get the top 5 results 
     resultado=''
     #print(top_k)
     for i in top_k:
        resultado+=('{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i]))+"\n"
     resultado=resultado+"Tiempo inferencia: "+str(time.time()-inicio)
     #print(resultado, '\n')
     resultado_max= resultado.partition('\n')[0]+'\n'+ resultado.split('\n')[-1] 
     return resultado_max, resultado

  


