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

# Obtener la fecha actual 
from datetime import datetime

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
        # Verificamos si es un valor reciente o no 
        # Verificamos si la sirena se debe encender
        # if items[0]['sirena'] == '1' or items[0]['sirena'] == 1:
        if items[0]['nusuario'] == 'ALEXIS BALSECA':
            output = True
        else:
            output = False

    except Exception as e:
        output = "No key Sirena"


    # Hora servidor
    fecha = items[0]['fechahora']
    # Hora del sistema
    now = datetime.now(fecha.tzinfo)
    # Calculamos la diferencia entre las fechas
    diff = now - fecha

    # Si la diferencia es inferior a 20 segundos, is_now será True, de lo contrario False
    is_new = diff.total_seconds() <= 20
        
    return {
        "alarm": output,
        "is_new": is_new,
        "alarm_time": fecha,
        "server_time": now,
        "time_difference": diff
    }


if __name__ == "__main__":
    import time
    while True:
        print(alarm_is_on(5))
        time.sleep(5)