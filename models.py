import hashlib

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


class Import(db.Model):
  PENDING = 1
  DONE = 2

  account = db.ReferenceProperty(Account, collection_name='imports')
  blob = blobstore.BlobReferenceProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  processed = db.DateTimeProperty()
  status = db.IntegerProperty(default=PENDING)
