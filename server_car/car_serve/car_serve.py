# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import logging
import sys

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application

from car_serve.car_state import CarState
from car_serve.handlers import (
    DriverSocketHandler,
    MainHandler
)

logger = logging.getLogger('car_server')
coloredlogs.install(format='%(asctime)s - %(levelname)s: %(message)s', level='DEBUG', logger=logger)


class CarServer(Application):
    def __init__(self, ioloop=None):
        urls = [
            (r"/", MainHandler),
            (r'/control_socket', DriverSocketHandler),
        ]
        self.car_state = CarState()
        self.log = logger

        super(CarServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    app = CarServer()

    try:
        http_server = HTTPServer(app)
        http_server.listen(8888, address='127.0.0.1')
        i = PeriodicCallback(app.car_state.update_physical_state, app.car_state.update_ms)
        i.start()
        IOLoop.current().start()
    except (SystemExit, KeyboardInterrupt):
        pass

    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
