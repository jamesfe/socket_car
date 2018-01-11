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

# for l in range(0, 1000, 50):
#     setup_and_test(servo_gpio_pin, 0, l, int(l/2))


print('setup results: {}'.format(wiringpi.wiringPiSetupGpio()))


def testrange(top):
    for i in range(0, top, int(top/10)):
        print('sending {}'.format(i))
        wiringpi.softPwmWrite(17, i)
        time.sleep(.3)


for k in range(10, 1000, 50):
    print('creating pin', k)
    wiringpi.softPwmCreate(17, 0, k)
    testrange(k)
