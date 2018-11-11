#coding=utf-8
import web

web.config.debug = True

urls = ("/", "hello")

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session

class hello:
   def GET(self):
       print('session', session)
       session.count += 1
       return 'Hello, %s!' % session.count

if __name__ == "__main__":
   app.run()