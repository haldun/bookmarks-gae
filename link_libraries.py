import os

import tornado
os.symlink(os.path.dirname(tornado.__file__), 'tornado')

import wtforms
os.symlink(os.path.dirname(wtforms.__file__), 'wtforms')
