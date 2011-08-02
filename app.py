import collections
import datetime
import itertools
import logging
import os
import re
import html5lib

import tornado.web
import tornado.wsgi
from tornado.web import url

from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext import blobstore
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
      url(r'/edit', EditBookmarkHandler, name='edit'),
      url(r'/update', UpdateBookmarkHandler, name='update'),
      (r'/upload', UploadHandler),

      # Task handlers
      (r'/tasks/import', ImportBookmarksHandler),
      (r'/tasks/process_tags', ProcessTagsHandler),
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

  def render_string(self, template, **kwds):
    return tornado.web.RequestHandler.render_string(
        self, template, users=users, **kwds)

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
                    .filter('account =', account) \
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
    tags = models.Tag.all().filter('account =', self.current_account) \
                           .order('-count') \
                           .fetch(20)
    self.render('list.html', bookmarks=bookmarks, tags=tags)


class NewBookmarkHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    # Check if popup
    is_popup = self.get_argument('p', None) == '1'
    if is_popup:
      bookmark = models.Bookmark.get_bookmark_for_uri(self.get_argument('uri'))
      if bookmark is None:
        form = forms.BookmarkForm(self)
      else:
        self.redirect(self.reverse_url('edit') + '?&p=1&id=' + bookmark.uri_digest)
        return
    else:
      form = forms.BookmarkForm()
    self.render('bookmark-form.html', form=form, is_popup=is_popup)

  @tornado.web.authenticated
  def post(self):
    is_popup = self.get_argument('p', None) == '1'
    form = forms.BookmarkForm(self)
    if form.validate():
      account_key_name = self.current_account.key().name()
      uri_digest = models.Bookmark.get_digest_for_uri(form.uri.data)
      key = '%s:%s' % (account_key_name, uri_digest)
      bookmark = models.Bookmark(
          key_name=key,
          account=self.current_account,
          uri_digest=uri_digest,
          **form.data)
      bookmark.put()
      if is_popup:
        self.write('<script>window.close()</script>')
      else:
        self.redirect(self.reverse_url('index'))
    else:
      self.render('bookmark-form.html', form=form)


class EditBookmarkHandler(BaseHandler):
  def get(self):
    form = forms.BookmarkForm(obj=self.bookmark)
    self.render('bookmark-form.html', form=form)

  def post(self):
    form = forms.BookmarkForm(self, obj=self.bookmark)
    if form.validate():
      form.populate_obj(self.bookmark)
      self.bookmark.put()
      if self.get_argument('p', None):
        self.write('<script>window.close()</script>')
      else:
        self.redirect(self.reverse_url('index'))
    else:
      self.render('bookmark-form.html', form=form)

  @tornado.web.authenticated
  def prepare(self):
    id = self.get_argument('id')
    bookmark = models.Bookmark.get_bookmark_for_digest(id)
    if bookmark is None:
      raise tornado.web.HTTPError(404)
    if bookmark.account.key() != self.current_account.key():
      raise tornado.web.HTTPError(403)
    self.bookmark = bookmark


class UploadHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render('upload.html', upload_url=blobstore.create_upload_url('/upload'))

  @tornado.web.authenticated
  def post(self):
    if IS_DEV:
      blob_key = re.findall(r'blob-key="*(\S+)"', self.request.body)[0]
    else:
      blob_key = re.findall(r'blob-key=(.+)', self.request.body)[0]
    new_import = models.Import(account=self.current_account,
                               blob=blob_key)
    new_import.put()
    taskqueue.add(url='/tasks/import', params={'key': new_import.key()})
    self.redirect('/')


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


# Task handlers

class BaseTaskHandler(BaseHandler):
  def initialize(self):
    self.application.settings['xsrf_cookies'] = False


class ImportBookmarksHandler(BaseTaskHandler):
  # TODO Catch exceptions
  def post(self):
    bookmark_import = models.Import.get(self.get_argument('key'))
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder('dom'))
    dom_tree = parser.parse(bookmark_import.blob.open())
    bookmarks = []
    account = bookmark_import.account
    for link in dom_tree.getElementsByTagName('a'):
      uri = link.getAttribute('href')
      if not uri.startswith('http://'):
        continue
      title = ''.join(node.data
                      for node in link.childNodes
                      if node.nodeType == node.TEXT_NODE)
      uri_digest = models.Bookmark.get_digest_for_uri(uri)
      key = '%s:%s' % (account.key().name(), uri_digest)
      is_private = link.getAttribute('private') == '1'
      created = link.getAttribute('add_date')
      try:
        created = datetime.datetime.utcfromtimestamp(float(created))
      except:
        pass
      tags = [tag.strip().lower()
              for tag in link.getAttribute('tags').strip().split(',')
              if link.getAttribute('tags')]
      bookmark = models.Bookmark(
          key_name=key, account=account, uri_digest=uri_digest,
          title=title, uri=uri, private=is_private, created=created,
          tags=tags)
      bookmarks.append(bookmark)
    db.put(bookmarks)
    # Mark this task as completed
    bookmark_import.status = bookmark_import.DONE
    bookmark_import.processed = datetime.datetime.utcnow()
    bookmark_import.put()
    # Remove blob
    # TODO The following line does not seem to be working!?
    # blobstore.delete(bookmark_import.blob)


class ProcessTagsHandler(BaseTaskHandler):
  def get(self):
    # TODO What about deleted bookmarks' tags?
    # TODO Process all accounts at once!?
    for account in models.Account.all():
      tags = collections.defaultdict(int)
      account_key_name = account.key().name()
      # TODO Process all bookmarks at once!?
      for bookmark in account.bookmarks:
        for tag_name in bookmark.tags:
          tag_key_name = '%s:%s' % (account_key_name, tag_name)
          tags[(tag_name, tag_key_name)] += 1
      db.put(models.Tag(key_name=key_name,
                        name=name,
                        count=count,
                        account=account)
                        for (name, key_name), count in tags.items())


def main():
  run_wsgi_app(Application())

if __name__ == '__main__':
  main()
