# Servo Control
import time
import wiringpi as wi

print('setup')
# use 'GPIO naming'
wi.wiringPiSetupGpio()
num = 18
# set #18 to be a PWM output
wi.pinMode(num, wi.GPIO.PWM_OUTPUT)
print('pin')
# set the PWM mode to milliseconds stype
wi.pwmSetMode(wi.GPIO.PWM_MODE_MS)

print('clock')
# divide down clock
wi.pwmSetClock(192)
wi.pwmSetRange(2000)


print('pulse')
wi.pwmWrite(num, 500)
time.sleep(1)
print('rotate back')
wi.pwmWrite(num, 1500)

time.sleep(1)
print('done')
# wi.pwmWrite(num, pulse-200)
