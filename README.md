# Alarma-Max

Codigo de `ESP32` para poder conectarse a `Firebase` con la librearía `Firebase_ESP_Client`.

Este proyecto busca encender una sirena, o cualquier otro dispositivo a través de Firebase.

## Configuraciones antes de iniciar
Para iniciar tendremos que configurar tanto las credenciales de RED como las necesarias para registrarnos en la aplicación (Correo)

```c++
/* 1. Define las credenciales WiFi */
#define WIFI_SSID ""
#define WIFI_PASSWORD ""

/* 2. Define la clave API */
#define API_KEY ""

/* 3. Define el ID del proyecto */
#define FIREBASE_PROJECT_ID ""

/* 4. Define el correo electrónico y la contraseña del usuario que ya está registrado o agregado en tu proyecto */
#define USER_EMAIL ""
#define USER_PASSWORD ""
```

Después vamos a configurar el puerto donde estara conectado el control del RELAY, que valor espera en el campo SIRENA y a que sector pertenece en formato texto.
```c++
// PIN RELAY
const int RELAY = 12;

// Zona de la sirena y Sirena valor
const String SECTOR = "5";
const int SIRENA = 1;
```

El código carga solo el último registro de la base de datos que coincida con el sector, debido a que el ESP32 puede variar la configuración de la Hora si es apagado o reiniciado.

En esta sección del código podemos configurar la duración de la Alarma.
```c++
      // Encendemos la alarma
      if(fecha != last_time && sirena == SIRENA && last_time != ""){
        Serial.println("Encendido, " + fecha);
        last_time = fecha;
        
        // Encendemos la sirena
        digitalWrite(RELAY, HIGH);
        delay(20000); // -> Tiempo en Milisegundos (20seg)
        digitalWrite(RELAY, LOW);
      }
```

## Librerias de Arduino
 - Firebase_ESP_Client (4.4.12 by mobizt)
 - ArduinoJson (0.2 by Benoit)

## Prototipo (Imagen)
> Las fuentes de poder son solo ejemplo.
![Prototipo](images/Prototipo.png)

### Materiales
 - ESP32
 - Modulo RELAY 12V
 - Fuente de alimentación 5V (ESP32)
 - Fuente de alimentación 12V (Sirena)

## Esquema (Imagen)
![Esquema](images/Esquemático.png)

## PCB (Imagen)
![PCB](images/PCB.png)

> Para el diagrama utilizar la aplicación `Fritzing`