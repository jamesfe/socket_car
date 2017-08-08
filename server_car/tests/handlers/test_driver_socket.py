# -*- coding: utf-8 -*-

from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.websocket import websocket_connect
from car_serve.car_serve import CarServer


class TestDriverSocket(AsyncHTTPTestCase):
    """Tests for badly formed messages."""

    test_url = 'ws://localhost:%d/control_socket'

    def get_app(self):
        self.test_app = CarServer(ioloop=self.io_loop)
        return self.test_app

    @gen_test
    def test_messages_are_received_and_replied_to(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message('blaggle')
        response = yield ws.read_message()
        self.assertIsNotNone(response)
