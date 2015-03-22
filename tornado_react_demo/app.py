"""
Demo app.
"""
import argparse
import logging
import os
import time

import duktape
import simplejson
import tornado.ioloop
import tornado.log
import tornado.web

from .handlers import MainHandler


_PROG = 'python-react-demo'

_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
_STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


class EnvConfig(object):
    def __init__(self):
        self.env = {}

    def add(self, var, default_value=None):
        self.env[var] = os.getenv(var, default_value)

    def get(self, var):
        return self.env[var.upper()]

    def require(self, parser, var):
        if self.env.get(var.upper()) is None:
            parser.error('{} is required'.format(var.upper()))


def main(args):
    _setup_logging()
    parser = ArgumentParser(
        prog=_PROG,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    opts = parser.parse_args(args)
    env = EnvConfig()
    env.add('ADDRESS', '')
    env.add('COOKIE_SECRET')
    env.add('DEBUG', False)
    env.add('PORT', 8000)
    env.require(parser, 'cookie_secret')
    with open(os.path.join(_DATA_PATH, 'manifest.json')) as f:
        manifest = simplejson.load(f)
    fname = os.path.join(_STATIC_PATH, 'js',
                         manifest['assetsByChunkName']['server'])
    ctx = duktape.DukContext()
    ctx.eval_file(fname)
    params = {
        'ctx': ctx,
    }
    handlers = [
        tornado.web.URLSpec(
            r'/',
            MainHandler, params, 'home',
        ),
    ]
    settings = dict(
        asset_env=manifest['assetsByChunkName'],
        autoescape='xhtml_escape',
        cookie_secret=env.get('cookie_secret'),
        debug=env.get('debug'),
        log_function=_log_request,
        static_path=_STATIC_PATH,
        template_path=_TEMPLATE_PATH,
        xsrf_cookies=True,
    )
    _start_tornado_app(int(env.get('port')), env.get('address'), handlers,
                       settings)


def _setup_logging():
    fmt = 'level=%(levelname)s %(message)s'
    logging.basicConfig(format=fmt)
    logging.getLogger('').setLevel(logging.DEBUG)

    logging.addLevelName(logging.DEBUG, 'debug')
    logging.addLevelName(logging.INFO, 'info')
    logging.addLevelName(logging.WARNING, 'warning')
    logging.addLevelName(logging.ERROR, 'error')
    logging.addLevelName(logging.CRITICAL, 'critical')


def _log_request(handler):
    """
    Writes a completed HTTP request to the logs.
    """
    if handler.get_status() < 400:
        log_method = tornado.log.access_log.info
    elif handler.get_status() < 500:
        log_method = tornado.log.access_log.warning
    else:
        log_method = tornado.log.access_log.error

    log_method('status=%d method=%s path=%s host=%s remote_ip=%s '
               'duration=%.5f',
               handler.get_status(), handler.request.method,
               handler.request.uri, handler.request.host,
               handler.request.remote_ip,
               handler.request.request_time())


def _start_tornado_app(port, address, handlers, settings):
    app = tornado.web.Application(handlers, **settings)
    logging.info('status=listening port=%d', port)
    app.listen(port, address)
    tornado.ioloop.IOLoop.instance().start()
