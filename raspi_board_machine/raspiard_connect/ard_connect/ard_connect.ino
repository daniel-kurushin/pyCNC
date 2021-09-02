#include "ramps_run.h"
#include <Wire.h>
#include <VL53L0X.h>

#define INIT     0
#define CONNECT  1
#define WORK     2

#define W_COMMAND     0
#define W_INIT        1
#define W_GET_DATA    2
#define W_RUN         3
#define W_OUTPUT_DATA 4

#define STEPPER_CH   0
#define STEPPER_X    1
#define STEPPER_Y    2
#define STEPPER_Z    3
#define INIT_XYZ     4
#define RETURN_MM    5
#define RETURN_XYZ   6
#define STEPPER_EXIT 7

int state_connect = 0;
int state_work = 0;
int state_stepper = 0;
float data = 0.0;

VL53L0X sensor;

float get_mm()
{
  long mm = 0;
  for (int i = 0; i < 100; i++)
  {
    mm += sensor.readRangeContinuousMillimeters();
  }
  return mm / 100.0;
}

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10);
  setup_steppers();
  setup_endstops();

  Wire.begin();
  sensor.setTimeout(500);

  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    delay(1000);
  }
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 10);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 6);
  sensor.setMeasurementTimingBudget(200000);
  //sensor.startContinuous();
}

void loop()
{
  switch(state_connect)
  {
    case INIT:
    {
      //init_ramps();
      state_connect = CONNECT;
      break;
    }
    case CONNECT:
    {
      if(Serial.available() > 0)
      {
        data = Serial.parseInt();
        if(data == 5)
        {
          Serial.println(666);
          state_connect = WORK;
        }
      }
      else
      {
        Serial.println(1);
      }
      break;
    }
    case WORK:
    {
      if(Serial.available())
      {
        switch(state_work)
        {
          case W_COMMAND:
          {
            data = Serial.parseInt();
            if(data == 10)
            {
              state_work = W_INIT;
              Serial.print(555);
            }
            else if (data == 20)
            {
              Serial.println(777);
              state_work = W_RUN;
            }
            else if (data == 30)
            {
              Serial.println(888);
              state_work = W_OUTPUT_DATA;
            }
            else if(data == 40)
            {
              Serial.print(999);
              state_work = W_COMMAND;
              state_connect = CONNECT;
            }
            else
            {
              Serial.println(666);
            }
            break;
          }
          case W_INIT:
          {
            Serial.println(555);
            init_ramps();
            state_work = W_COMMAND;
            Serial.println(666);
            break;
          }
          case W_RUN:
          {
            switch(state_stepper)
            {
              case STEPPER_CH:
              {
                data = Serial.parseInt();
                if(data == 11)
                {
                  Serial.println(7777);
                  state_stepper = STEPPER_X;
                }
                else if (data == 12)
                {
                  Serial.println(7777);
                  state_stepper = STEPPER_Y;
                }
                else if (data == 13)
                {
                  Serial.println(7777);
                  state_stepper = STEPPER_Z;
                }
                else if (data == 14)
                {
                  Serial.println(7777);
                  state_stepper = INIT_XYZ;
                }
                else if (data == 15)
                {
                  Serial.println(7777);
                  state_stepper = RETURN_MM;
                }
                else if (data == 16)
                {
                  Serial.println(7777);
                  state_stepper = RETURN_XYZ;
                }
                else
                {
                  Serial.println(777);
                }
                break;
              }
              case STEPPER_X:
              {
                data = Serial.parseFloat();
                if(data != 0)
                {
                  x_go(data);
                  //init_ramps();
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                Serial.println(7777);
                break;
              }
              case STEPPER_Y:
              {
                data = Serial.parseFloat();
                if(data != 0)
                {
                  y_go(data);
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                Serial.println(7777);
                break;
              }
              case STEPPER_Z:
              {
                data = Serial.parseFloat();
                if(data != 0)
                {
                  z_go(data);
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                Serial.println(7777);
                break;
              }
              case INIT_XYZ:
              {
                data = Serial.parseInt();
                if(data != 0)
                {
                  init_ramps();
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                Serial.println(7777);
                break;
              }
              case RETURN_MM:
              {
                data = Serial.parseInt();
                if(data == 42)
                {
                  Serial.println(get_mm());
                  //Serial.println(42.42);
                  data = 0;
                }
                else if (data == 73)
                {
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                Serial.println(7777);
                break;
              }
              case RETURN_XYZ:
              {
                data = Serial.parseInt();
                if(data == 42)
                {
                  Serial.println(get_x_now());
                  data = 0;
                }
                else if (data == 43)
                {
                  Serial.println(get_y_now());
                  data = 0;
                }
                else if (data == 44)
                {
                  Serial.println(get_z_now());
                  data = 0;
                }
                else if (data == 73)
                {
                  data = 0;
                  state_stepper = STEPPER_EXIT;
                  Serial.println(666);
                }
                //Serial.println(7777);
                break;
              }
              case STEPPER_EXIT:
              {
                data = 0;
                state_work = W_COMMAND;
                state_stepper = STEPPER_CH;
                Serial.println(666);
                break;
              }
            }
            /*
            data = Serial.parseInt();
            if(data != 0)
            {
              x_go(data);
              data = 0;
              state_work = W_COMMAND;
            }
            Serial.println(777);
            state_work = W_RUN;
            */
            break;
          }
          case W_OUTPUT_DATA:
          {
            Serial.println(888);
            Serial.println(2021);
            data = Serial.parseInt();
            if(data == 666)
            {
              state_work = W_COMMAND;
            }
            Serial.println(666);
            break;
          }
        }
      }
      break;
    }
  }
  //while(1);
}
