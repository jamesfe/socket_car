# -*- coding: utf-8 -*-

import json

from tornado.testing import AsyncHTTPTestCase
from tornado import escape

from car_serve.car_serve import CarServer


def get_config(infile):
    with open(infile, 'r') as cfile:
        return json.load(cfile)


class TestMainServer(AsyncHTTPTestCase):

    def get_app(self):
        config = get_config('./tests/test_config/config.json')
        self.test_app = CarServer(config, ioloop=self.io_loop)
        return self.test_app

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello, world')

    def test_history(self):
        response = self.fetch('/history')
        self.assertEqual(response.code, 200)
        item = escape.json_decode(response.body)
        self.assertIsInstance(item, dict)
