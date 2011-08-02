import tornado.web

class Form(tornado.web.UIModule):
  def render(self, form):
    return self.render_string('module-form.html', form=form)


class Bookmark(tornado.web.UIModule):
  def render(self, bookmark):
    return self.render_string('module-bookmark.html', bookmark=bookmark)


class AddBookmarkBookmarklet(tornado.web.UIModule):
  def render(self):
    return '<a class="button icon like" ' \
       'href="javascript:e=encodeURIComponent;u=e(location.href);' \
       's=document.getSelection;d=\'\';' \
       'if(document.getSelection){d=document.getSelection();}' \
       't=e(document.title);' \
       'open(\'' + self.request.protocol + "://" + self.request.host + '/new?p=1' \
       '&uri=\'+u+\'&title=\'+t+\'&description=\'+d,\'bookmarklove\',' \
       '\'toolbar=no,width=700,height=350\');">Add Bookmark</a>'


class ReadLaterBookmarklet(tornado.web.UIModule):
  def render(self):
    return '<a class="button icon pin" '                                     \
       'href="javascript:e=encodeURIComponent;u=e(location.href);'       \
       's=document.getSelection;d=\'\';if(document.getSelection){'         \
       'd=document.getSelection();}'                                     \
       't=e(document.title);'                                            \
       'w=open(\'' + self.request.protocol + "://" + self.request.host + '}}/new?p=1'  \
       '&uri=\'+u+\'&title=\'+t+\'&unread=1\'+\'&description=\'+d,'      \
       '\'bookmarklove\',\'toolbar=no,width=10,height=10\');w.blur();'   \
       '">Read Later</a>'
