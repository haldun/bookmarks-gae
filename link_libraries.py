import os
import html5lib
import tornado
import wtforms

try:
  os.symlink(os.path.dirname(tornado.__file__), 'tornado')
except:
  pass

try:
  os.symlink(os.path.dirname(wtforms.__file__), 'wtforms')
except:
  pass

try:
  os.symlink(os.path.dirname(html5lib.__file__), 'html5lib')
except:
  pass
