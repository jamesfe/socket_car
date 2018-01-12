import wiringpi
import time

servo_gpio_pin = 23 
_max = 200
first = 50


print('setup results: {}'.format(wiringpi.wiringPiSetupGpio()))

def setup_and_test(pin, small, large, first):
    print('{} {} {}'.format(small, large, first))

    print('creating pin')
    cr = wiringpi.softPwmCreate(pin, small, large)
    print('Create results: {}'.format(cr))

    print('first write')
    wres = wiringpi.softPwmWrite(servo_gpio_pin, first)
    print('Write res {}'.format(wres))

    time.sleep(1)
    print('done sleeping')
    wiringpi.softPwmWrite(servo_gpio_pin, small)

# for l in range(0, 1000, 50):
#     setup_and_test(servo_gpio_pin, 0, l, int(l/2))
setup_and_test(servo_gpio_pin, 0, 200, 50)


def big_test_a_bunch_of_ranges():
    def testrange(top):
        for i in range(0, top, int(top/10)):
            print('sending {}'.format(i))
            wiringpi.softPwmWrite(servo_gpio_pin, i)
            time.sleep(1)


    for k in range(10, 1000, 50):
        time.sleep(2)
        print('creating pin', k)
        wiringpi.softPwmCreate(17, 0, k)
        testrange(k)
