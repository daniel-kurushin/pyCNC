#include <Servo.h>

Servo servo1;

void setup() 
{
  Serial.begin(9600); 
  Serial.setTimeout(10);
  pinMode(13, OUTPUT);
  servo1.attach(8);
}

float data = 0;
int state_begin, state_end;
String input;

void loop() 
{
  String honepa, data;
  int k = 0;
  if(Serial.available() > 0)
  {
    k = Serial.read();
    if(k == 123)
    {
      honepa = Serial.readStringUntil('\n');
      k = 0;
      Serial.println(honepa.indexOf(','));
      Serial.println(honepa.indexOf('"', honepa.indexOf('"') + 1));
    }
  }
  if(honepa.length() > 0)
  {
    for(int i = honepa.indexOf(','); i <= honepa.indexOf(',', honepa.indexOf(',') + 1); i++)
    {
      Serial.print(honepa[i]);
    }
    Serial.println();
    for(int i = honepa.indexOf(',', honepa.indexOf(',') + 1); i <= honepa.indexOf('}'); i++)
    {
      Serial.print(honepa[i]);
    }
    honepa = "";
  }
}
