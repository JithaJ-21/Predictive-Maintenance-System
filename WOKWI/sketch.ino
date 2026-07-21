#include <WiFi.h>
#include <HTTPClient.h>

#include <DHT.h>
#include <Adafruit_Sensor.h>

// -------------------------
// WiFi Credentials
// -------------------------

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* server = "http://192.168.56.1:5000/update";

// -------------------------
// ThingSpeak
// -------------------------

String apiKey = "CG12P2D7N6PES2DA";

// -------------------------
// DHT22
// -------------------------

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

// -------------------------
// Variables
// -------------------------

int vibration = 0;

float temperature = 0;

int statusCode = 0;

int faultCount = 0;

void setup() {

  Serial.begin(115200);

  dht.begin();

  WiFi.begin(ssid, password);

  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.println();
  Serial.println("WiFi Connected");
}

void loop() {

  // -------------------------
  // Read Sensors
  // -------------------------

  vibration = analogRead(34);

  temperature = dht.readTemperature();

  if (isnan(temperature)) {

    Serial.println("DHT Read Failed");

    delay(2000);

    return;

  }

  // -------------------------
  // Machine Status
  // -------------------------

  if (temperature > 45 || vibration > 3000) {

    statusCode = 2;

  }

  else if (temperature > 40 || vibration > 1800) {

    statusCode = 1;

  }

  else {

    statusCode = 0;

  }

  // -------------------------
  // Fault Counter
  // -------------------------

  if (statusCode != 0) {

    faultCount++;

  }

  // -------------------------
  // Serial Monitor
  // -------------------------

  Serial.println();
  Serial.println("========================================");
  Serial.println("      INDUSTRIAL SENSOR NODE");
  Serial.println("========================================");

  Serial.print("Temperature : ");
  Serial.print(temperature, 1);
  Serial.println(" °C");

  Serial.print("Vibration   : ");
  Serial.println(vibration);

  Serial.print("Machine Status : ");

  if (statusCode == 0)
      Serial.println("HEALTHY");

  else if (statusCode == 1)
      Serial.println("WARNING");

  else
      Serial.println("CRITICAL");

  Serial.println();

  Serial.print("Uploading to ThingSpeak");

  if (WiFi.status() == WL_CONNECTED) {

      HTTPClient http;

      String url = "https://api.thingspeak.com/update?api_key=" + apiKey +
      "&field1=" + String(vibration) +
      "&field2=" + String(temperature,1) +
      "&field3=" + String(statusCode) +
      "&field4=" + String(faultCount);

      http.begin(url);

      int code = http.GET();

      Serial.println("...");

      Serial.print("HTTP Response : ");
      Serial.println(code);

      if(code == 200){
          Serial.println("Cloud Upload Successful");
      }
      else{
          Serial.println("Cloud Upload Failed");
      }

      http.end();
  }

  Serial.println("========================================");
  delay(3000);
}
