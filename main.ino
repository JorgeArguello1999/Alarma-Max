#include <ArduinoJson.h>
#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>

// Proporciona la información del proceso de generación de token.
#include <addons/TokenHelper.h>

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

// Define el objeto de datos de Firebase
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long dataMillis = 0;

// PIN RELAY
const int RELAY = 12;

// Zona de la sirena y Sirena valor
const String SECTOR = "5";
const int SIRENA = 1;

void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }

  Serial.print("Conectado con IP: ");
  Serial.println(WiFi.localIP());

  Serial.printf("Cliente de Firebase v%s\n\n", FIREBASE_CLIENT_VERSION);

  // Asigna el host del proyecto y la clave API (requerido)
  config.api_key = API_KEY;

  // Asigna las credenciales de inicio de sesión del usuario
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback;  // ver addons/TokenHelper.h

  // Reestablece la red WiFi si se desconecta
  Firebase.reconnectNetwork(true);

  // Ajusta el tamaño del búfer SSL
  fbdo.setBSSLBufferSize(4096, 1024);

  // Limita el tamaño del payload de respuesta
  fbdo.setResponseSize(2048);

  Firebase.begin(&config, &auth);

  // Configuramos PIN 12 para salida de RELAY
  pinMode(RELAY, OUTPUT);

  Serial.println("Consultando la base de datos de Firestore... ");
}

String last_time = "";
void loop() {
  if (Firebase.ready() && (millis() - dataMillis > 5000 || dataMillis == 0)) {
    dataMillis = millis();

    FirebaseJson query;
    // Colección
    query.set("from/collectionId", "alarmas");

    // Campos a utilizar
    query.set("select/fields/[0]/fieldPath", "idsector");
    query.set("select/fields/[1]/fieldPath", "sirena");
    query.set("select/fields/[2]/fieldPath", "fechahora");

    // En qué orden utilizarlos
    query.set("orderBy/field/fieldPath", "fechahora");
    query.set("orderBy/direction", "DESCENDING");

    // Filtro sector
    query.set("where/fieldFilter/field/fieldPath", "idsector");
    query.set("where/fieldFilter/op", "EQUAL");
    query.set("where/fieldFilter/value/stringValue", SECTOR);

    // Limitamos los items
    query.set("limit", 1);

    if (Firebase.Firestore.runQuery(&fbdo, FIREBASE_PROJECT_ID, "", "/", &query)) {
      // Imprimimos las respuestas
      // Serial.printf("ok\n%s\n\n", fbdo.payload().c_str());

      DynamicJsonDocument doc(2048);
      DeserializationError error = deserializeJson(doc, fbdo.payload());

      if (error) {
        Serial.print("Error al parsear el JSON: ");
        Serial.println(error.c_str());
        return;
      }

      // Para el registro 0
      String fecha = doc[0]["document"]["fields"]["fechahora"]["timestampValue"].as<String>();
      
      int sirena = 0;
      if (doc[0]["document"]["fields"]["sirena"].containsKey("integerValue")) {
        sirena = doc[0]["document"]["fields"]["sirena"]["integerValue"].as<int>();
      }

      // Encendemos la alarma
      if(fecha != last_time && sirena == SIRENA && last_time != ""){
        Serial.println("Encendido, " + fecha);
        last_time = fecha;
        
        // Encendemos la sirena
        digitalWrite(RELAY, HIGH);
        delay(20000);
        digitalWrite(RELAY, LOW);
      }

      if(last_time == ""){
        last_time = fecha;
        Serial.println("Cargando último registro: " + fecha);
      }

    } else {
      Serial.println(fbdo.errorReason());
    }
  }
}