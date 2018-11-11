#coding=utf-8
# import fcntl
from functools import wraps
import logging
from flask import(
    request,
    session,
    redirect,
    url_for,
    jsonify,
)
def debug(func):
    def f(*args, **kwargs):
        func(*args, **kwargs)
        input()
    return f

@debug
def log(*args):
    m = logging.info(*args)
    return m

def write_stop_word(word):
    with open('Data/stop_word.txt', 'a') as f:
#         fcntl.flock(f, fcntl.LOCK_EX)
        f.write(word + '\n')
#         fcntl.flock(f, fcntl.LOCK_UN)

def delete_trash_word(name):
    tra_word_list = [
        '副教授',
        '教授',
        '讲师',
        '研究员',
        '院士',
    ]
    for i in tra_word_list:
        name = name.replace(i, '')
    return name

def login_required(func):
    @wraps(func)
    def f(*args, **kwargs):
        u_id = session.get('user_id', -1)
        if u_id == 1:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'you should login'})
    return f

def get_list_first_name(first_name_file):
    with open(first_name_file, 'r') as f1:
        list_first_name = f1.readlines()
        list_first_name = [
            s_i.replace('\n', '') for s_i in list_first_name if s_i != ''
        ]
    return list_first_name
