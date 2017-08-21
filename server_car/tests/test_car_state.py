# -*- coding: utf-8 -*-

import unittest

from socket_car import car_state


class TestCarState(unittest.TestCase):

    def test_max_intervals(self):
        a = car_state.CarState()
        # Set max items
        # Run a few updates
        # Check length of telemetry
