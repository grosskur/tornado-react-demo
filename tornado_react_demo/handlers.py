"""
Handlers.
"""
import os

import duktape
import tornado.web


_ROOT = os.path.dirname(__file__)


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, ctx):
        self.ctx = ctx

    def get(self):
        self.ctx.eval_string('React.renderToString(React.createElement(Components.Hello));')
        self.write(self.ctx.get())
        self.ctx.pop()
