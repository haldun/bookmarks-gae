import datetime
import logging
import os
import html5lib

import tornado.web
import tornado.wsgi
from tornado.web import url

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import forms
import models
import uimodules

# Constants
IS_DEV = os.environ['SERVER_SOFTWARE'].startswith('Dev')  # Development server

class Application(tornado.wsgi.WSGIApplication):
  def __init__(self):
    handlers = [
      url(r'/', IndexHandler, name='index'),
      url(r'/new', NewBookmarkHandler, name='new_bookmark'),
      url(r'/bookmarks/([^/]+)', ListBookmarksHandler, name='list'),
      url(r'/import', ImportBookmarksHandler, name='import'),
      url(r'/edit', EditBookmarkHandler, name='edit'),
      url(r'/update', UpdateBookmarkHandler, name='update'),
    ]
    settings = dict(
      debug=IS_DEV,
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      template_path=os.path.join(os.path.dirname(__file__), 'templates'),
      xsrf_cookies=True,
      cookie_secret="zmxc12msadkzx209923/asd98123.=-sadnu129uaks/Vo=",
      ui_modules=uimodules,
    )
    tornado.wsgi.WSGIApplication.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
  def get_current_user(self):
    user = users.get_current_user()
    if user:
      user.admin = users.is_current_user_admin()
      account = models.Account.get_account_for_user(user)
      self.current_account = account
    return user

  def get_login_url(self):
    return users.create_login_url(self.request.uri)

  def get_integer(self, name, default, min_value=None, max_value=None):
    value = self.get_argument(name, '')
    if not isinstance(value, (int, long)):
      try:
        value = int(value)
      except (TypeError, ValueError), err:
        value = default
    if min_value is not None:
      value = max(min_value, value)
    if max_value is not None:
      value = min(value, max_value)
    return value


class IndexHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.redirect(self.reverse_url('list', self.current_account.nickname))


class ListBookmarksHandler(BaseHandler):
  def get(self, nickname):
    account = models.Account.get_account_for_nickname(nickname)
    if account is None:
      raise tornado.web.HTTPError(404)
    if self.current_user and account.key() == self.current_account.key():
      query = models.Bookmark.all().filter('account =', self.current_account)
    else:
      query = models.Bookmark.all() \
                    .filter('account =', self.current_account) \
                    .filter('is_private =', False)
    query = query.order('-created')
    # Pagination
    offset = self.get_integer('offset', 0, 0)
    limit = self.get_integer('limit', 25, 1, 100)
    params = {
      'limit': limit,
      'first': offset + 1,
    }
    bookmarks = query.fetch(limit + 1, offset)
    self.render('list.html', bookmarks=bookmarks)


class NewBookmarkHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render('new.html', form=forms.BookmarkForm())

  @tornado.web.authenticated
  def post(self):
    form = forms.BookmarkForm(self)
    if form.validate():
      uri_digest = models.Bookmark.get_digest_for_uri(form.uri.data)
      key = '%s:%s' % (self.current_account.key().name(), uri_digest)
      bookmark = models.Bookmark(
          key_name=key,
          account=self.current_account,
          uri_digest=uri_digest,
          **form.data)
      bookmark.put()
      self.redirect(self.reverse_url('index'))
    else:
      self.render('new.html', form=form)


class EditBookmarkHandler(BaseHandler):
  def get(self):
    form = forms.BookmarkForm(obj=self.bookmark)
    self.render('new.html', form=form)

  def post(self):
    form = forms.BookmarkForm(self, obj=self.bookmark)
    if form.validate():
      self.write('%s' % self.bookmark.title)
      form.populate_obj(self.bookmark)
      self.bookmark.put()
      self.redirect(self.reverse_url('index'))
    else:
      self.render('new.html', form=form)

  @tornado.web.authenticated
  def prepare(self):
    id = self.get_argument('id')
    bookmark = models.Bookmark.get_bookmark_for_digest(id)
    if bookmark is None:
      raise tornado.web.HTTPError(404)
    if bookmark.account.key() != self.current_account.key():
      raise tornado.web.HTTPError(403)
    self.bookmark = bookmark


class ImportBookmarksHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render('import.html')

  @tornado.web.authenticated
  def post(self):
    body = self.request.files['file'][0]['body']
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder('dom'))
    dom_tree = parser.parse(body)
    bookmarks = []
    for link in dom_tree.getElementsByTagName('a'):
      uri = link.getAttribute('href')
      if not uri.startswith('http://'):
        continue
      title = ''.join(node.data
                      for node in link.childNodes
                      if node.nodeType == node.TEXT_NODE)
      uri_digest = models.Bookmark.get_digest_for_uri(uri)
      key = '%s:%s' % (self.current_account.key().name(), uri_digest)
      is_private = link.getAttribute('private') == '1'
      created = link.getAttribute('add_date')
      try:
        created = datetime.datetime.utcfromtimestamp(float(created))
      except:
        pass
      tags = [tag.strip()
              for tag in link.getAttribute('tags').strip().split(',')
              if link.getAttribute('tags')]
      bookmark = models.Bookmark(
          key_name=key, account=self.current_account, uri_digest=uri_digest,
          title=title, uri=uri, private=is_private, created=created,
          tags=tags)
      bookmarks.append(bookmark)
    db.put(bookmarks)
    self.redirect(self.reverse_url('index'))


class UpdateBookmarkHandler(BaseHandler):
  @tornado.web.authenticated
  def post(self):
    id = self.get_argument('id')
    action = self.get_argument('action')
    bookmark = models.Bookmark.get_bookmark_for_digest(id)
    if bookmark is None:
      raise tornado.web.HTTPError(404)
    if bookmark.account.key() != self.current_account.key():
      raise tornado.web.HTTPError(403)
    if action == 'star':
      bookmark.is_starred = True
    elif action == 'unstar':
      bookmark.is_starred = False
    elif action == 'read':
      bookmark.is_unread = False
    elif action == 'unread':
      bookmark.is_unread = True
    bookmark.put()
    self.render('module-bookmark.html', bookmark=bookmark)

def main():
  run_wsgi_app(Application())

if __name__ == '__main__':
  main()
