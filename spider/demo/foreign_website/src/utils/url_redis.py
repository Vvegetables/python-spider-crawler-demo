#coding=utf-8
import redis

class UrlRedis:
    redis_conn = None
    # used_urls = None
    last_url = None
    
    @classmethod
    def _connect(cls):
        if not cls.redis_conn:
            cls.redis_conn = redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)
        return cls.redis_conn
    @classmethod
    def add_url(cls,param):
        cls._connect()

        # if not cls.redis_conn.exists('last'):
        #     cls.redis_conn.set('last',param)

        if not cls.redis_conn.hexists('used',param):
            cls.redis_conn.hset('used',param,param)
            cls.redis_conn.set('last',param)
            return False
        else:
            if param == cls.redis_conn.get('last'):
                return False
        return True

        
        