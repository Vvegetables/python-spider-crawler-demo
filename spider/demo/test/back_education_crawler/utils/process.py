#coding=utf-8
import Queue
from datetime import datetime
import json
import os
import re
import socket
import sys 
import threading
import time
from urlparse import urljoin

import chardet
from lxml import etree
import requests

from models import Sql, EducationNews,db_get_urls,db_get_titles,ForeignEduNews
from back_education_crawler.utils.self_excel import excel_read, get_excel_cell_data, \
    get_single_column_data
from back_education_crawler.utils.dynamic_func import DynamicJSHandler

reload(sys)
sys.setdefaultencoding('utf-8')


    

class SelfProcess:
    
    def __init__(self,_type,_start_url=None,deep = 1,path = None,timeout=5,_model=EducationNews):
#         self.sheet = excel_read(path)
        self.url = db_get_urls(_type)#get_single_column_data(self.sheet,3) or _start_url
        self.deep = deep
        self.timeout = timeout
        self.data_q = Queue.Queue()
        self.url_q = Queue.Queue()
        self.spided_urls = Sql(_model=EducationNews).get_all_spidered_urls()
        self.crawled_items = []
#         self.sheettitle = []
        self.stop_flag = False
        self.strip_spaces = re.compile('\s+')
        self.encoding = None
        self.urlname = None
        self.titles = set()
        self.cmp_title = ['陕西']
        self._model = _model
        self._type = _type
        self._titles,self.subtitles = db_get_titles(_type)
        
    
        
    def spider(self):
        if not isinstance(self.url,(list,tuple)):
            self.url = [self.url]
        for k,e_url in enumerate(self.url,0):
#             q = self.url_q
            self.url_q.queue.clear()
            try:
                address = self._titles[k]
                source = address + (('_' + self.subtitles[k]) if self.subtitles[k] else '')
                self.urlname = address
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
                            _error_dict = {}
                            _error_dict['url'] = c_url 
                            _error_dict['level'] = 'error'
                            _error_dict['time'] = str(datetime.now())
                            _error_dict['reason'] = '获得response'
                            _error_dict['source'] = source
                            f.write(json.dumps(_error_dict,ensure_ascii=False))  #.decode('utf8').encode('gb2312')
                            f.write(os.linesep)
            
                    _html = self.get_html(_response)
                    self.get_data(_html,e_url,_response)
                    for item in self.crawled_items:
                        item.append(source)
                        self.url_q.put(item[1])
                        if item[0] and (filter(lambda x:x in self.urlname,self.cmp_title)):
                            self.data_q.put({'title':item[0],'link':item[1],'source':item[2],'check_title':'1'})
                        else:
                            self.data_q.put({'title':item[0],'link':item[1],'source':item[2]})
#                             print item[0],item[1]
                    self.crawled_items = []
                if self.url_q.empty():
                    break
                deep += 1
        
        self.data_q.put(None)
        self.stop_flag = True
        
                
    
    def handle_url(self,url,method='GET',*args,**kwargs):
        timeout = self.timeout
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
        except Exception,e:
            print e
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
#         cD = chardet.detect(response.content)
#         CHARSET = 'utf-8'
#         charset = response.encoding
#         self.encoding = charset
#         if charset.startswith('gb') or charset.startswith('GB') or charset.startswith('ISO') or charset.startswith('iso'):
#             self.encoding = 'gb2312'
#         else:
#             self.encoding = 'utf-8'
#         response.encoding = charset
        return response
    
    def get_html(self,response):
        if hasattr(response,'error'):
            return None
        charset = response.encoding
        self.encoding = charset
        if charset and (charset.startswith('gb') or charset.startswith('GB')):
            self.encoding = 'GBK'
        elif charset and (charset.startswith('ISO') or charset.startswith('iso')):
            self.encoding = 'gb2312'
        elif charset:
            self.encoding = 'utf-8'
#         response.encoding = charset
        text = response.content.replace('?xml','head')
#         response.content.decode('GBK')
        try:
            text = text.decode(self.encoding)
        except:
            try:
                text = text.decode('GBK')
            except:
                try:
                    text = text.decode('gb2312')
                except:
                    try:
                        text = text.decode('utf-8')
                    except:
                        pass
        return etree.HTML(text)
    
    def get_data(self,html,main_url,response):
        if not html:
            return
        infos = html.xpath('//a')
        count = 0
        for info in infos:
            url = ''.join(info.xpath('@href'))
            abs_url = urljoin(main_url, url)
#             if abs_url == 'http://www.cas.cn/syky/201807/t20180702_4656749.shtml':
#                 pass
            if abs_url in self.url or (abs_url not in self.spided_urls):
                title = info.xpath('string(.)').strip()
                _title = ''.join(info.xpath('@title')).strip()
                
                title = _title if _title else title
                
#                 if not title:
#                     title = ''.join(html.xpath('//head/title/text()')).strip()
#                 if not title.strip():
#                     title = ''.join(info.xpath('//img/@title'))
                if title and len(title) > 8:
                    title = re.sub(self.strip_spaces,'',title)
                    abs_url = re.sub(self.strip_spaces,'',abs_url)
                    if self.urlname and (filter(lambda x:x in self.urlname,self.cmp_title)):
                        if title and title not in self.titles:
                            self.titles.add(title)
                            self.crawled_items.append([title,abs_url])
                    else:
                        self.crawled_items.append([title,abs_url])
                    count += 1    
                    self.spided_urls.add(abs_url)
        
        if count <= 5:
            time.sleep(3)
            with DynamicJSHandler() as dy_handler:
                for dy_data in dy_handler.get_label_a(response.url):
                    _text,_title,_url = dy_data
                    abs_url = urljoin(response.url, _url)
                    if abs_url in self.url or (abs_url not in self.spided_urls):
                        _text = _text.strip()
                        title = _title.strip()
                        title = title if title else _text
                         
                        if title and len(title) > 8:
                            title = re.sub(self.strip_spaces,'',title)
                            abs_url = re.sub(self.strip_spaces,'',abs_url)
                            if self.urlname and (filter(lambda x:x in self.urlname,self.cmp_title)):
                                if title and title not in self.titles:
                                    self.titles.add(title)
                                    self.crawled_items.append([title,abs_url])
                            else:
                                self.crawled_items.append([title,abs_url])
                            count += 1    
                            self.spided_urls.add(abs_url)
    
    def save_database(self):
        count = 0
        with Sql(_model=self._model) as s:
            while True:
                _data = self.data_q.get()
                
                if _data is None and self.stop_flag:
        #                 return
                    break
                if _data is None:
                    time.sleep(2)
                    continue
                
                for key,value in _data.items():
                    if not isinstance(value,unicode): 
                        detect_res = chardet.detect(value)
                        enc = detect_res.get('encoding',None)
                        if enc:
                            value.decode(enc).encode('utf-8')
                    else:
                        value = value.encode('utf-8')        
                    _data[key] = value
                        
                if (_data.get('title') is None) or (not(_data.get('title'))):# or (not(_data.get('link').endswith('htm') or _data.get('link').endswith('html'))):
                    continue
#                 logging.info(_data)
                try:
                    if _data.has_key('check_title'):
                        if not s.query(self._model).filter(self._model.title == _data.get('title')).first():#EducationNews.title == _data.get('title'),
                            _data['createtime'] = datetime.now()
                            _data.pop("check_title")
                            s.add(
                                self._model(**_data)
                            )
                            count += 1
                            print("download:" + str(count) + ',' + datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
                    else: 
                        if not s.query(self._model).filter(self._model.link == _data.get('link')).first():#EducationNews.title == _data.get('title'),
                            _data['createtime'] = datetime.now()
                            s.add(
                                self._model(**_data)
                            )
                            count += 1
                            print("download:" + str(count) + ',' + datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
    #                     else:
    #                         print "download:pass," + datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                    
                    if count > 0 and count % 5 == 0:
                        s.commit()
                except Exception,e:
                    print e
                    with open('error.log','a') as f:
                        _error_dict = {}
                        _error_dict.update(_data)
                        _error_dict['level'] = 'error'
                        _error_dict['time'] = str(datetime.now())
                        _error_dict['reason'] = '数据库插入'
                        if _error_dict.has_key('createtime'):
                            _error_dict['createtime'] = str(_error_dict['createtime'])
                        f.write(json.dumps(_error_dict,ensure_ascii=False))  #.decode('utf8').encode('gb2312')
                        f.write(os.linesep)
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