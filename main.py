from fastapi import FastAPI
import uvicorn

from firebase import alarm_is_on

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Obtener si la alarma esta encendida
@app.get("/")
async def read_root(idsector:str):
    value = alarm_is_on(idsector)
    return {"alarm": value}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)