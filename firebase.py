from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.firestore_v1.base_query import FieldFilter

import firebase_admin

# Cargamos variables de entorno
from dotenv import load_dotenv
from os import getenv
load_dotenv()

# Inicializar la aplicación Firebase con las credenciales del archivo JSON
route = getenv('FIREBASE_DIR')
cred = credentials.Certificate(route)
firebase_admin.initialize_app(cred)

def alarm_is_on(idsector:str = 5) -> dict:
    """
    idsector -> str -> Sector al que se va a escuchar
    """

    # Obtener una referencia a la base de datos Firestore
    db = firestore.client()
    collection = db.collection('alarmas')
    query = collection.where(filter=FieldFilter('idsector', '==', str(idsector)))
    order = query.order_by('fechahora', direction=firestore.Query.DESCENDING)
    limit = order.limit(1)
    result = limit.stream()

    # Obtenemos los valores 
    items = [ item.to_dict() for item in result ]

    try:
        if items[0]['sirena'] == '1' or items[0]['sirena'] == 1:
            output = True
        else:
            output = False

    except Exception as e:
        output = "No key Sirena"
        
    return {
        "alarm": output
    }


if __name__ == "__main__":
    print(alarm_is_on(5))