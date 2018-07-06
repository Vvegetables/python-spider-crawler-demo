#coding=utf-8
from datetime import datetime
import os
import socket
import threading
import time
from urlparse import urljoin

import chardet
from lxml import etree
import queue
import requests

from education_crawler.models import Sql, EducationNews
from education_crawler.utils.self_excel import excel_read, get_excel_cell_data, \
    get_single_column_data


class SelfProcess:
    
    def __init__(self,_start_url=None,deep = 2,path = None,timeout=5):
        self.sheet = excel_read(path)
        self.url = get_single_column_data(self.sheet,3) or _start_url
        self.deep = deep
        self.data_q = queue.Queue()
        self.url_q = queue.Queue()
        self.spided_urls = Sql().get_all_spidered_urls()
        self.crawled_items = []
        self.sheettitle = []
        self.stop_flag = False
    
        
    def spider(self):
        if not isinstance(self.url,(list,tuple)):
            self.url = [self.url]
        for k,e_url in enumerate(self.url,3):
            try:
                source = get_excel_cell_data(self.sheet,k,1) + '_' + get_excel_cell_data(self.sheet,k,2)
            except:
                source = ''
#             e_url = get_excel_cell_data(_url,k,3)
            if e_url:
                self.url_q.put(e_url)
            deep = 0
            while deep < self.deep:
                _end = self.url_q.qsize()
                for i in range(_end):
                    c_url = self.url_q.get()
                    if c_url not in self.url and (deep == self.deep - 1) and c_url in self.spided_urls:
                        continue
                    _response = self.handle_url(c_url)
                    if int(_response.status_code) > 200:
                        with open('error.log','a') as f:
                            f.write('error:'.encode('utf-8')+c_url.encode('utf-8')+os.linesep) 
                    _html = self.get_html(_response)
                    self.get_data(_html,e_url)
                    for item in self.crawled_items:
                        item.append(source)
                        self.url_q.put(item[1])
                        self.data_q.put({'title':item[0],'link':item[1],'source':item[2]})
                    self.crawled_items = []
                if self.url_q.empty():
                    break
                deep += 1
        
        self.data_q.put(None)
        self.stop_flag = True
        
                
    
    def handle_url(self,url,method='GET',timeout=5,*args,**kwargs):
        r = {
            'GET': requests.get,
            'POST': requests.post,
        }
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        try:
            response = r.get(method)(url, headers=headers,timeout=timeout, *args, **kwargs)
            if 'Connection' in response.headers.keys():
                del response.headers['Connection']
        except socket.timeout:
            print 'timeout'
            response = self.err_response()
        except:
            response = self.err_response()
        response = self.html_code(response)
        return response
    
    def err_response(self):
        class Response:
            text = ''
            error = True
            url = self.url
            status_code = '404'

            def __repr__(self):
                return 'Bad requests'
        return Response
    
    def html_code(self, response):
        if hasattr(response, 'error'):
            return response
        cD = chardet.detect(response.content)
        CHARSET = 'utf8'
        charset = cD.get('encoding', CHARSET)
        response.encoding = charset
        return response
    
    def get_html(self,response):
        if hasattr(response,'error'):
            return None
        text = response.text.replace('?xml','head')
        return etree.HTML(text)
    
    def get_data(self,html,main_url):
        if not html:
            return
        infos = html.xpath('//a')
        for info in infos:
            url = ''.join(info.xpath('@href'))
            abs_url = urljoin(main_url, url)
            if abs_url == 'http://www.cas.cn/syky/201807/t20180702_4656749.shtml':
                pass
            if abs_url not in self.spided_urls:
                title = info.xpath('string(.)').strip()
                _title = ''.join(info.xpath('@title')).strip()
                
                title = _title if _title else title
                
                if not title:
                    title = ''.join(html.xpath('//head/title/text()')).strip()
#                 if not title.strip():
#                     title = ''.join(info.xpath('//img/@title'))
                self.crawled_items.append([title,abs_url])
                self.spided_urls.add(abs_url)
    
    def save_database(self):
        count = 1
        with Sql() as s:
            while True:
                _data = self.data_q.get()
                
                if _data is None and self.stop_flag:
        #                 return
                    break
                if _data is None:
                    time.sleep(2)
                    continue
                
                for key,value in _data.items():
                    if isinstance(value,unicode): 
                        _data[key] = value.encode('utf-8')
                        
                if (_data.get('title') is None) or (not(_data.get('title').strip())):
                    continue
#                 logging.info(_data)
                if not s.query(EducationNews).filter(EducationNews.title == _data.get('title'),EducationNews.link == _data.get('link')).first():#Data.teacher == _data.get('teacher'), 
                    _data['createtime'] = datetime.now()
                    s.add(
                        EducationNews(**_data)
                    )
                    count += 1
                    print("download:" + str(count) + ',' + datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
                else:
                    print "download:pass," + datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                if count % 5 == 0:
                    s.commit()
    def run(self):
        t1 = threading.Thread(target=self.spider)
        t2 = threading.Thread(target=self.save_database)
#         t1 = thread.start_new_thread(self.spider,('thread-1',))
#         t2 = thread.start_new_thread(self.download,('thread-2',))
        t1.start()
#         time.sleep(2)
        t2.start()
        t1.join()
        t2.join() 