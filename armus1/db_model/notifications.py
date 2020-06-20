# coding=utf-8
from sqlalchemy import Column, String, DATE, DATETIME, Text
from sqlalchemy.ext.declarative import declarative_base
import pymysql
pymysql.install_as_MySQLdb()
Base = declarative_base()

class Notification(Base):

    """the class map to table of crystal.notifications"""

    __tablename__ = 'notifications'

    url = Column(String, primary_key=True)      #通知全文的url
    title = Column(String(100))                      #讲座题目
    college = Column(String)                    #讲座所在大学
    speaker = Column(String)                    #讲座演讲人
    venue = Column(String)                      #讲座地点
    time = Column(DATETIME)                     #讲座时间
    notify_time = Column(DATE)                  #通知发布时间
