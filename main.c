/*
CC2511 - Assignment 2
CNC Controller Software
John Edmer Ortiz, Thomas Mehes, Quentin Bouet
*/

/* Library dependencies */
#include "pico/stdlib.h"
#include <stdbool.h>
#include <stdio.h>
#include "hardware/pwm.h"

/* Pico GPIO pins */
#define STEP_X 5
#define STEP_Y 17
#define STEP_Z 21
#define DIR_X 4
#define DIR_Y 16
#define DIR_Z 22
#define Z_MODE0 20
#define Z_MODE1 19
#define XY_RST_AND_SLP 14
#define SPINDLE 15
#define Z_RESET 2

/* Python script signal encoding for function calls */
#define Y_UP '1'
#define X_LEFT '2'
#define Y_DOWN '3'
#define X_RIGHT '4'
#define Z_RAISE '5'
#define Z_LOWER '6'
#define TOGGLE_SPINDLE '7'
#define INC_PWM '8'
#define DEC_PWM '9'
#define DRAW '0'
#define STOP_SPINDLE 'Q'

/* PWM constants */
#define PWM_MIN 0
#define PWM_MAX 100
#define PWM_STEP 10

/* Step delay */
#define DELAY 1

/* Function prototypes */
void move_left();
void move_right();
void move_up();
void move_down();
void move_raise();
void move_lower();
void start_drawing(uint slice_spindle, int pwm_level);
void toggle_spindle(uint slice_spindle, int pwm_level, bool *spindle_status);
void inc_pwm(uint slice_spindle, int *pwm_level);
void dec_pwm(uint slice_spindle, int *pwm_level);
void stop_spindle(uint slice_spindle);
void gpio_setup();

int main(void)
{
  /* Initialises pico IO interfaces and GPIO pins */
  stdio_init_all();
  gpio_setup();

  /* Sets up spindle function, slice and initial values */
  gpio_set_function(SPINDLE, GPIO_FUNC_PWM);
  uint slice_spindle = pwm_gpio_to_slice_num(SPINDLE);
  pwm_set_wrap(slice_spindle, PWM_MAX);
  int pwm_level = PWM_MIN;
  pwm_set_chan_level(slice_spindle, PWM_CHAN_B, pwm_level);
  bool spindle_status = true;

  char ch;

  /* Translates python script signals to corresponding function calls */
  while (true)
  {
    ch = getchar_timeout_us(0);
    switch (ch)
    {
    case X_LEFT:
      move_left();
      break;
    case X_RIGHT:
      move_right();
      break;
    case Y_UP:
      move_up();
      break;
    case Y_DOWN:
      move_down();
      break;
    case Z_RAISE:
      move_raise();
      break;
    case Z_LOWER:
      move_lower();
      break;
    case DRAW:
      start_drawing(slice_spindle, pwm_level);
      break;
    case TOGGLE_SPINDLE:
      toggle_spindle(slice_spindle, pwm_level, &spindle_status);
      break;
    case INC_PWM:
      inc_pwm(slice_spindle, &pwm_level);
      break;
    case DEC_PWM:
      dec_pwm(slice_spindle, &pwm_level);
      break;
    case STOP_SPINDLE:
      stop_spindle(slice_spindle);
      break;
    default:
    }
  }
}

/* Move X motor one full step to the left */
void move_left()
{
  gpio_put(DIR_X, true);
  gpio_put(STEP_X, true);
  sleep_ms(DELAY);
  gpio_put(STEP_X, false);
  sleep_ms(DELAY);
}

/* Move X motor one full step to the right */
void move_right()
{
  gpio_put(DIR_X, false);
  gpio_put(STEP_X, true);
  sleep_ms(DELAY);
  gpio_put(STEP_X, false);
  sleep_ms(DELAY);
}

/* Move Y motor one full step upward */
void move_up()
{
  gpio_put(DIR_Y, true);
  gpio_put(STEP_Y, true);
  sleep_ms(DELAY);
  gpio_put(STEP_Y, false);
  sleep_ms(DELAY);
}

/* Move Y motor one full step downward */
void move_down()
{
  gpio_put(DIR_Y, false);
  gpio_put(STEP_Y, true);
  sleep_ms(DELAY);
  gpio_put(STEP_Y, false);
  sleep_ms(DELAY);
}

/* Raise Z motor half a step */
void move_raise()
{
  gpio_put(DIR_Z, false);
  gpio_put(STEP_Z, true);
  sleep_ms(DELAY);
  gpio_put(STEP_Z, false);
  sleep_ms(DELAY);
}

/* Lower Z motor half a step */
void move_lower()
{
  gpio_put(DIR_Z, true);
  gpio_put(STEP_Z, true);
  sleep_ms(DELAY);
  gpio_put(STEP_Z, false);
  sleep_ms(DELAY);
}

/* Starts spindle at selected PWM level */
void start_drawing(uint slice_spindle, int pwm_level)
{
  pwm_set_enabled(slice_spindle, true);
  pwm_set_chan_level(slice_spindle, PWM_CHAN_B, pwm_level);
}

/* Toggles spindle ON/OFF */
void toggle_spindle(uint slice_spindle, int pwm_level, bool *spindle_status)
{
  pwm_set_enabled(slice_spindle, true);
  *spindle_status = !*spindle_status;
  if (!*spindle_status)
  {
    pwm_set_chan_level(slice_spindle, PWM_CHAN_B, PWM_MIN);
  }
  else
  {
    pwm_set_chan_level(slice_spindle, PWM_CHAN_B, pwm_level);
  }
}

/* Increase PWM level by PWM_STEP */
void inc_pwm(uint slice_spindle, int *pwm_level)
{
  if (*pwm_level < PWM_MAX)
  {
    *pwm_level = *pwm_level + PWM_STEP;
  }
  pwm_set_chan_level(slice_spindle, PWM_CHAN_B, *pwm_level);
}

/* Decrease PWM level by PWM_STEP */
void dec_pwm(uint slice_spindle, int *pwm_level)
{
  if (*pwm_level > PWM_MIN)
  {
    *pwm_level = *pwm_level - PWM_STEP;
  }
  pwm_set_chan_level(slice_spindle, PWM_CHAN_B, *pwm_level);
}

/* Turns off spindle */
void stop_spindle(uint slice_spindle)
{
  pwm_set_chan_level(slice_spindle, PWM_CHAN_B, PWM_MIN);
  pwm_set_enabled(slice_spindle, false);
}

/* Sets up GPIO pins */
void gpio_setup()
{
  gpio_init(Z_RESET);
  gpio_init(STEP_X);
  gpio_init(STEP_Y);
  gpio_init(STEP_Z);
  gpio_init(SPINDLE);
  gpio_init(DIR_X);
  gpio_init(DIR_Y);
  gpio_init(DIR_Z);
  gpio_init(Z_MODE0);
  gpio_init(Z_MODE1);
  gpio_init(XY_RST_AND_SLP);

  gpio_set_dir(Z_RESET, GPIO_OUT);
  gpio_set_dir(STEP_X, GPIO_OUT);
  gpio_set_dir(STEP_Y, GPIO_OUT);
  gpio_set_dir(STEP_Z, GPIO_OUT);
  gpio_set_dir(DIR_X, GPIO_OUT);
  gpio_set_dir(DIR_Y, GPIO_OUT);
  gpio_set_dir(DIR_Z, GPIO_OUT);
  gpio_set_dir(Z_MODE0, GPIO_OUT);
  gpio_set_dir(Z_MODE1, GPIO_OUT);
  gpio_set_dir(XY_RST_AND_SLP, GPIO_OUT);
  gpio_set_dir(SPINDLE, GPIO_OUT);

  gpio_put(Z_MODE0, true);
  gpio_put(Z_MODE1, false);
  gpio_put(XY_RST_AND_SLP, true);
  gpio_put(Z_RESET, true);  
}