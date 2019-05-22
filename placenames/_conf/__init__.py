from os.path import dirname, realpath, join, abspath
from .db import *
from .secrets import *


APP_DIR = dirname(dirname(realpath(__file__)))
TEMPLATES_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'templates')
STATIC_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'static')


LOGFILE = APP_DIR + '/flask.log'
DEBUG = True


JURISDICTION_INSTANCE_URI_STEM = 'http://localhost:5000/jurisdiction/'
GAZETTEER_INSTANCE_URI_STEM = 'http://localhost:5000/gazetteer/'