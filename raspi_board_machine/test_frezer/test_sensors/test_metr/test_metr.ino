#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

float get_mm()
{
  long mm = 0;
  for (int i = 0; i < 10; i++)
  {
    mm += sensor.readRangeContinuousMillimeters();
  }
  //S_mm = S_mm + mm - A_mm;
  //A_mm = S_mm / An;
  return mm / 10.0;
}

void setup()
{
  Serial.begin(9600);

  Wire.begin();
  sensor.setTimeout(500);

  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    delay(1000);
  }
  //sensor.startContinuous();
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 10);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 6);
  sensor.setMeasurementTimingBudget(200000);
  sensor.startContinuous();
}

void loop()
{
  Serial.println(sensor.readRangeContinuousMillimeters());
  delay(500);
}
