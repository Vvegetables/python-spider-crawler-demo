import sys
from os.path import abspath
from os.path import dirname
import app
import logging


logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(filename)s[line:%(lineno)d] \
    %(levelname)s %(message)s',
    filename='Data/web_log.txt'
    )


sys.path.insert(0, abspath(dirname(__file__)))
application = app.configured_app()
