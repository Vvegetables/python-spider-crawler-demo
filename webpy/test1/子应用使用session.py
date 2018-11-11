#coding=utf-8
#web.py默认session信息只能在主应用中共享，即便在其他模块中import Session都不行。在app.py（或main.py）可以这样初始化session：

session = web.session.Session(app, web.session.DiskStore('sessions'),
initializer = {'test': 'woot', 'foo':''})
#.. 接下来创建一个被web.loadhook加载的处理器(processor)

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))
#.. 在子应用(假设是sub-app.py)中，可以这样操作session:

print(web.ctx.session.test)
web.ctx.session.foo = 'bar'