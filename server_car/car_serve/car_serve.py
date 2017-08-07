# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import tornado.ioloop
import tornado.web

from socket_car import DriverSocketHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/control_socket', DriverSocketHandler),

    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
