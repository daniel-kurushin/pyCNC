#ifndef ramps_run_H
#define ramps_run_H

#define X_END 15
#define Y_END 19
#define Z_END 2

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

#define X_STEPS_MM 796.0
#define Y_STEPS_MM 796.0
#define Z_STEPS_MM 796.0

void setup_x();
void setup_y();
void setup_z();

void setup_steppers();
void setup_endstops();

void x_enable(int a);
void y_enable(int a);
void z_enable(int a);

void x_step(int dir);
void y_step(int dir);
void z_step(int dir);

void x_go(float mm);
void y_go(float mm);
void z_go(float mm);

void init_ramps();

float get_x_now();
float get_y_now();
float get_z_now();

#endif
