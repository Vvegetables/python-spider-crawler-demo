#coding=utf-8
'''
https://blog.csdn.net/freeking101/article/details/53020865


https://max.book118.com/html/2016/1227/77555145.shtm


web.input()?
开发子程序？
web.seeother() 303
web.redirect() 301
web.header('Content-Type','Text/xml')
web.ctx 客户端信息
web.ctx.env.get('HTTP_REFFER','http://google.com')
web.ctx.environ
web.Request
web.Response


def POST():
	data = web.data()


'''

import web
import another_app
# import sys, logging
# from wsgilog import WsgiLog, LogIO
# import config

urls = (
	"/blog",another_app.app_blog,
	'/(.*)/','redirect',
	'/', "Index",
	'/(.*)','Guest',
	

)

app = web.application(urls,globals())

#模板公共变量
t_globals = {
	"datestr" : web.datestr,
	"cookies" : web.cookies,
}


 
login = web.form.Form(  
                      web.form.Textbox('username'),  
                      web.form.Password('password'),  
                      web.form.Button('login')  
                      )


# 注意：在模板内的变量,如果包含有HTML 标记,以$ 方式引用变量的话,
# HTML 标记只会以纯文本的显示出来。要想HTML 标记产生效果，
# 可以用$: 引用变量

render = web.template.render('templates/')

#相当于django中的中间件
def my_processor(handler):
	print("before handling")
	result = handler()
	print("after handling")
	return result

app.add_processor(my_processor)
'''
def my_loadhook():
	print("my load hook")

def my_unloadhook():
	print("my unload hook")

app.add_processor(web.loadhook(my_loadhook))
app.add_processor(web.unloadhook(my_unloadhook))
'''

#无效
# class Log(WsgiLog):
#     def __init__(self, application):
#         WsgiLog.__init__(
#             self,
#             application,
#             logformat = '%(message)s',
#             tofile = True,
#             file = config.log_file,
#             interval = config.log_interval,
#             backups = config.log_backups
#             )
#         sys.stdout = LogIO(self.logger, logging.INFO)
#         sys.stderr = LogIO(self.logger, logging.ERROR)




#保证网址有无/结尾，都能指向同一个类。
class redirect:
	def GET(self,path):
		web.seeother('/' + path)


class Index:
	def GET(self):
		# login_form = login()
		# posts = []
		return render.base()
		# return 'Hello World!'
class Guest:
	def GET(self,name):
		if name:
			return render.guest_name(name)
		else:
			return render.base()

'''
对web.py而言，设置/获取Cookie非常方便。

###设置Cookies ####概述 setcookie(name, value, expires=””, domain=None, secure=False):

name (string) - Cookie的名称，由浏览器保存并发送至服务器。
value (string) -Cookie的值，与Cookie的名称相对应。
expires (int) - Cookie的过期时间，这是个可选参数，它决定cookie有效时间是多久。以秒为单位。它必须是一个整数，而绝不能是字符串。
domain (string) - Cookie的有效域－在该域内cookie才是有效的。一般情况下，要在某站点内可用，该参数值该写做站点的域（比如.webpy.org），而不是站主的主机名（比如wiki.webpy.org）
secure (bool)- 如果为True，要求该Cookie只能通过HTTPS传输。.
'''


class CookieSet:
    def GET(self):
        i = web.input(age='25')
        web.setcookie('age', i.age, 3600)
        return "Age set in your cookie"

class CookieGet:
    def GET(self):
        age=web.cookies().get('age')
        if age:
            return "Your age is: %s" % age
        else:
            return "Cookie does not exist."


def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")

    # You can use template result like below, either is ok:
    #return web.notfound(render.notfound())
    #return web.notfound(str(render.notfound()))

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")

#自定义404
class example:
    def GET(self):
        raise web.notfound()



app.internalerror = internalerror
app.notfound = notfound


if __name__ == "__main__":
	app.run(Log)


'''
另外两种模板方法
1.
  render=web.template.frender("templates/index.html")
  return render("Lisa")
2.
  template = "$def with (name)\nHello $name"
  render = web.template.Template(template)
  return render("Lisa")

'''