from .base import *

try:
    from .local import *
except ImportError:
    print("Can't find module settings/local.py! Make it from settings/local.py.skeleton!")
