import network
import time
import urequests
from machine import Pin

# Configurar la conexión WiFi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando a la red WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        
    print('Conexión WiFi exitosa')
    print('Dirección IP:', wlan.ifconfig()[0])

# Función para realizar la solicitud GET
def make_get_request(url):
    try:
        response = urequests.get(url)
        return response.json()
        response.close()
        
    except Exception as e:
        print('Error al realizar la solicitud:', e)

# Función para encender la sirena
def sirena_on():
    pin = Pin(12, Pin.OUT)  # Configurar el pin 12 como salida
    pin.on()                # Encender la sirena
    print('Sirena encendida')
    time.sleep(60)          # Esperar 12 segundos
    pin.off()               # Apagar la sirena
    print('Sirena apagada')

# Configurar la conexión WiFi
SSID = "TECNICO"
PASSWORD = "DTC.2020"
connect_wifi(SSID, PASSWORD)

# URL para la solicitud GET
URL = "http://192.168.11.114:8000/?idsector=5"

# Realizar la solicitud GET y encender la sirena cada 15 segundos
last_time = ""
while True:
    output = make_get_request(URL)
    
    time_alarm = output['alarm']['alarm_time']
    alarm_is_on = output['alarm']['alarm']
    
    print(alarm_is_on)
    
    if last_time == "":
        last_time = time_alarm
        print("Inicio")
    
    if time_alarm != last_time and last_time != "":
        if alarm_is_on:
            last_time = time_alarm
            sirena_on()
            print(True)
        
    elif time_alarm == last_time:
        print("Ya sono")
        
    else:
        print("Error")
        
    time.sleep(2)