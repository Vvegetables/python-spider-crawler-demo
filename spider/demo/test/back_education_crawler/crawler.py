#coding=utf-8
import os
import time

from utils.models import ForeignEduNews
from utils.process import SelfProcess


if __name__ == '__main__':
#     path = os.path.dirname(__file__)
#     path = os.path.join(path,'data','cingta.xlsx')
    sp = SelfProcess(_type=0,timeout=15)
    sp.run()
    time.sleep(10)
    sp2 = SelfProcess(_type=1,_model=ForeignEduNews,timeout=30)
    sp2.run()