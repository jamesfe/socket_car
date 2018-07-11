# -*- coding: utf-8 -*-

import json

from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.websocket import websocket_connect

from car_serve.car_serve import CarServer


def get_config(infile):
    with open(infile, 'r') as cfile:
        return json.load(cfile)


def generate_turn_message(val):
    return json.dumps({
        'purpose': 'turn',
        'value': val
    })


def generate_zero_message():
    return json.dumps({
        'purpose': 'zero'
    })


def generate_stop_message():
    return json.dumps({
        'purpose': 'stop'
    })


def generate_speed_inc_message(val, left=False, right=False):
    return json.dumps({
        'purpose': 'speed',
        'value': val,
        'left': left,
        'right': right
    })


class TestDriverSocket(AsyncHTTPTestCase):
    """Tests for badly formed messages."""

    test_url = 'ws://localhost:%d/control_socket'

    def get_app(self):
        config = get_config('./tests/test_config/config.json')
        self.test_app = CarServer(config, ioloop=self.io_loop)
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
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(generate_turn_message(5))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.steering_servo, -5)

    @gen_test
    def test_zero_all_stops_everything(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(generate_zero_message())
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, 0)
        self.assertEqual(car_state.right_motor, 0)

    @gen_test
    def test_inc_speed_increases_speed(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(generate_speed_inc_message(-10, left=True))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, -10)
        self.assertEqual(car_state.right_motor, 0)

    @gen_test
    def test_stop_does_stop_car(self):
        self.test_app.car_state.zero_all()
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)

        ws.write_message(generate_speed_inc_message(-10, left=True))
        response = yield ws.read_message()

        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, -10)
        self.assertEqual(car_state.right_motor, 0)

        ws.write_message(generate_stop_message())
        response = yield ws.read_message()

        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, 0)
        self.assertEqual(car_state.right_motor, 0)
        self.test_app.car_state.zero_all()
