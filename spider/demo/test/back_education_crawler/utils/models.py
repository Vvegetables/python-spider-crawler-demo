#coding=utf-8

'''
MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
  
pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
  
MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime,Text
from sqlalchemy.orm import sessionmaker

LOGIN = dict(
    username = 'hanyj',
    password = 'Ihad#kd1234',
    dbname = 'CrawlerDB',
    host = '192.168.2.212',
    port = '3306'
)


engine = create_engine('mysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(**LOGIN))

Base = declarative_base()

class EducationNews(Base): #User.__table__�鿴��Ϣ
    __tablename__ = 'educationnews'
    id = Column('id',Integer,primary_key=True)
    title = Column('title',String(length=1000))
    link = Column('link',String(length=1000))
    content = Column('content',Text())
    source = Column('source',String(length=500))
    
    createtime = Column('createtime',DateTime)
    modifytime = Column('modifytime',DateTime)
    number = Column('number',String(length=1000))
    
    def __repr__(self):
        return '{}'.format(self.id)

def create_table():

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine) #Session.configure(bind=engine)

    return Session()
    

def get_session():
    
    Session = sessionmaker(bind=engine) #Session.configure(bind=engine)

    return Session()
    
class Sql:
 
    def __init__(self, engine=engine):
        self._session = sessionmaker(bind=engine)
        self._s  = self._session()
    
    def commit(self):
        
        self._s.commit()
       
    def get_all_spidered_urls(self):
        myset = set(self._s.query(EducationNews.link).all())
        return myset
    
    
    def __enter__(self):
        return self._s
 
    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            self._s.commit()
        except:
            self._s.close()
            del self
#����
# ed_user = EducationNews(name='ed',fullname='ed jones',pas='pass')
# _session.add(ed_user)
# 
# 
# #��ѯ
# our_user = _session.query(EducationNews).filter_by(name='ed').first()
# 
# #�ύ�����ݿ�
# _session.commit()