# -*- coding: utf-8 -*-

from tornado.websocket import WebSocketHandler


class DriverSocketHandler(WebSocketHandler):

    def open(self):
        pass

    def on_message(self, message):
        pass
        # self.write_message("message")

    def on_close(self):
        pass
