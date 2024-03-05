# Alarma-Max

Este proyecto crea una API REST con `FASTAPI` y con `Firebase Firestore` que tiene finalidad devolver el estado de una alarma que sera consumida a través de `ESP32`

# FASTAPI (Python)
Primero vamos a instalar las dependencias:
```bash
pip install -r requeriments.txt
``` 

También debemos tener nuestro archivo `JSON` de `Firebase` que esta en la ruta `.tokens/`:
```
├── firebase.py
├── main.py
├── README.md
├── requirements.txt
└── tokens
    └── alarm-max.json -> JSON Credencial
```

Deberemos crear un archivo `.env` el cual debemos tener la siguiente estructura:
```bash
FIREBASE_DIR=.tokens/alarm-max.json
# La dirección debe apuntar a la ruta donde se encuentra tu JSON Credencial
```

# Arduino