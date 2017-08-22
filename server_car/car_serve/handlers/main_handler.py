from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    """I'll just leave this here for posterity."""

    def get(self):
        self.write('Hello, world')
