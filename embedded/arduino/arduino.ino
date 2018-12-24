void setup()
{
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop()
{
  int val = analogRead(A0);
  Serial.println(val);
  delay(1000);
}
