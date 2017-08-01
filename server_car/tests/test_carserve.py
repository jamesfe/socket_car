# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from car_serve import car_serve


class TestMainServer(AsyncHTTPTestCase):

    def get_app(self):
        return car_serve.make_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello, world')
