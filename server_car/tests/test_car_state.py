# -*- coding: utf-8 -*-

import json
import unittest

from car_serve import car_state


def get_config(infile):
    with open(infile, 'r') as cfile:
        return json.load(cfile)


def get_a_state():
    config = get_config('./tests/test_config/config.json').get('car_state', {})
    return car_state.CarState(config)


class TestCarState(unittest.TestCase):

    def test_max_intervals(self):
        config = get_config('./tests/test_config/config.json').get('car_state', {})
        a = car_state.CarState(config)
        a.max_prev_states = 5
        self.assertEqual(len(a.previous_states), 0)
        for i in range(10):
            a.update_physical_state()
        self.assertEqual(len(a.previous_states), 5)

    def test_health_check_returns_dict(self):
        config = get_config('./tests/test_config/config.json').get('car_state', {})
        a = car_state.CarState(config)
        self.assertIsInstance(a.health_check(), dict)

    def test_car_print_state_does_not_throw_an_exception(self):
        ts = get_a_state()
        ts.print_state()

    def test_get_valid_speed(self):
        ts = get_a_state()
        self.assertEqual(ts.get_valid_speed(-10000), ts._MIN_SPEED)
        self.assertEqual(ts.get_valid_speed(10000), ts._MAX_SPEED)
        self.assertEqual(ts.get_valid_speed(ts._MAX_SPEED - 10), ts._MAX_SPEED - 10)

    def test_states_are_capped(self):
        ts = get_a_state()
        for i in range(0, ts.max_prev_states + 10):
            ts.update_state_histories()
        self.assertEqual(len(ts.previous_states), ts.max_prev_states)
