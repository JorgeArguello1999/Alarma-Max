import asyncio
import websockets

async def main():
    # uri = "ws://localhost:8000/ws"  # Asegúrate de reemplazar localhost con la dirección correcta si es necesario
    # uri = "ws://server-ojievlbbua-uk.a.run.app/ws"  # Asegúrate de reemplazar localhost con la dirección correcta si es necesario
    uri = "ws://server-ojievlbbua-uk.a.run.app/"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                # Envía un mensaje al servidor
                message = input("Ingrese el número del sector: ")
                await websocket.send(message)

                # Espera la respuesta del servidor
                response = await websocket.recv()
                print(f"Respuesta del servidor: {response}")

            except KeyboardInterrupt:
                break

asyncio.run(main())