import hashlib
import web    

def POST(self):
    i = web.input()

    authdb = sqlite3.connect('users.db')
    pwdhash = hashlib.md5(i.password).hexdigest()
    check = authdb.execute('select * from users where username=? and password=?', (i.username, pwdhash))
    if check: 
        session.loggedin = True
        session.username = i.username
        raise web.seeother('/results')   
    else: return render.base("Those login details don't work.")