#coding=utf-8
class InnerMethodTest(object):
    q = 'o'
    def __init__(self,a=1,b=2):
        self.a = a
        self.b = b
        self.c = 3
        self.d = 4
    def __call__(self):
        print 'this is a method of __call__'
    def __get__(self,instance,owner):
        print 'this is __get__ method'#,instance,owner
        return self
    def __set__(self,instance,value):
        print '__set__ method',instance
    def __delete__(self,instance):
        print '__delete__ method'
#     def __del__(self):
#         print '__del__'
    def __getattribute__(self, *args, **kwargs):
        return object.__getattribute__(self, *args, **kwargs)
    def __getattr__(self,name):
        print 'this name={} is not exists'.format(name)
        return name
    
class Outer(object):
    s = InnerMethodTest(1,2)

#getattr(),setattr(),delattr()

    
inner = InnerMethodTest()
out = Outer()

print InnerMethodTest.__name__

print out.s.a   #调用了 __get__方法
out.s = 3 #调用了__set__方法
del out.s #调用了__delete__方法
