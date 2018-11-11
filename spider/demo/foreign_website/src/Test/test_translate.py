#coding=utf-8
import MySQLdb
import urllib
import urllib2
import json
import time
import hashlib
import MySQLdb

import requests
import time
import random
import hashlib
import json


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
        m2.update(src)
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
        res = json.loads(p.text)
        # print res
        return res['translateResult'][0][0]['tgt'].encode('utf-8')


class connect:
    db_instance = None
    def __init__(self,):
        pass
    @classmethod    
    def get_instance(cls):
        if not cls.db_instance:
            cls.db_instance = MySQLdb.connect('118.31.168.208','hanyj','CingHTa#1234','paTest',charset='utf8') 
        return cls.db_instance
    @classmethod
    def translate_title(cls):
        db = cls.get_instance()
        cursor = db.cursor()
        cursor.execute("SET NAMES utf8mb4")
        query_sql = "SELECT id,title FROM t_articles WHERE `trans_title` IS NULL OR `trans_title` = '';"

        #执行
        cursor.execute(query_sql)
        
        results = cursor.fetchall()
        for res in results:
            zh_cn = youdao.fanyi(res[1])
            query_sql = "UPDATE t_articles SET `trans_title`=%s WHERE id = %d" % (zh_cn,res[0]);
            #执行
            print res[0]
            cursor.execute(query_sql)
        cursor.close()
    @classmethod
    def translate_content(cls):
        db = cls.get_instance()
        cursor = db.cursor()
        query_sql = '''
            SELECT * FROM t_articles WHERE `trans_content` IS NULL OR `trans_content` = '';

        '''
        #执行
        cursor.execute(query_sql)
        results = cursor.fetchall()
        for res in results:
            zh_cn = youdao.fanyi(res[4])
            query_sql = "UPDATE t_articles SET `trans_content`=%s WHERE id = %d" % (zh_cn,res[0]);
            #执行
            cursor.execute(query_sql)

connect.translate_title()
connect.get_instance().close()
# print youdao.fanyi('Accessibility')