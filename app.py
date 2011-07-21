import logging
import os

import tornado.web
import tornado.wsgi
from tornado.web import url

from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import forms
import models

# Constants
IS_DEV = os.environ['SERVER_SOFTWARE'].startswith('Dev')  # Development server

class Application(tornado.wsgi.WSGIApplication):
  def __init__(self):
    handlers = [
      (r'/', IndexHandler),
      # TODO Put your handlers here
    ]
    settings = dict(
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      template_path=os.path.join(os.path.dirname(__file__), 'templates'),
      xsrf_cookies=True,
      # TODO Change this cookie secret
      cookie_secret="asjidoh91239jasdasdasdasdasdkja8izxc21312sjdhsa/Vo=",
    )
    tornado.wsgi.WSGIApplication.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
  pass


class IndexHandler(BaseHandler):
  def get(self):
    self.write('Hello from tornado on app engine')

def main():
  run_wsgi_app(Application())

if __name__ == '__main__':
  main()
