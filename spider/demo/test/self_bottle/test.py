#coding=utf-8
# from __future__ import unicode_literals


from datetime import datetime
import json
import os

 
with open('error.log','a') as f:
    _error_dict = {}#.update(_data)
    _error_dict['level'] = 'error'
    _error_dict['time'] = str(datetime.now())
    _error_dict['reason'] = '数据库插入'
    json_data = json.dumps(_error_dict,ensure_ascii=False).decode('utf8').encode('gb2312') #达到写中文的目的
#     json_data = json_data.encode('gbk')
#     print json_data 
    f.write(json_data)
     
    f.write(os.linesep)

#文件中写中文
# with open('chinese.txt','ab') as c:
#     c.write('中国'.encode('gbk'))