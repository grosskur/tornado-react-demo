"""
Handlers.
"""
import os

import duktape
import tornado.web


_ROOT = os.path.dirname(__file__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        c = duktape.DukContext()
        c.eval_file(os.path.join(_ROOT, 'static', 'js', 'server.bundle.js'))
        c.eval_string('React.renderToString(React.createElement(Components.Hello));')
        self.write(c.get())
