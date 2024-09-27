# Milling Machine
*John Edmer Ortiz*, 
*Thomas Mehes*, 
*Quentin Bouet*

## Overview
A control system for a computer numerical controlled (CNC) mill was designed and constructed.
Specifically, a printed circuit board was created to enable computer control of the mill’s motors. The
hardware design was in the form of a printed circuit board that fits under a Pico development board.
Basic control of the machine was programmed in C language whereas the GUI and the
drawing feature was done in a higher-level language, Python.

## Software
The software consists of a Python GUI
which allows manual and automated control of the
milling machine. All signals (both manual and
automated) are sent over the serial port from the Python
script directly to the Pico. Each signal is a character,
which is processed by the Pico with the
getchar_timeout_us() function along with a switch
statement. These signals (mostly matching the buttons)
are processed as commands for the Pico to use on the
mill. The main commands include rotating (by sending
pulses through STEP) in any direction (setting DIR to
either high or low) any stepper motor. Other commands
include triggering and adjusting the spindle speed
through PWM. It should also be noted that the step mode
of the Z axis is ½ step instead of a full step, to allow more
precision when adjusting the spindle height.

### Q Code
Moreover, the drawing feature (triggered by the DRAW button) consists of an algorithm (**Q code**) in
Python that reads a matrix of strictly “1”s and “0”s from a text file (where “1” represents a point on
a drawing and “0” represents empty space). It then returns efficient commands to the Pico by
calculating the difference between its old and new position in the matrix. Q code works by first
scanning the entire matrix for a “1”, before scanning surrounding bits from either the left or right
side of the bit it is currently at. Once there are no more surrounding “1”s, the program loops back
until there are no more remaining “1”s in the entire matrix or an x or y limit is reached.

### Calibration
Furthermore, the CNC App includes a few calibration factors: SCALE and MOTOR DELAY. SCALE
allows the user to scale the already prepared image to a desired size for drawing. MTR_DELAY
delays the signals sent to the Pico. It should also be noted that reducing MTR_DELAY to a small value
such as 1ms, helps reduce vibrations and improve responsiveness of the stepper motors.
