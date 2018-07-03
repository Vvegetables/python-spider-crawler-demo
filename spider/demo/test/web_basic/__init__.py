#coding=utf-8
import datetime
import re
import time
import urllib2
import urlparse


#下载限速
class Throttle:
    '''
    Add a delay between downloads to the same domain
    '''
    def __init__(self,delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        self.domains = {}
        
    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get()
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
            self.domains[domain] = datetime.datetime.now()

#具备存储已发现URL的功能可以避免重复下载


#爬虫陷阱
# def link_crawler():
# 避免陷入爬虫陷阱，一个简单的方法是记录一个深度值，当到达最大深度时，爬虫就不再向队列中添加该网页中的链接了。

#下载网页的函数
def download(url,user_agent='wswp',proxy=None,num_retries=2):
    print 'download:',url
    #用户
    headers = {'User-agent':user_agent}
    
    try:
        request = urllib2.Request(url,headers=headers)
        opener = urllib2.build_opener()
        #代理
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme:proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
#         html = urllib2.urlopen(url).read()
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        #有疑问
        print 'Download error:',e
        
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                return download(url,user_agent,proxy,num_retries-1)
        
        return html
    

def crawl_sitemap(url):
    
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html = download(link)
        
    
    


if __name__ == '__main__':
    url = 'http://www.meetup.com/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    html = download(url,user_agent)
    print html