# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import sys

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from car_serve.handlers import (
    DriverSocketHandler,
    MainHandler
)


class CarState(object):
    """This manages the car state."""

    def print_state(self):
        """Mostly a debug function."""
        print('{} {} {}'.format(self.steering_servo, self.left_motor, self.right_motor))

    def __init__(self):
        self.steering_servo = 0
        self.left_motor = 0
        self.right_motor = 0

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


class CarServer(Application):
    def __init__(self, ioloop=None):
        urls = [
            (r"/", MainHandler),
            (r'/control_socket', DriverSocketHandler),
        ]
        self.car_state = CarState()

        super(CarServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    app = CarServer()

    try:
        http_server = HTTPServer(app)
        http_server.listen(8888, address='127.0.0.1')
        IOLoop.current().start()

    except (SystemExit, KeyboardInterrupt):
        pass

    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
