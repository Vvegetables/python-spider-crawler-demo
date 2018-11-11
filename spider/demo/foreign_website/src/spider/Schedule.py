#coding=utf-8
import logging
import os
import thread
import threading
import time

import MySQLdb
import queue

from my_Model import Data, Sql, DBsession, get_all_spidered_urls
import settings
from spider.Content import Content, Scontent
from spider.Html import URL
from utils.util import delete_trash_word
from datetime import datetime


# from my_Model import myDB
class Schedule:

    def __init__(
                self, url, university, en_university,region,#department
                slowdown='None',
#                 list_first_name=[],
                deep=1,
                ):

        self.start_url = url
        self.deep = deep
        self.url_q = queue.Queue()
#         self.spided_urls = set() #保存已经访问过的url
        
        self.data_q = queue.Queue()
        self.university = university
        self.region = region,
        self.en_university = en_university,
        self.spided_urls = get_all_spidered_urls(en_university=self.en_university,region=self.region)
#         self.department = department
#         self.list_first_name = list_first_name
        self.slowdown = slowdown
        self.max_len = 500
        self.counter = 1
        

    def spider(self):
        self.url_q.put(self.start_url)  #url队列
        deep = 0
        while not self.url_q.empty() and deep < self.deep:
            
            c_url = self.url_q.get() #取出一个url
#             print c_url
            if c_url in self.spided_urls: #访问过的url跳过
                continue
            c_u = URL(c_url)    #对url进行处理，获得response
            n_url_items = c_u.url_items #对response处理，返回name和name对应的链接（set）
            if len(n_url_items) > self.max_len:
                n_url_items = set(list(n_url_items)[:500])
                
            for n_url, n_title in n_url_items:
                
#                 n_title = delete_trash_word(n_title)
#                 if n_url not in self.spided_urls and \
#                 Content.verify_name(n_title, self.list_first_name):
                if n_url not in self.spided_urls and Scontent.check_url(self.start_url, n_url): 
                    n_u = URL(n_url)
                    
#                     n_n_items = n_u.url_items

#                     probability, content = Content.compare_content(
#                         c_u.text, n_u.text)
#                     if probability > 0.005:
#                         content = content
#                     else:
#                         content = Content(n_u.text).content
                    #处理文本
                    res1 = Scontent.get_result(c_url,c_u.text)
                    res2 = Scontent.get_result(n_url,n_u.text)
                    content,title = '',''
                    if res1['content'] and res1['title']:
                        content = res1['content']
                        title = res1['title']
                    if res2['content'] and res2['title']:
                        content = res2['content']
                        title = res2['title']
                    if content and title:
                        data = dict(
                            content=content,
                            university=self.university,
    #                         department=self.department,
                            url=n_url,
                            title = title,
                            region = self.region,
                            en_university = self.en_university,
                            createtime = datetime.now(),
    #                         teacher=n_title,
                        )
                        self.data_q.put(data)
                        print('spider:' + str(self.counter) + ',' + datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
                        self.counter += 1
                    else:
                        print 'spider:pass,' + datetime.now().strftime("%Y-%m-%d %H:%I:%S")
#                     for n_n_url, n_n_title in n_n_items:
#                         self.url_q.put(n_n_url)
                    time.sleep(self.set_crawl_speed().get(self.slowdown, 0))
                else:
#                     self.url_q.put(n_url)
                    print "spider:pass," + datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                self.spided_urls.add(c_url)
            deep += 1
        self.data_q.put(None)

    def set_crawl_speed(self):
        r = {
            'None': 0,
            '1': 1,
            '2': 2,
            '5': 5,
            '10': 10,
        }
        return r

    def download(self):
        count = 1
#         print count
        with Sql() as s:
            while True:
                _data = self.data_q.get()
                
                if _data is None:
        #                 return
                    break
                for key,value in _data.items():
                    if isinstance(value,unicode): 
                        _data[key] = value.encode('utf-8')
#                 logging.info(_data)
                if not s.query(Data).filter(Data.title == _data.get('title'), Data.university == _data.get('university')).first():#Data.teacher == _data.get('teacher'), 
                    s.add(
                        Data(**_data)
                    )
                    print("download:" + str(count) + ',' + datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
                    count += 1
                else:
                    print "download:pass," + datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                if count % 5 == 0:
                    s.commit()
                
#                 if count == 20:
#                     break
#         while True:
#             _data = self.data_q.get()
#             if _data is None:
#                 break
#             for key,value in _data.items():
#                 if isinstance(value,unicode): 
#                     _data[key] = value.encode('utf-8')
#             sql = "insert into t_teachers(university,teacher,department,content,url) values({university},{teacher},{department},{content},{url})".format(**_data)
#             db = myDB()
#             db.data_execute(sql)
#     def func1(self):
#         a = 1
#         while True:
#             print a
    def run(self):
        t1 = threading.Thread(target=self.spider)
        t2 = threading.Thread(target=self.download)
#         t1 = thread.start_new_thread(self.spider,('thread-1',))
#         t2 = thread.start_new_thread(self.download,('thread-2',))
        t1.start()
#         time.sleep(2)
        t2.start()
        t1.join()
        t2.join()
