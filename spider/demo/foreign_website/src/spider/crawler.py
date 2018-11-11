# import logging
# import time
# 
# import queue
# 
# from spider.Content import Content
# from spider.Html import URL
# from spider.Model import Model
# from utils.util import delete_trash_word
# 
# 
# class Spider:
#     def __init__(
#                 self, url, university, department,
#                 slowdown='None',
#                 list_first_name=[],
#                 deep=1,
#                 ):
# 
#         self.start_url = url
#         self.deep = deep
#         self.url_q = queue.Queue()
#         self.spided_urls = set()
#         self.data_q = queue.Queue()
#         self.university = university
#         self.department = department
#         self.list_first_name = list_first_name
#         self.slowdown = slowdown
# 
#     def spider(self):
#         self.url_q.put(self.start_url)
#         deep = 0
#         while not self.url_q.empty() and deep < self.deep:
#             c_url = self.url_q.get()
#             if c_url in self.spided_urls:
#                 continue
#             c_u = URL(c_url)
#             n_url_items = c_u.url_items
#             for n_url, n_title in n_url_items:
#                 n_title = delete_trash_word(n_title)
#                 if n_url not in self.spided_urls and \
#                 Content.verify_name(n_title, self.list_first_name):
#                     logging.info('\n spider: name:{}; url:{} \n'.format(
#                             n_title, n_url))
#                     n_u = URL(n_url)
#                     n_n_items = n_u.url_items
#                     probability, content = Content.compare_content(
#                         c_u.text, n_u.text)
#                     if probability > 0.005:
#                         content = content
#                     else:
#                         content = Content(n_u.text).content
#                     data = dict(
#                         content=content,
#                         university=self.university,
#                         department=self.department,
#                         url=n_url,
#                         teacher=n_title,
#                     )
#                     self.data_q.put(data)
#                     for n_n_url, n_n_title in n_n_items:
#                         self.url_q.put(n_n_url)
#                     time.sleep(self.set_crawl_speed().get(self.slowdown, 0))
#                 else:
#                     logging.info('\n filter: {}; length: {}; url: {} \n'.format(
#                         n_title, len(n_title), n_url
#                     ))
#                     self.url_q.put(n_url)
#                 self.spided_urls.add(c_url)
#             deep += 1
#         self.data_q.put(None)
# 
#     def set_crawl_speed(self):
#         r = {
#             'None': 0,
#             '1': 1,
#             '2': 2,
#             '5': 5,
#             '10': 10,
#         }
#         return r
# 
#     def run(slef):
#         self.spider()
# 
# class Crawler:
# 
#     def __init__(self):
#         self.c_list = []
# 
#     def crawle(self, Spider, *args, **kwargs):
#         self.c_list.append(Spider(*args, **kwargs))
# 
#     def start(self):
#         for Spider in self.c_list:
#             Spider.run()
