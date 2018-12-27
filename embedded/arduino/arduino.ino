#include <Wire.h>
#include "SparkFunBME280.h"

BME280 sensor;

void setup()
{
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Wire.begin();
  if ( !sensor.beginI2C() )
  {
    Serial.println("The sensor did not respond.");
    while (1);
  }
}

void loop()
{
  int moisture = analogRead(A0);
  Serial.print(moisture);
  Serial.print('\t');

  int light = analogRead(A1);
  Serial.print(light);
  Serial.print('\t');

  float temperature = sensor.readTempC();
  Serial.print(temperature);
  Serial.print('\t');

  float humidity = sensor.readFloatHumidity();
  Serial.print(humidity);
  Serial.print('\n');

  delay(1000);
}
