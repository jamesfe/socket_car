# -*- coding: utf-8 -*-
"""A class that controls the physical state of the car.  The car's physical state is updated by the
    `update_physical_state` function: this is called by the parent server every `update_ms` milliseconds."""


import logging

import coloredlogs


logger = logging.getLogger('car_state')
coloredlogs.install(format='%(asctime)s - %(levelname)s: %(message)s', level='DEBUG', logger=logger)


class CarState(object):
    """This manages the car state."""

    def print_state(self):
        """Mostly a debug function."""
        out_string = '{} {} {}'.format(self.steering_servo, self.left_motor, self.right_motor)
        logger.info(out_string)

    def __init__(self):
        self.steering_servo = 0
        self.left_motor = 0
        self.right_motor = 0
        self.update_ms = 1000

    def _inc_motor(self, begin, val):
        """A helper function we can change later to modify how values are calculated."""
        return begin + val

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

    def inc_motor(self, choice, val):
        if choice == 'left':
            self.left_motor = self._inc_motor(self.left_motor, val)
        elif choice == 'right':
            self.right_motor = self._inc_motor(self.right_motor, val)
        elif choice == 'both':
            self.left_motor = self._inc_motor(self.left_motor, val)
            self.right_motor = self._inc_motor(self.right_motor, val)

    def _turn(self, value):
        """Seemingly stupid, maybe we will have to do something more complex here later."""
        self.steering_servo += value

    def turn(self, value):
        """Turn by value: negative is left, positive is right."""
        self._turn(value)

    def zero_both_motors(self):
        self._zero_left()
        self._zero_right()

    def zero_all(self):
        self.zero_both_motors()
        self.zero_steering()

    def update_physical_state(self):
        """Send the right values to the GPIO pins."""
        pass

    def health_check(self):
        return {
            'steering': self.steering_servo,
            'left_motor': self.left_motor,
            'right_motor': self.right_motor
        }
