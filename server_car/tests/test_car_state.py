# -*- coding: utf-8 -*-

import json
import unittest

from car_serve import car_state


def get_config(infile):
    with open(infile, 'r') as cfile:
        return json.load(cfile)


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
