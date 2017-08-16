# -*- coding: utf-8 -*-

import json

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
    def test_non_json_messages_return_error(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message('blaggle')
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        msg = {'type': 'error', 'message': 'not json'}
        self.assertDictEqual(res, msg)

    @gen_test
    def test_messages_are_received_and_replied_to(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps({'blaggle': True}))
        response = yield ws.read_message()
        self.assertIsNotNone(response)

    @gen_test
    def test_messages_with_no_purpose_receive_error(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps({'blaggle': 'blah'}))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        msg = {'type': 'error', 'message': 'no purpose'}
        self.assertDictEqual(res, msg)

    @gen_test
    def test_turning_turns_the_vehicle(self):
        turn_message = {
            'purpose': 'turn',
            'value': 5,
            'direction': 'left'
        }
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps(turn_message))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.steering_servo, -5)

    @gen_test
    def test_zero_all_stops_everything(self):
        zero_message = {
            'purpose': 'zero'
        }
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps(zero_message))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, 0)
        self.assertEqual(car_state.right_motor, 0)

    @gen_test
    def test_inc_speed_increases_speed(self):
        speed_inc_message = {
            'purpose': 'speed',
            'value': -10,
            'left': True,
            'right': False
        }
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps(speed_inc_message))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, -10)
        self.assertEqual(car_state.right_motor, 0)

    @gen_test
    def test_stop_does_stop_car(self):
        pass
