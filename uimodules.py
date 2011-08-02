import tornado.web

class Form(tornado.web.UIModule):
  def render(self, form):
    return self.render_string('module-form.html', form=form)


class Bookmark(tornado.web.UIModule):
  def render(self, bookmark):
    return self.render_string('module-bookmark.html', bookmark=bookmark)

