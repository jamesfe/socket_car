# Servo Control
import time
import wiringpi

num = 18
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #num to be a PWM output
wiringpi.pinMode(num, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

while True:
        for pulse in range(50, 250, 1):
                wiringpi.pwmWrite(num, pulse)
                time.sleep(delay_period)
        for pulse in range(250, 50, -1):
                wiringpi.pwmWrite(num, pulse)
                time.sleep(delay_period)
