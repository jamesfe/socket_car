# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import sys

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from car_serve.handlers import (
    DriverSocketHandler,
    MainHandler
)


class CarServer(Application):
    def __init__(self, ioloop=None):
        urls = [
            (r"/", MainHandler),
            (r'/control_socket', DriverSocketHandler),
        ]

        super(CarServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    app = CarServer()

    try:
        http_server = HTTPServer(app)
        http_server.listen(8888, address='127.0.0.1')
        IOLoop.current().start()

    except (SystemExit, KeyboardInterrupt):
        pass

    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
