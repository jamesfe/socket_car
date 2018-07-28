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


def generate_shift_message(val):
    return json.dumps({
        'value': val,
        'purpose': 'shift'
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
    def check_malformed_message(self, message, err_msg):
        car_state = self.test_app.car_state
        prev_state = car_state.health_check()
        del prev_state['time']
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(message)
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        curr_state = car_state.health_check()
        del curr_state['time']
        self.assertDictEqual(curr_state, prev_state)
        self.assertEqual(res['message'], err_msg)

    @gen_test
    def test_missing_fields_append(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        msg = {'purpose': 'speed'}
        ws.write_message(json.dumps(msg))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        self.assertEqual(res['message'], "Missing fields: ['value', 'left', 'right']")

    def test_malformed_messages(self):
        self.check_malformed_message('blaggle', 'not json')
        self.check_malformed_message(json.dumps({'no': 'purpose'}), 'no purpose')
        self.check_malformed_message(generate_turn_message(0.5), 'turn value must be an int')
        self.check_malformed_message(generate_turn_message('hello'), 'turn value must be an int')

    @gen_test
    def test_messages_are_received_and_replied_to(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(json.dumps({'blaggle': True}))
        response = yield ws.read_message()
        self.assertIsNotNone(response)

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
        self.assertEqual(car_state.steering_servo, 5)

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
    def test_shifting_increases_speed(self):
        ws = yield websocket_connect(
            self.test_url % self.get_http_port(),
            io_loop=self.io_loop)
        ws.write_message(generate_shift_message(3))
        response = yield ws.read_message()
        self.assertIsNotNone(response)
        res = json.loads(response)
        self.assertIsInstance(res, dict)
        car_state = self.test_app.car_state
        self.assertEqual(car_state.left_motor, 288)
        self.assertEqual(car_state.right_motor, 288)

    def test_failing_shift_messages(self):
        self.check_malformed_message(generate_shift_message('hello'), 'must contain a value from 1-6')
        self.check_malformed_message(generate_shift_message(7), 'must contain a value from 1-6')

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
