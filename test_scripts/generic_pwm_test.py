# Servo Control
"""
We use this test script for the servo but also for the motors.
"""
import time
import argparse

import wiringpi

parser = argparse.ArgumentParser()
parser.add_argument("pin", help="PIN number you are testing for PWM", type=int)
parser.set_defaults(cycles=5, delay=0.01)
parser.add_argument("cycles", help="number of cycles you want to run for", type=int)
parser.parse_args()

num = parser.pin
cycles = parser.cycles

# use 'GPIO naming'
res = wiringpi.wiringPiSetupGpio()
print('Setup returns: ', res)

# set #num to be a PWM output
wiringpi.pinMode(num, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay = parser.delay
for i in range(0, cycles):
    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(num, pulse)
        time.sleep(delay)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(num, pulse)
        time.sleep(delay)
