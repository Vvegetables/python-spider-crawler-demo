#coding=utf-8

import logging
import time


# logging.basicConfig(filename='example.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
 
# logging.basicConfig(format='%(asctime)s -- %(levelname)s:%(message)s', level=logging.DEBUG)
# logging.debug('This message should appear on the console')
 
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')