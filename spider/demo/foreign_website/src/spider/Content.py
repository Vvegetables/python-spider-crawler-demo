#coding=utf-8
import os
import re
import difflib
from goose import Goose
import urlparse


class Scontent:
    
    goose = None
    
#     def __init__(self):
#         pass
    
    @classmethod
    def get_instance(cls):
        if not cls.goose:
            cls.goose = Goose()
        return cls.goose
    @classmethod
    def get_result(cls,url,raw_html=None):
        article = cls.get_instance().extract(url=url,raw_html=raw_html)
        return {'content':article.cleaned_text.encode('utf-8'),'title':article.title.encode('utf-8')}
    @staticmethod
    def check_url(base_url,cmp_url):
        url_p = urlparse.urlparse(base_url)
        netloc = url_p.netloc
        path = url_p.path
        scheme = url_p.scheme
        _base = scheme + '://' + netloc
        if _base in cmp_url:
            return True
        else:
            return False
        

class Content:

    def __init__(self, text):
        self.text = text
        self.content = self.process_content()

    def delete_html_tags(self):
        text = self.text
        delete_symbol = [
            '&nbsp;',
            '&#160;',
            '#',
            '&',
            '*',
        ]
        for i in delete_symbol:
            if i in text:
                text = text.replace(i, '')
        delete_tags = [
            '<!--(.*?)-->',
            '<script[^>]*?>[\\s\\S]*?<\\/script>',
            '<style[^>]*?>[\\s\\S]*?<\\/style>',
            '<p/[^>]*?>\s*?<p/>',
            '<[^>]+>',
        ]
        for i in delete_tags:
            text = re.sub(i, '', text)
        return_sign = [
            ' ',
            '\t',
        ]
        for i in return_sign:
            text = text.replace(i, '\n')
        text = (i for i in text.split('\n') if i != '')
        return text

    def process_content(self):
        _d = {}
        n = 0
        text = self.delete_html_tags()
        content_sign = [
            ',',
            '.',
            '!',
            '"',
#             '"',
            '(',
            ')',
            ';',
#             '.',
            '-',
        ]
        for i in text: #对回车换行进行处理
            if i != '\r':
                for _ in content_sign:
                    if _ in i:
                        _d[n] = _d.get(n, '') + '\n' + i
                        break
            elif i == '\r':
                n += 1
        max_content = 0
        content = ''
        for i in _d.values():  #返回字最多的
            if len(i) > max_content:
                max_content = len(i)
                content = i
        return content

    @classmethod
    def compare_content(cls, f_text, n_text):
        f = cls(f_text)
        f_text_without_tags = list(f.delete_html_tags())
        n = cls(n_text)
        n_text_without_tags = list(n.delete_html_tags())
        dif = difflib.Differ().compare(
            f_text_without_tags, n_text_without_tags
        )
        dif = list(dif)
        content = ''
        n = 0
        for i in dif:
            l = i.split(' ')
            if l[0] == '':
                n += 1
            elif l[0] == '+':
                content += l[1] + '\n'
        probability = n / len(dif)
        return probability, content

    @staticmethod
    def verify_name(name, list_first_name):
        with open('Data/stop_word.txt', 'r') as f2:
            list_stop_word = f2.readlines()
            list_stop_word = [
                s_i.replace('\n', '') for s_i in list_stop_word if s_i != ''
            ]
        if not list_first_name and not list_stop_word:
            return len(name) >= 2 and len(name) <= 3
        for i in list_stop_word:
            if i in name:
                return False
        b_name = False
        for i in list_first_name:
            if name.startswith(i):
                b_name = True
                break
        return len(name) >= 2 and len(name) <= 3 and b_name
