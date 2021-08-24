
void setup()
{
  pinMode(19, INPUT);
  pinMode(15, INPUT);
  pinMode(2,  INPUT);
  Serial.begin(9600);
}

void loop()
{
  /*
  Serial.print(digitalRead(19)); //y
  Serial.print("  ");
  Serial.print(digitalRead(15)); //x
  Serial.print("  ");
  Serial.print(digitalRead(2)); //z
  Serial.println("");
  //delay(1500);
  */
  int y, x, z = 0;
  y = digitalRead(19);
  x = digitalRead(15);
  z = digitalRead(2);
  if(!y)
  {
    Serial.println("Y");
  }
  else if(!x)
  {
    Serial.println("X");
  }
  else if(!z)
  {
    Serial.println("Z");
  }

}
