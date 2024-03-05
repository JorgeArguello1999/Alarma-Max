from fastapi import FastAPI, WebSocket
from firebase import alarm_is_on

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Ruta WebSocket para manejar las conexiones WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Intenta convertir el dato a un entero
                idsector = int(data)
                # Ejecuta la función alarm_is_on con el número proporcionado
                value = alarm_is_on(str(idsector))
                # Envía el valor obtenido al cliente
                await websocket.send_text(str(value))

            except ValueError:
                # Si no se pudo convertir a entero, envía un mensaje de error al cliente
                await websocket.send_text("Por favor, envíe un número válido.")

    except Exception as e:
        print(e)
        websocket.close()
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)