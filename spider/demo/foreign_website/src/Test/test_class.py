from spider.Html import Request


class Test_request:


    def __init__(self):
        self.url = 'http://python.jobbole.com/80994/'

    def run(self):
        with Request(self.url) as r:
            print(r.text)
            
