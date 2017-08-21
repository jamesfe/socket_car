# -*- coding: utf-8 -*-

import unittest

from car_serve import car_state


class TestCarState(unittest.TestCase):

    def test_max_intervals(self):
        a = car_state.CarState()
        a.max_prev_states = 5
        self.assertEqual(len(a.previous_states), 0)
        for i in range(10):
            a.update_physical_state()
        self.assertEqual(len(a.previous_states), 5)

    def test_health_check_returns_dict(self):
        a = car_state.CarState()
        self.assertIsInstance(a.health_check(), dict)
