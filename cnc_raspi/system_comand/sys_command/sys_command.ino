#define X_END 15
#define Y_END 19
#define Z_END 2
#define F_END 3

#define FREZA 8

#define xEN 38
#define xDR A1
#define xST A0

#define yEN A2
#define yDR A7
#define yST A6

#define zEN A8
#define zDR 48
#define zST 46

#define FRW  1
#define BCK -1

#define pm pinMode
#define dr digitalRead
#define dw digitalWrite
#define ar analogRead
#define aw analogWrite

#define X_STEPS_MM 8
#define Y_STEPS_MM 8
#define Z_STEPS_MM 8

#define INIT 0
#define FSB  1
#define SSB  2
#define ANG  4
#define END  5

int x;
int data;
int state = INIT;
int n, end_x, end_y, end_z;
int L;
float y_now, z_now;
float zero_freza = 10.56;

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

long x_step(int dir, float speed_x)
{
  bool d = dir == FRW ? 1 : 0;
  dw(xST, 0); dw(xDR, d);
  delayMicroseconds(round(round((pow(speed_x * 800, -1) * pow(10, 5))) / 2));
  dw(xST, 1); dw(xDR, !d);
  delayMicroseconds(round(round((pow(speed_x * 800, -1) * pow(10, 5))) / 2));
  return dir * 125; // round((1 / X_STEPS_MM) * 100000)
}

void y_step(int dir, float speed_y)
{
  bool d = dir == FRW ? 1 : 0;
  dw(yST, 0); dw(yDR, d);
  delayMicroseconds(round(round((pow(speed_y * 800, -1) * pow(10, 5))) / 2));
  dw(yST, 1); dw(yDR, !d);
  delayMicroseconds(round(round((pow(speed_y * 800, -1) * pow(10, 5))) / 2));
  y_now += dir * 125;
}

void z_step(int dir, float speed_z)
{
  bool d = dir == FRW ? 1 : 0;
  dw(zST, 0); dw(zDR, d);
  delayMicroseconds(round(round((pow(speed_z * 800, -1) * pow(10, 5))) / 2));
  dw(zST, 1); dw(zDR, !d);
  delayMicroseconds(round(round((pow(speed_z * 800, -1) * pow(10, 5))) / 2));
  z_now += dir * 125;
}

long x_go(long x,  long mm, float speed_x)
{
  long x1 = x;
  long steps = mm * X_STEPS_MM;
  x_enable(1);
  int d = steps > 0 ? FRW : BCK;
  //Serial.println(steps);
  for (long i = 0; i < abs(steps); i++)
  {
    x1 += x_step(d, speed_x);
  }
  x_enable(0);
  return x1;
}

void y_go(long mm, float speed_y)
{
  long steps = mm * Y_STEPS_MM;
  y_enable(1);
  int d = steps > 0 ? FRW : BCK;
  for (long i = 0; i < abs(steps); i++)
  {
    y_step(d, speed_y);
  }
  y_enable(0);
}

void z_go(long mm, float speed_z)
{
  long steps = mm * Z_STEPS_MM;
  z_enable(1);
  int d = steps > 0 ? FRW : BCK;
  for (long i = 0; i < abs(steps); i++)
  {
    z_step(d, speed_z);
  }
  z_enable(0);
}

float get_zero_freza()
{
  float freza_mm;
  while (dr(F_END) and (z_now < 80))
  {
    z_go(0.01, 0.25);
  }
  freza_mm = z_now;
  int count = 0;
  while (dr(Z_END) and (count < 80))
  {
    z_go(-1, 1);
    count++;
  }
  count = 0;
  z_go(5, 1);
  while (dr(Z_END) and (count < 80))
  {
    z_go(-0.25, 0.05);
    count++;
  }
  while (!dr(Z_END))
  {
    z_go(0.01, 0.05);
  }
  z_now = 0.00;
  return freza_mm;
}

void init_ramps()
{
  int count = 0;
  long x;
  while (dr(X_END) and (count < 270))
  {
    x_go(x, -100, 1);
    count++;
  }
  count = 0;
  x_go(x, 3, 1);
  while (dr(X_END) and (count < 270))
  {
    x_go(x, -1, 0.05);
    count++;
  }
  while (!dr(X_END))
  {
    x_go(x, 1, 0.05);
  }

  count = 0;
  while (dr(Y_END) and (count < 270))
  {
    y_go(-100, 1);
    count++;
  }
  count = 0;
  y_go(3, 1);
  while (dr(Y_END) and (count < 900))
  {
    y_go(-1, 0.05);
    count++;
  }
  while (!dr(Y_END))
  {
    y_go(1, 0.05);
  }


  count = 0;
  while (dr(Z_END) and (count < 80))
  {
    z_go(-100, 1);
    count++;
  }
  count = 0;
  z_go(500, 1);
  while (dr(Z_END) and (count < 80))
  {
    z_go(-25, 0.05);
    count++;
  }
  while (!dr(Z_END))
  {
    z_go(1, 0.05);
  }
  y_now = 0;
  z_now = 0;
}

void setup()
{
  Serial.begin(9600);
  setup_steppers();
  pinMode(X_END, INPUT);
  pinMode(Y_END, INPUT);
  pinMode(Z_END, INPUT);
  pinMode(F_END, INPUT_PULLUP);
  pinMode(FREZA, OUTPUT);
  init_ramps();
}

void loop()
{
  long x_now = 0;
  float d = 0.00;
  while (1)
  {
    if (Serial.available()) {
      data = Serial.read() << 8 | Serial.read();
      switch (state) {
        case INIT:
          L = 0;
          n = 0;
          if (data = 255) {
            state = FSB;
          }
          break;
        case FSB:
          if (data = 255) {
            state = SSB;
          }
          else {
            state = INIT;
          }
          break;
        case SSB:
          if (data < 20) {
            L = data;
            state = ANG;
            n = 0;
          }
          else {
            state = INIT;
          }
          break;
        case ANG:
          if (data != 253)
          {
            switch (n++) {
              case 0:
                x_now = x_go(x_now, data, 1);
                break;
              case 1:
                y_go(data, 1);
                break;
              case 2:
                z_go(data, 1);
                break;
              case 3:
                analogWrite(FREZA, data);
                break;
            }
          }
          else
          {
            state = INIT;
            n = 0;
            L = 0;
          }
          break;
      }

    }
    Serial.println(state);
    Serial.println(data);
    Serial.println(666);
    Serial.println(x_now);
    Serial.println(y_now);
    Serial.println(z_now);
    Serial.println(zero_freza);
    Serial.println("<");
  }
 }
