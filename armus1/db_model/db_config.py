# coding=utf-8

from sqlalchemy import create_engine, Column, String, DATETIME, DATE, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import redis
import pymysql
pymysql.install_as_MySQLdb()
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:Tr120156317@localhost:3306/notice_information')
# engine=create_engine('sqlite:///universitys.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

Base = declarative_base()

class Notification(Base):

    """the class map to table of crystal.notifications"""

    __tablename__ = 'notifications'

    url = Column(String(100), primary_key=True)      #通知全文的url
    title = Column(Text)                      #讲座题目
    college = Column(String(100))                    #讲座所在大学
    speaker = Column(String(150))                    #讲座演讲人
    venue = Column(String(100))                      #讲座地点
    time = Column(String(50))                     #讲座时间
    notify_time = Column(String(50))

class Seed(Base):

    """the class map to table of crystal.seeds"""
    __tablename__ = 'seeds'

    start_url = Column(String(100), primary_key=True)    #待爬取学校学院的学术通知网址
    college = Column(String(100))                        #待爬取学校学院的名称
    url_xpath = Column(String(100))                      #总的通知网页下，每个通知的超链接的xpath选择路径
    nextpage_xpath=Column(String(100))                   #总的通知网页下，下一页标签的xpath选择路径
    title_word = Column(String(100))                     #选取有关我们需要的通知的关键词
    notice_time_xpath=Column(String(150))                #通知时间的xpath选择器规则
    title= Column(String(100))                           #通知标题匹配格式
    speaker = Column(String(100))                        #讲座演讲人匹配格式
    venue = Column(String(100))                          #讲座地点匹配格式
    time = Column(String(300))                           #讲座时间匹配格式
    text_xpath = Column(String(100))                     #具体通知页面下，爬取通知正文的xpath选择器规则

Base.metadata.create_all(engine)
