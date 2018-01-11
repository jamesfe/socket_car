# -*- coding: utf-8 -*-
"""A class that controls the physical state of the car.  The car's physical state is updated by the
    `update_physical_state` function: this is called by the parent server every `update_ms` milliseconds."""


import logging
import time

import coloredlogs

logger = logging.getLogger('car_state')
logger.propagate = False
coloredlogs.install(format='%(asctime)s - %(levelname)s: %(message)s', level='DEBUG', logger=logger)

try:
    from dual_mc33926_rpi import motors
    import wiringpi
except ImportError:
    logger.error('Could not import PWM library')


class CarState(object):
    """This manages the car state."""

    def print_state(self):
        """Mostly a debug function."""
        out_string = '{} {} {}'.format(self.steering_servo, self.left_motor, self.right_motor)
        logger.info(out_string)

    def get_valid_speed(self, value):
        value = int(value)
        if value > self._MAX_SPEED:
            value = self._MAX_SPEED
        elif value < self._MIN_SPEED:
            value = self._MIN_SPEED
        return value

    def __init__(self, config):
        self.config = config
        self.gear_lookup = {}
        self._not_initialized = True
        self.steering_servo = config.get('zero_servo', 100)
        self.left_motor = 0
        self.right_motor = 0

        self.use_motors = config.get('use_motors', False)
        self.use_servo = config.get('use_servo', False)

        # Some config items
        self.update_ms = config.get('update_ms', 1000)
        self.servo_gpio_pin = config.get('servo_gpio_pin', 17)
        # Previous states are a rotating number of states
        self.max_prev_states = config.get('max_prev_states', 2000)
        self.previous_states = []

    def _inc_motor(self, begin, val):
        """A helper function we can change later to modify how values are calculated."""
        return self.get_valid_speed(begin + val)

    def _set_absolute_left(self, value):
        """Set the value for the left motor absolutely."""
        self.left_motor = self.get_valid_speed(value)

    def _set_absolute_right(self, value):
        """Set the value for the right motor absolutely."""
        self.right_motor = self.get_valid_speed(value)

    def _zero_left(self):
        """Zero out the left motor."""
        self.left_motor = 0

    def _zero_right(self):
        """Zero out the right motor."""
        self.right_motor = 0

    def _zero_steering(self):
        self.steering_servo = 0

    def zero_steering(self):
        self._zero_steering()

    def shift_gear(self, value):
        """A shortcut to a given speed so we don't have to accelerate all the time."""
        speed = self.gear_lookup[value]
        self._set_absolute_right(speed)
        self._set_absolute_left(speed)

    def inc_motor(self, choice, val):
        """Increment the motor; but I think we can send a negative val and slow down. I hope."""
        if choice == 'left':
            self.left_motor = self._inc_motor(self.left_motor, val)
        elif choice == 'right':
            self.right_motor = self._inc_motor(self.right_motor, val)
        elif choice == 'both':
            self.left_motor = self._inc_motor(self.left_motor, val)
            self.right_motor = self._inc_motor(self.right_motor, val)

    def _turn(self, value):
        """Check max and min, then set value."""
        new_steering = self.steering_servo + value
        if new_steering > self._MAX_SERVO:
            self.steering_servo = self._MAX_SERVO
        elif new_steering < self._MIN_SERVO:
            self.steering_servo = self._MIN_SERVO
        else:
            self.steering_servo = new_steering

    def turn(self, value):
        """Turn by value: negative is left, positive is right."""
        self._turn(value)

    def zero_both_motors(self):
        self._zero_left()
        self._zero_right()

    def zero_all(self):
        self.zero_both_motors()
        self.zero_steering()

    def initialize_state(self):
        self._not_initialized = False
        self._MAX_SPEED = self.config.get('max_motor_speed', 480)
        self._MIN_SPEED = self._MAX_SPEED * -1
        self._MIN_SERVO = 0
        self._MAX_SERVO = self.config.get('min_servo', 0)
        self._INITIAL_SERVO = 100
        gears = 5
        for index in range(1, gears + 1):
            self.gear_lookup[index] = int((self._MAX_SPEED / gears) * index)
        logger.info('Setting gears: ' + str(self.gear_lookup))

        if self.use_motors:
            logger.info('Setting motor speeds to zero.')
            motors.enable()
            motors.setSpeeds(0, 0)
        if self.use_servo:
            logger.info('Setting up Servo Software-Based PWM')
            wiringpi.wiringPiSetupGpio()
            wiringpi.softPwmCreate(self.servo_gpio_pin, 0, self._MAX_SERVO)
            wiringpi.softPwmWrite(self.servo_gpio_pin, self._INITIAL_SERVO)

    def update_physical_state(self):
        """Send the right values to the GPIO pins."""
        # Do some note taking
        history_unit = {
            'time': time.time(),
            'health_check': self.health_check()
        }
        self.previous_states.append(history_unit)
        if len(self.previous_states) > self.max_prev_states:
            delta = len(self.previous_states) - self.max_prev_states
            self.previous_states = self.previous_states[delta:]

        if self._not_initialized:
            logger.info('initializing state, should only happen once or so')
            self.initialize_state()

        # If we are on the rPi, make the physical state changes
        if self.use_motors:
            logger.info('State: L {} R {} DIR {}'.format(self.left_motor, self.right_motor, self.steering_servo))
            motors.motor1.setSpeed(self.left_motor)
            motors.motor2.setSpeed(self.right_motor)
        if self.use_servo:
            wiringpi.softPwmWrite(self.servo_gpio_pin, self.steering_servo)

    def health_check(self):
        return {
            'time': time.time(),
            'health_check': {
                'steering': self.steering_servo,
                'left_motor': self.left_motor,
                'right_motor': self.right_motor
            }
        }
