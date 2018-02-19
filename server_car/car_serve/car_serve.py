# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import datetime as dt
import logging
import os
import json
import sys
import time

import argparse

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application

from car_serve.car_state import CarState
from car_serve.handlers import (
    DriverSocketHandler,
    MainHandler,
    HistoryHandler
)

logger = logging.getLogger('car_server')
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger)
# TODO: Maybe add log_function here?


class CarServer(Application):

    def internal_log(self, msg):
        self.command_log.write(msg)

    def __init__(self, config, ioloop=None):
        self.server_config = config.get('car_serve', {})
        urls = [
            (r'/', MainHandler),
            (r'/control_socket', DriverSocketHandler),
            (r'/history', HistoryHandler)
        ]
        self.car_state = CarState(config.get('car_state', {}))

        self.log_dir = self.server_config.get('log_dir', './logs/')

        # Previous commands are going to be dumped to a file
        now = dt.datetime.fromtimestamp(time.time())
        command_log_name = 'command_log_{}.log'.format(now.strftime('%Y_%m_%d_%H%M%S'))
        self.command_log = open(os.path.join(self.log_dir, command_log_name), 'w')
        self.internal_log('Command received')

        self.log = logger

        super(CarServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='config file')
    args = parser.parse_args()
    logger.warn('Reading config from {}'.format(args.config))

    config = {}
    with open(args.config, 'r') as infile:
        config = json.load(infile)

    if config == {}:
        sys.exit()

    serve_config = config.get('car_serve', {})
    logger.warn(serve_config)

    app = CarServer(config)

    try:
        logger.info('Opening HTTP server.')
        http_server = HTTPServer(app)
        http_server.listen(serve_config.get('port', 9001), address=serve_config.get('ip_address', '127.0.0.1'))
        update_ms = serve_config.get('update_ms', 1000)
        logger.debug('Registering periodic callback. Every {} ms'.format(update_ms))
        i = PeriodicCallback(app.car_state.update_physical_state, update_ms)
        i.start()
        IOLoop.current().start()
    except (SystemExit, KeyboardInterrupt):
        pass

    logger.info('Stopping server.')
    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
