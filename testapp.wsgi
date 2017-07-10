import os
import sys

path = '/var/www/testapp'
if path not in sys.path:
    sys.path.append(path)

from run import app as application
