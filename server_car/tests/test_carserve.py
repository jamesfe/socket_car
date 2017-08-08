# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from car_serve.car_serve import CarServer


class TestMainServer(AsyncHTTPTestCase):

    def get_app(self):
        self.test_app = CarServer(ioloop=self.io_loop)
        return self.test_app

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello, world')
