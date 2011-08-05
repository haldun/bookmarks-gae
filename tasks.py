import collections
import datetime
import logging

import html5lib

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import deferred

import models

def ComputeTagCounts(account_key):
  account = models.Account.get(account_key)
  tags = collections.defaultdict(int)
  account_key_name = account.key().name()
  logging.info("Started processing tags of %s" % account.nickname)
  # TODO Process all bookmarks at once!?
  for bookmark in account.bookmarks:
    for tag_name in bookmark.tags:
      tag_key_name = '%s:%s' % (account_key_name, tag_name)
      tags[(tag_name, tag_key_name)] += 1
  db.put([models.Tag(key_name=key_name,
                    name=name,
                    count=count,
                    account=account)
                    for (name, key_name), count in tags.items()
                    if name])
  logging.info("Processed tags")

def CheckBookmarks(account_key):
  account = models.Account.get(account_key)
  if account is None:
    logging.info("Account not found %s" % account_key)
    return
  last_checked_date = datetime.datetime.utcnow() - datetime.timedelta(days=2)
  query = models.Bookmark.all().filter('account =', account) \
                               .filter('last_checked <', last_checked_date) \
                               .order('last_checked')
  cursor_key = 'check_bookmarks_cursor:%s' % account_key
  cursor = memcache.get(cursor_key)
  if cursor:
    query.with_cursor(cursor)
    memcache.delete(cursor_key)
  bookmarks = query.fetch(50)
  if not bookmarks:
    return
  processed = []
  for bookmark in bookmarks:
    logging.info("Checking: %s" % bookmark.uri)
    try:
      result = urlfetch.fetch(bookmark.uri, follow_redirects=False, method='HEAD')
      bookmark.last_status_code = result.status_code

      logging.info("Got %s from %s" % (result.status_code, bookmark.uri))
      if result.status_code == 200:
        # TODO Get the contents and put it to the blobstore
        pass
      if result.status_code in (301, 302):
        bookmark.redirected = result.headers.get('location', bookmark.uri)
    except urlfetch.DownloadError:
      bookmark.last_status_code = 500
    except Exception, e:
      logging.error("Exception: %s" % e)
    bookmark.last_checked = datetime.datetime.utcnow()
    processed.append(bookmark)
  db.put(processed)
  memcache.set(cursor_key, query.cursor())
  deferred.defer(CheckBookmarks, account_key, _countdown=120)

def ImportBookmarks(import_key):
  bookmark_import = models.Import.get(import_key)
  parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder('dom'))
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
  deferred.defer(ComputeTagCounts, account.key())
