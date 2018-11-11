#coding=utf-8
'''
如果用数据库代替磁盘文件来存储session信息，
只要用DBStore代替DiskStore即可。
使用DBStore需要建立一个表

 create table sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

db = web.database(dbn='postgres', db='mydatabase', user='myname', pw='')
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'count': 0})

｀web.config｀中的sessions_parameters保存着session的相关设置，
sessions_parameters本身是一个字典，可以对其修改。默认设置如下：

web.config.session_parameters['cookie_name'] = 'webpy_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400, #24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
web.config.session_parameters['expired_message'] = 'Session expired'

cookie_name - 保存session id的Cookie的名称
cookie_domain - 保存session id的Cookie的domain信息
timeout - session的有效时间 ，以秒为单位
ignore_expiry - 如果为True，session就永不过期
ignore_change_ip - 如果为False，就表明只有在访问该session的IP与创建该session的IP完全一致时，session才被允许访问。
secret_key - 密码种子，为session加密提供一个字符串种子
expired_message - session过期时显示的提示信息。

'''

import web
web.config.debug = False
urls = (
    "/count", "count",
    "/reset", "reset"
)
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

class count:
    def GET(self):
        session.count += 1
        return str(session.count)
        
class reset:
    def GET(self):
        session.kill()
        return ""

if __name__ == "__main__":
    app.run()