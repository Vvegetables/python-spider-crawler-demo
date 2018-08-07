#coding=utf-8
import json
import os

from lxml import etree
import requests
import chardet
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

_url = 'http://www.sninfo.gov.cn:8083/initSnFirstPageList.do?method=initSnFirstPageList'

try:
    response = requests.get(url=_url,headers=headers,timeout=10)
except Exception,e:
    print e

print 'status_code:',response.status_code
html = etree.HTML(response.text)
print response.encoding
infos = html.xpath('//a')
paths = {}
for info in infos:
    key = info.xpath('string(.)').strip()
    value = ''.join(info.xpath('@href'))
#     if not isinstance(key,unicode):
#         detect_res = chardet.detect(key)
    if key and not isinstance(key,unicode):
        print 'chardetect:',chardet.detect(key)
 
    p = re.compile('\s+') 
    key = re.sub(p,'',key)
    value = re.sub(p,'',value)
    paths[key] = value
    print key,paths[key]

# with open('testlog.txt','a') as f:
#     data = json.dumps(paths,ensure_ascii=False).decode('utf8').encode('gb2312')
#     f.write(data)
#     f.write(os.linesep)

# print paths