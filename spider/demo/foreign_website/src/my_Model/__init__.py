#coding=utf-8

import hashlib
import json
from operator import or_
import random
import time
import urllib
import urllib2

import MySQLdb
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.expression import or_

from settings import SqlAlchemy, LOGIN


from sqlalchemy import(
    Column,
    String,
    create_engine,
    INTEGER,
    Text,
    func,
    Date,
)
 
def engine():
    engine = create_engine(SqlAlchemy)
    return engine
 
e = engine()
Session = sessionmaker(bind=engine)
 
def DBsession():
    session = sessionmaker(bind=e)
    return session()

def get_all_spidered_urls(en_university,region):
    urls = DBsession().query(Data.url).filter(Data.en_university == en_university,Data.region == region).all()
    myset = set()
    for url in urls:
        myset.add(url[0])
    return myset


 
class Sql:
 
    def __init__(self, engine=e):
        self._session = sessionmaker(bind=engine)
        self._s  = self._session()
    
    def commit(self):
        
        self._s.commit()
        
    def get_all_spidered_urls(self):
        myset = set(self._s.query(Data).all())
        return myset
    
    
    def __enter__(self):
        return self._s
 
    def __exit__(self, exc_type, exc_value, exc_tb):
        self._s.commit()
        self._s.close()
        del self
 
 
Base = declarative_base()
 
 
class Data(Base):
 
    __tablename__ = 't_articles'
    id = Column('id', INTEGER, primary_key=True)
    university = Column('university', String(length=255), nullable=True)
    en_university = Column('en_university', String(length=255), nullable=True)
    region = Column('region', String(length=255), nullable=True)
#     department = Column('department', String(length=255), nullable=True)
#     teacher = Column('teacher', String(length=255), nullable=True)
    title = Column('title', String(length=255), nullable=True)
    content = Column('content', Text())
    url = Column('url', String(length=1000), nullable=True)
    createtime = Column('createtime',Date())
    trans_title = Column('trans_title', String(length=255), nullable=True)
    trans_content = Column('trans_content', Text())
 
    @classmethod
    def universitys(cls):
        with Sql() as s:
            u = s.query(cls.university).group_by(cls.university).all()
        if u:
            u = [i[0] for i in u]
        return u
 
    @classmethod
#     def departments(cls, university):
#         with Sql() as s:
#             d = s.query(cls.title).filter(cls.university == university).group_by(cls.department).all()#cls.department
#         if d:
#             d = [i[0] for i in d]
#         return d
 
    @classmethod
    def count_data(cls, **kwargs):
        with Sql() as s:
            nums = s.query(
                func.count(cls.id)
                ).filter_by(
                    **kwargs
                ).scalar()
        return nums
 
 
class CompletedUniversity(Base):
 
    __tablename__ = 't_completed_articles'
    id = Column('id', INTEGER, primary_key=True)
    university = Column('university', String(length=255), nullable=True)
#     department = Column('department', String(length=255), nullable=True)
    region = Column('region', String(length=255), nullable=True)
    en_university = Column('en_university', String(length=255), nullable=True)
    title = Column('title', String(length=255), nullable=True)
    url = Column('url', String(length=1000), nullable=False)
 
    @classmethod
    def save_from_txt(cls, file_name):
        with open(file_name, 'r') as f:
            datas = f.readlines()
        d_list = []
        for data in datas:
            data = eval(data)
            print(data)
            d = cls(
                university=data['university'],
                en_university=data['en_university'],
#                 department=data['department'],
                url=data['url'],
                title = data['title'],
                region = data['region'],
            )
            d_list.append(d)
        with Sql() as s:
            for d in d_list:
                s.add(d)

 
class User:
 
    @staticmethod
    def verify_login(username, password):
        return username == LOGIN['username'] and password == LOGIN['password']


# import MySQLdb
# 
# class myDB:
#     def __init__(self):
#         self.db = MySQLdb.connect('118.31.168.208','hanyj','CingHTa#1234','paTest')#,charset='utf8mb4'
#         self.cursor = self.db.cursor()
# #         self.result = [] 
#     def data_query(self,sql_query):
#         return self.cursor.execute(sql_query)
#     
#     def data_execute(self,sql_query):
#         try:
#             self.cursor.execute(sql_query)
#             self.db.commit()
#         except:
#             self.db.rollback()
#     def close(self):
#         self.db.close()







class youdao:
    u = 'fanyideskweb'
    l = 'aNPG!!u6sesA>hBAW1@(-'
    s = requests.session()
    i = None
    sendstr = None
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    head = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Content-Length':'200',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    @classmethod
    def set_salt(cls):
        cls.i = str(int(time.time()*1000)+random.randint(1,10))
    @classmethod
    def set_sendstr(cls,t):
        i = str(int(time.time()*1000)+random.randint(1,10))
        src = cls.u + t + cls.i + cls.l 
        m2 = hashlib.md5()
        m2.update(src.encode('utf-8'))
        cls.sendstr = m2.hexdigest()
    @classmethod
    def set_headers(cls,header):
        cls.head.update(header)
    @classmethod
    def set_session(cls):
        cls.head['Cookie'] = 'OUTFOX_SEARCH_USER_ID=833904829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1846816080.1245883;  ___rl__test__cookies='+str(time.time()*1000)
    @classmethod
    def fanyi(cls,en):
        cls.set_session()
        cls.set_salt()
        cls.set_sendstr(en)
        data = {
            'i': en,
            'from':'AUTO',
            'to':'AUTO',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'salt':cls.i,
            'sign':cls.sendstr,
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_REALTIME',
            'typoResult':'false'
        }
        p = cls.s.post(cls.url,data=data,headers=cls.head)
#         time.sleep(1)
        # print res
        try:
#             print p.text
            res = json.loads(p.text)
            try:
                str_sum = []
                for r in res['translateResult']:
                    for t in r:
                        str_sum.append(t['tgt'].encode('utf-8'))
                kk = ''.join(str_sum)
                return kk
            except:
#                 print kk
                return ''
        except:
            try:
                browser = selenium_conf()
                res = selenium_spider(browser,en)
                selenium_close(browser)
                return res
            except:
                print 'selenium_wrong'
                return ''




def translate_title():
    s = DBsession()
    datas = s.query(Data).filter(or_(Data.trans_title == '',Data.trans_title==None)).all()
    for i,data in enumerate(datas,1):
        print "title:" + str(i)
        data.trans_title = youdao.fanyi(data.title)
    s.commit()

def translate_content():
    s = DBsession()
    datas = s.query(Data).filter(or_(Data.trans_content == '',Data.trans_content==None)).all()
    for i,data in enumerate(datas,1):
#         strip_d = data.content.replace("\n",'').replace("\r",'')
#         print strip_d
        print 'content:' + str(i)
        data.trans_content = youdao.fanyi(data.content)
    s.commit()



def selenium_conf():
    
    exe = 'C:\\Users\\Zcxu\\Downloads\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
    # driver = 'C:\\Users\\Zcxu\\Downloads\\chromedriver_win32\\chromedriver.exe'
    # browser = webdriver.Chrome(driver)
    browser = webdriver.PhantomJS(exe)
    
    browser.get('http://fanyi.youdao.com/')
    time.sleep(1)
    return browser

def selenium_close(browser):
    
    browser.quit()


def selenium_spider(browser,content):
    try:
        browser.find_element_by_class_name("guide-con").click()
    except ElementNotVisibleException:
        time.sleep(1)
    time.sleep(2)
    
    try:
        browser.find_element_by_class_name("i-know").click()
    except ElementNotVisibleException:
        time.sleep(1)
    time.sleep(1)
    
    browser.find_element_by_id("inputOriginal").send_keys(content)
    time.sleep(2)
    
    browser.find_element_by_id("transMachine").click()
    # ps = browser.find_elements_by_xpath('//div[@id="transTarget"]/p/span')
    s_sum = []
    for s in browser.find_elements_by_xpath('//div[@id="transTarget"]/p/span'):
        s_sum.append(s.text)
    res = ''.join(s_sum)
#     browser.quit()
    return res



if __name__ == '__main__':
    
    translate_title()
    translate_content()
    
#     datas = s.query(Data).filter(or_(Data.trans_title == '',Data.trans_title==None)).all()






