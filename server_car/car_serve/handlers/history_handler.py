# -*- codin: utf-8 -*-

import json
import time

from tornado.web import RequestHandler


class HistoryHandler(RequestHandler):

    def get(self):
        history = self.application.car_state.previous_states
        message = {
            'time_sent': time.time(),
            'states': history
        }
        self.write(json.dumps(message))
        self.finish()
