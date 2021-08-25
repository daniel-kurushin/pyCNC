#include "ramps_run.h"
#include "Arduino.h"

float x_now = 0;
float y_now = 0;
float z_now = 0;

void setup_x()
{
  pm(xEN, 1); dw(xEN, 1);
  pm(xDR, 1); dw(xDR, 0);
  pm(xST, 1); dw(xST, 0);
}

void setup_y()
{
  pm(yEN, 1); dw(yEN, 1);
  pm(yDR, 1); dw(yDR, 0);
  pm(yST, 1); dw(yST, 0);
}

void setup_z()
{
  pm(zEN, 1); dw(zEN, 1);
  pm(zDR, 1); dw(zDR, 0);
  pm(zST, 1); dw(zST, 0);
}

void setup_steppers()
{
  setup_x();
  setup_y();
  setup_z();
}

void setup_endstops()
{
  pm(X_END, 0);
  pm(Y_END, 0);
  pm(Z_END, 0);
}

void x_enable(int a)
{
  dw(xEN, !a);
}

void y_enable(int a)
{
  dw(yEN, !a);
}

void z_enable(int a)
{
  dw(zEN, !a);
}

void x_step(int dir)
{
  bool d = dir == FRW ? 1 : 0;
  dw(xST, 0); dw(xDR, d);
  delayMicroseconds(60);
  dw(xST, 1); dw(xDR, !d);
  delayMicroseconds(60);
  x_now += dir * (1 / X_STEPS_MM);
}

void y_step(int dir)
{
  bool d = dir == FRW ? 1 : 0;
  dw(yST, 0); dw(yDR, d);
  delayMicroseconds(60);
  dw(yST, 1); dw(yDR, !d);
  delayMicroseconds(60);
  y_now += dir * (1 / Y_STEPS_MM);
}

void z_step(int dir)
{
  bool d = dir == FRW ? 1 : 0;
  dw(zST, 0); dw(zDR, d);
  delayMicroseconds(60);
  dw(zST, 1); dw(zDR, !d);
  delayMicroseconds(60);
  y_now += dir * (1 / Z_STEPS_MM);
}

void x_go(float mm)
{
  float steps = mm * X_STEPS_MM;
  x_enable(1);
  int d = steps > 0 ? FRW : BCK;
  for (long i = 0; i < abs(steps); i++)
  {
    x_step(d);
  }
  x_enable(0);
}

void y_go(float mm)
{
  float steps = mm * Y_STEPS_MM;
  y_enable(1);
  int d = steps > 0 ? FRW : BCK;
  for (long i = 0; i < abs(steps); i++)
  {
    y_step(d);
  }
  y_enable(0);
}

void z_go(float mm)
{
  float steps = mm * Z_STEPS_MM;
  z_enable(1);
  int d = steps > 0 ? FRW : BCK;
  for (long i = 0; i < abs(steps); i++)
  {
    z_step(d);
  }
  z_enable(0);
}

void init_ramps()
{
  int count = 0;
  while(dr(X_END) and (count < 270))
  {
    x_go(-1);
    count++;
  }

  count = 0;
  while(dr(Y_END) and (count < 170))
  {
    y_go(-1);
    count++;
  }
  count = 0;
  while(dr(Z_END) and (count < 80))
  {
    z_go(-1);
    count++;
  }
  x_now = 0;
  y_now = 0;
  z_now = 0;
}
