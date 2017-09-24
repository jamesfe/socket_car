# -*- coding: utf-8 -*-

import json

from tornado.websocket import WebSocketHandler


class DriverSocketHandler(WebSocketHandler):

    def lazy_write_message(self, msg):
        self.write_message(json.dumps(msg))

    def check_required_fields(self, fields, message):
        missing_fields = []
        for field in fields:
            if field not in message:
                missing_fields.append(field)
        if len(missing_fields) != 0:
            self.write_error_message('Missing fields: {}'.format(missing_fields))
            return False
        return True

    def open(self):
        self.application.log.info('New websocket!')
        pass

    def write_error_message(self, msg):
        message = {
            'type': 'error',
            'message': msg
        }
        self.application.log.error(msg)
        self.lazy_write_message(message)

    def get_car_state(self):
        return self.application.car_state.health_check()

    def handle_turns(self, message):
        if not self.check_required_fields(['value', 'direction'], message):
            # If we return false, junk it.
            return

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

    def handle_speed(self, message):
        if not self.check_required_fields(['value', 'left', 'right'], message):
            return
        try:
            value = int(message.get('value', 0))
        except ValueError:
            self.write_error_message('speed value must be an int')

        if value != 0:
            if message.get('left'):
                self.application.car_state.inc_motor('left', value)
            if message.get('right'):
                self.application.car_state.inc_motor('right', value)
        self.write_message(self.get_car_state())

    def handle_zero(self, message):
        """Zero everything out on the car.  Full stop."""
        self.application.car_state.zero_all()
        self.write_message(self.get_car_state())

    def handle_stop(self, message):
        """Stop the car but leave the servo in place."""
        self.application.car_state.zero_both_motors()
        self.write_message(self.get_car_state())

    def on_message(self, message):
        self.application.internal_log(message)
        self.application.log.info('Received message')
        json_msg = {}
        try:
            json_msg = json.loads(message)
        except ValueError:
            self.write_error_message('not json')
        if 'purpose' not in json_msg:
            self.write_error_message('no purpose')
            return None
        purpose = json_msg['purpose']

        if purpose == 'turn':
            self.handle_turns(json_msg)
        elif purpose == 'speed':
            self.handle_speed(json_msg)
        elif purpose == 'zero':
            self.handle_zero(json_msg)
        elif purpose == 'stop':
            self.handle_stop(json_msg)

    def on_close(self):
        pass
