# -*- coding: utf-8 -*-

import json

from tornado.websocket import WebSocketHandler


class DriverSocketHandler(WebSocketHandler):

    def open(self):
        pass

    def write_error_message(self, msg):
        message = {
            'type': 'error',
            'message': msg
        }
        json_message = json.dumps(message)
        self.write_message(json_message)

    def get_car_state(self):
        return {'alive': True}

    def handle_turns(self, message):
        required_fields = ['value', 'direction']
        missing_fields = []
        for field in required_fields:
            if field not in message:
                missing_fields.append(field)
        if len(missing_fields) != 0:
            # TODO: LOG ERROR
            self.write_error_message('missing fields: {}'.format(missing_fields))
            return False

        # Check direction
        if message['direction'] not in ['left', 'right']:
            self.write_error_message('turn direction must be left or right')

        # Check turn value.
        try:
            val = int(message['value'])
        except ValueError:
            self.write_error_message('turn value must be an int')
        if message['direction'] == 'left':
            self.application.car_state.turn(-1 * val)
        elif message['direction'] == 'right':
            self.application.car_state.turn(val)
        self.write_message(self.get_car_state())

    def handle_speed(message):
        pass

    def on_message(self, message):
        json_msg = {}
        try:
            json_msg = json.loads(message)
        except ValueError:
            # TODO: LOG ERROR
            self.write_error_message('not json')
        if 'purpose' not in json_msg:
            # TODO: LOG ERROR
            self.write_error_message('no purpose')
            return None
        purpose = json_msg['purpose']

        if purpose == 'turn':
            self.handle_turns(json_msg)
        elif purpose == 'speed':
            self.handle_speed(message)

    def on_close(self):
        pass
