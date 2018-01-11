import wiringpi
import time

servo_gpio_pin = 17
_max = 200
first = 50



def setup_and_test(pin, small, large, first):
    print('{} {} {}'.format(small, large, first))
    print('setup: {}'.format(wiringpi.wiringPiSetupGpio()))

    print('creating pin')
    wiringpi.softPwmCreate(pin, small, large)

    print('first write')
    wiringpi.softPwmWrite(servo_gpio_pin, first)

    time.sleep(1)
    print('done sleeping')
    wiringpi.softPwmWrite(servo_gpio_pin, small)

for l in range(0, 1000, 50):
    setup_and_test(servo_gpio_pin, 0, l, int(l/2))

