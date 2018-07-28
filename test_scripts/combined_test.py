# Servo Control
import time
import argparse

import wiringpi as wi


def scale_to_motor(servo_min, servo_max, motor_min, motor_max):
    def rval(val):
        val = val - servo_min
        norm_max = servo_max - servo_min
        numerator = val * (motor_max - motor_min)
        return (numerator / norm_max) + motor_min
    return rval


parser = argparse.ArgumentParser()
parser.set_defaults(cycles=5, delay=0.01, servo_min=70, servo_max=220, servo_step=10)
parser.add_argument("cycles", help="number of cycles you want to run for", type=int)
parser.add_argument("servo_pin", help="servo pin number", type=int)
parser.add_argument("servo_min", help="minimum servo", type=int)
parser.add_argument("servo_max", help="maximum servo", type=int)
parser.add_argument("servo_step", help="servo step size", type=int)
parser.add_argument("motor_pin", help="motor pin number", type=int)
parser.add_argument("motor_min", help="minimum motor", type=int)
parser.add_argument("motor_max", help="maximum motor", type=int)

parser.parse_args()

servo_min = parser.servo_min
servo_max = parser.servo_max
servo_step = parser.servo_step

print('setup')
# use 'GPIO naming'
wi.wiringPiSetupGpio()
print('Setting up servo pin')
wi.pinMode(parser.servo_pin, wi.GPIO.PWM_OUTPUT)

print('Setting up motor pin')
wi.pinMode(parser.motor_pin, wi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wi.pwmSetMode(wi.GPIO.PWM_MODE_MS)

print('setting clock, range to 192, 2000')
wi.pwmSetClock(192)
wi.pwmSetRange(2000)

scale = scale_to_motor(servo_min, servo_max, parser.motor_min, parser.motor_max)

for i in range(0, parser.cycles):
    for x in range(servo_min, servo_max, servo_step):
        print("To X: ", x)
        wi.pwmWrite(parser.servo_pin, x)
        wi.pwmWrite(parser.motor_pin, scale(x))
        time.sleep(.1)

    for x in range(servo_max, servo_min, servo_step):
        print("To X: ", x)
        wi.pwmWrite(parser.servo_pin, x)
        wi.pwmWrite(parser.motor_pin, scale(x))
        time.sleep(.1)
