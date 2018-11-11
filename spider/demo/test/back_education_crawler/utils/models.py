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
from sqlalchemy import and_
import pymysql
pymysql.install_as_MySQLdb()

LOGIN = dict(
    username = 'ct',
    password = 'IhadKD#4321',
    dbname = 'innerweb',
    host = '47.96.253.99',
    port = '3306'
)


engine = create_engine('mysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(**LOGIN))

Base = declarative_base()

class EducationNews(Base): #User.__table__�鿴��Ϣ
    __tablename__ = 'sp_educationnews'
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
    
    
class ForeignEduNews(Base): #User.__table__
    __tablename__ = 'sp_foreignedunews'
    id = Column('id',Integer,primary_key=True)
    title = Column('title',String(length=1000))
    link = Column('link',String(length=1000))
    content = Column('content',Text())
    source = Column('source',String(length=500))
    
    createtime = Column('createtime',DateTime)
    modifytime = Column('modifytime',DateTime)
    number = Column('number',String(length=1000))
    
    
class ConfigTable(Base):
    __tablename__ = "sp_configtable"
    id = Column('id',Integer,primary_key=True)
    title = Column('title',String(length=1000))
    link = Column('link',String(length=1000))
    subtitle = Column('subtitle',String(length=1000))
    type = Column('type',Integer)
    visited = Column('visited',Integer)
    createtime = Column('createtime',DateTime)
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
 
    def __init__(self, engine=engine,_model=EducationNews):
        self._session = sessionmaker(bind=engine)
        self._s  = self._session()
        self._model = _model
    
    def commit(self):
        
        self._s.commit()
       
    def get_all_spidered_urls(self):
        myset = set(self._s.query(self._model.link).all())
        return myset
    
    
    def __enter__(self):
        return self._s
 
    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            self._s.commit()
        except:
            self._s.close()
            del self
            
            
def db_get_urls(_type):
    _session = sessionmaker(bind=engine)
    _s = _session()
    links = _s.query(ConfigTable.link).filter(and_(ConfigTable.type == _type , ConfigTable.visited == 0)).all()
    links = [x[0] for x in links]
    return links

def db_get_titles(_type):
    _session = sessionmaker(bind=engine)
    _s = _session()
    titles = _s.query(ConfigTable.title).filter(and_(ConfigTable.type == _type,ConfigTable.visited == 0)).all()
    subtitles = _s.query(ConfigTable.subtitle).filter(and_(ConfigTable.type == _type,ConfigTable.visited == 0)).all()
    return [x[0] for x in titles],[x[0] for x in subtitles]
    

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