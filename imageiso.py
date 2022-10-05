#Esta es la versión a utilizar, no hay que usar cloud functin
#Este script va a obtener el modelo y las labels del cliente. 


def model():    
    GCLOUD_PATH = '/tmp/'
    db = firestore.Client(project='mvp-arin')
    doc=str(event['value']['name'].rsplit('/',1)[1])
    doc_ref = db.collection(u'projects').document(doc)
    #print("\n\n --", str(event['value']['fields']))


    #obtener el odmodelo
    event['sdpdw']['modelo']
    event['¡dslsdñl']['value']

    #h

def path():
