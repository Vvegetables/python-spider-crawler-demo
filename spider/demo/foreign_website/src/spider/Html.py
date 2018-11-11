import requests
import re
from urlparse import urljoin
from lxml import etree
import chardet
import socket

class Request:

    def __init__(self, url, method='GET', timeout=5, *args, **kwargs):
        self.url = url
        self.response = self.process_url(url, method, timeout, *args, **kwargs)

    def process_url(self, url, method, timeout, *args, **kwargs):
        r = {
            'GET': requests.get,
            'POST': requests.post,
        }
        try:
            response = r.get(method)(url, timeout=timeout, *args, **kwargs)
            if 'Connection' in response.headers.keys():
                del response.headers['Connection']
        except socket.timeout:
            print 'timeout'
            response = self.err_response()
        except Exception,e:
            print 'dont know why,{}'.format(e.message)
            response = self.err_response()
        response = self.html_code(response)
        return response

    def err_response(self):
        class Response:
            text = ''
            error = True
            url = self.url

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


    @staticmethod
    def complete_url(host_url, url):
        return urljoin(host_url, url)

    @property
    def text(self):
        return self.response.text

    @property
    def html(self):
        if hasattr(self.response, 'error'):
            return None
        text = self.response.text.replace('?xml', 'head')
        return etree.HTML(text)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        del self

class URL:

    def __init__(self, start_url):
        self.start_url = start_url
        self.url_list = set()
        self.HTML = Request(self.start_url)

    def process_url(self, url):
        nu = urljoin(self.start_url, url)
        return nu

    @staticmethod
    def process_title(title):
        title = ''.join(filter(str.isalnum, title.encode('utf-8')))
        return ''.join(title)

    def url_list_add_items(self):
        html = self.HTML.html
        if html is None:
            return
        infos = html.xpath('//a')
        for info in infos:
            url = ''.join(info.xpath('@href'))
            n_u = self.process_url(url)
            title = info.xpath('string(.)')
#             title = self.process_title(title)
            self.url_list.add((n_u, title))

    @property
    def text(self):
        return self.HTML.text

    @property
    def url_items(self):
        self.url_list_add_items()
        return self.url_list

