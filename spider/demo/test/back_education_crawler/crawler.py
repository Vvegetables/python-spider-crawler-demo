#coding=utf-8
import os

from utils.process import SelfProcess


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    path = os.path.join(path,'data','cingta.xlsx')
    sp = SelfProcess(path=path)
    sp.run()