#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
#from web import background, backgrounder
from web.background import background
from web.backgrounder import backgrounder
from datetime import datetime; now = datetime.now
from time import sleep

urls = (
    '/', 'index',
    )

apps = web.application(urls,globals())

class index:
    @backgrounder
    def GET(self):
        print("Started at %s" % now())
        print("hit f5 to refresh!")
        longrunning()
        return "aaa"
        

@background
def longrunning():
    for i in range(10):
        sleep(1)
        print("%s: %s" % (i, now()))

if __name__ == '__main__':
    apps.run()