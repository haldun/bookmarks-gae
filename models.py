import hashlib
import itertools
import logging

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import blobstore

class Account(db.Model):
  user = db.UserProperty(auto_current_user_add=True, required=True)
  email = db.EmailProperty(required=True) # key == <email>
  nickname = db.StringProperty(required=True)
  unreads = db.ListProperty(int)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)

  lower_email = db.StringProperty()
  lower_nickname = db.StringProperty()

  # Note that this doesn't get called when doing multi-entity puts.
  def put(self):
    self.lower_email = str(self.email).lower()
    self.lower_nickname = self.nickname.lower()
    super(Account, self).put()

  @classmethod
  def get_account_for_user(cls, user):
    """Get the Account for a user, creating a default one if needed."""
    email = user.email()
    assert email
    key = '<%s>' % email
    account = cls.get_by_key_name(key)
    if account is not None:
      return account
    nickname = cls.create_nickname_for_user(user)
    return cls.get_or_insert(key, user=user, email=email, nickname=nickname)

  @classmethod
  def create_nickname_for_user(cls, user):
    """Returns a unique nickname for a user."""
    name = nickname = user.email().split('@', 1)[0]
    next_char = chr(ord(nickname[0].lower()) + 1)
    existing_nicks = [account.nickname
                      for account in cls.gql(('WHERE lower_nickname >= :1 AND '
                                              'lower_nickname < :2'),
                                              nickname.lower(), next_char)]
    suffix = 0
    while nickname.lower() in existing_nicks:
      suffix += 1
      nickname = '%s%d' % (name, suffix)
    return nickname

  @classmethod
  def get_account_for_nickname(cls, nickname):
    """Get the list of Accounts that have this nickname."""
    assert nickname
    assert '@' not in nickname
    return cls.all().filter('lower_nickname =', nickname.lower()).get()

  def get_tags(self):
    tags = memcache.get('%s:tags' % self.key())
    if tags is not None:
      return tags
    tags = list(Tag.all().filter('account =', self))
    if not memcache.add('%s:tags' % self.key(), tags, 3600):
      logging.error('Memcache set failed')
    return tags

  def get_popular_tags(self, limit=20):
    tags = memcache.get('%s:popular_tags' % self.nickname)
    if tags is not None:
      return tags
    tags = Tag.all().filter('account =', self).order('-count').fetch(limit)
    if not memcache.add('%s:popular_tags' % self.nickname, tags, 3600):
      logging.error('Memcache set failed')
    return tags


class Bookmark(db.Model):
  account = db.ReferenceProperty(Account, collection_name='bookmarks')
  uri = db.LinkProperty(required=True)
  uri_digest = db.StringProperty()
  title = db.StringProperty()
  description = db.TextProperty()
  tags = db.ListProperty(unicode)
  is_private = db.BooleanProperty(default=False)
  is_unread = db.BooleanProperty(default=False)
  is_starred = db.BooleanProperty(default=False)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)

  @classmethod
  def get_digest_for_uri(cls, uri):
    m = hashlib.md5()
    m.update(uri.encode('utf-8'))
    return m.hexdigest()

  @classmethod
  def get_bookmark_for_digest(cls, digest):
    return cls.all().filter('uri_digest =', digest).get()

  @classmethod
  def get_bookmark_for_uri(cls, uri):
    return cls.get_bookmark_for_digest(cls.get_digest_for_uri(uri))


class Tag(db.Model):
  account = db.ReferenceProperty(Account, collection_name='tags')
  name = db.StringProperty(required=True)
  count = db.IntegerProperty(default=0)

  def __repr__(self):
    return u'<Tag: %s(%s)>' % (self.name, self.count)

  @classmethod
  def update_tags(cls, account, added=[], removed=[]):
    # TODO Code duplication here
    account_key_name = account.key().name()
    tag_keys = ('%s:%s' % (account_key_name, tag) for tag in added)
    tags = []
    for name, tag in itertools.izip(added, cls.get_by_key_name(tag_keys)):
      if tag is None:
        tags.append(cls(account=account,
                        key_name='%s:%s' % (account_key_name, name),
                        name=name,
                        count=1))
      else:
        tag.count += 1
        tags.append(tag)
    db.put(tags)

    tag_keys = ('%s:%s' % (account_key_name, tag) for tag in removed)
    tags = []
    for name, tag in itertools.izip(added, cls.get_by_key_name(tag_keys)):
      if tag is None:
        # Though this shouldn't be happened
        continue
      else:
        tag.count -= 1
        tags.append(tag)
    db.put(tags)


class Import(db.Model):
  PENDING = 1
  DONE = 2

  account = db.ReferenceProperty(Account, collection_name='imports')
  blob = blobstore.BlobReferenceProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  processed = db.DateTimeProperty()
  status = db.IntegerProperty(default=PENDING)
