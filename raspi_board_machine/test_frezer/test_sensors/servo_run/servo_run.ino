#include <Servo.h>

Servo lazer_servo;

void setup()
{
  lazer_servo.attach(6);
}

void loop()
{
  lazer_servo.write(0);
  delay(2000);
  lazer_servo.write(180);
  delay(2000);
}
