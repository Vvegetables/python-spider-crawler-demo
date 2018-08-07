#coding=utf-8
import datetime
from functools import wraps


#初级装饰器
def simple_decorator(func):
    def wrapper():
        print "[DEBUG]:enter{}()".format(func.__name__)
        return func()
    return wrapper

def say_hello():
    print "hello"

say_hello = simple_decorator(say_hello)



#晋级

@simple_decorator
def say_hello2():
    print 'hello!'
    
#再次晋级，被装饰的函数带上参数
def middle_decorator(func):
    def wrapper(*args,**kwargs):
        print "[DEBUG]:enter{}()".format(func.__name__)
        print 'prepare and say...'
        return func(*args,**kwargs)
    return wrapper

@middle_decorator
def say_hello3(something):
    print "hello{}!".format(something)


#高级写法,带参数的装饰器

def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print "[{level}]: enter function {func}()".format(
                level=level,
                func=func.__name__)
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper

@logging(level='INFO')
def say(something):
    print "say {}!".format(something)

# 如果没有使用@语法，等同于
# say = logging(level='INFO')(say)

@logging(level='DEBUG')
def do(something):
    print "do {}...".format(something)


#类装饰器

class logging_(object):
    def __init__(self, level='INFO'):
        self.level = level
        
    def __call__(self, func): # 接受函数
        def wrapper(*args, **kwargs):
            print "[{level}]: enter function {func}()".format(
                level=self.level,
                func=func.__name__)
            func(*args, **kwargs)
        return wrapper  #返回函数

@logging(level='INFO')
def say_(something):
    print "say {}!".format(something)
    
#----------------------------------    
#类装饰器
# -*- coding:utf-8 -*-
from functools import wraps
from datetime import datetime

#类的装饰器写法，日志
class log(object):
    def __init__(self, logfile='c:\out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):                     
            self.writeLog(*args, **kwargs)    # 先调用 写入日志         
            return func(*args, **kwargs)     # 正式调用主要处理函数       
        return wrapped_func

    #写入日志    
    def writeLog(self, *args, **kwargs):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_str = time+' 操作人:{0[0]} 进行了【{0[1]}】操作'.format(args)           
        with open(self.logfile, 'a',encoding='utf8') as file:
            file.write(log_str + '\n')

@log()
def myfunc(name,age):
    print('姓名：{0},年龄：{1}'.format(name,age))

if __name__ == '__main__':
    myfunc('小白', '查询')
    myfunc('root', '添加人员')
    myfunc('小小', '修改数据')


#-------------------------------------------------


def logging2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """print log before a function."""
        print "[DEBUG] {}: enter {}()".format(datetime.datetime.now(), func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logging
def say2(something):
    """say something"""
    print "say {}!".format(something)

print say.__name__  # say
print say.__doc__ # say something


