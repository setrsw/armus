# coding=utf-8
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import datetime
from datetime import timedelta
# from sqlalchemy import Column, String, DATE, DATETIME, Text
# from sqlalchemy.ext.declarative import declarative_base
# import pymysql
# pymysql.install_as_MySQLdb()
from db_model.db_config import DBSession

Base = declarative_base()
engine=create_engine('sqlite:///universitys.db')

class Notification(Base):

    """the class map to table of db_model.notifications"""

    __tablename__ = 'notifications'

    url = Column(String(255), primary_key=True)      #通知全文的url
    title = Column(String(255))                      #讲座题目
    college = Column(String(255))                    #讲座所在大学
    speaker = Column(String(255))                    #讲座演讲人
    venue = Column(String(255))                      #讲座地点
    time = Column(String(255))                     #讲座时间
    notify_time = Column(String(20))                  #通知发布时间

    # def __init__(self):
    #     self.session = DBSession()
    #     Base.metadata.create_all(engine)
    #     self.info_byrelease=[] #按照通知时间
    #     self.info_bytime=[]    #按照讲座时间

    def delete(self):  # 进行筛选操作，选出标题中含有密码学和信息安全的数据，清空表格，再插入选中的数据
        # session = DBSession()
        self.session = DBSession()
        temp = self.session.query(Notification).filter(
            or_(Notification.title.like("%密码学%"), Notification.title.like("%信息安全%"))).all()
        temp_Eng = self.session.query(Notification).filter(
            or_(Notification.title.like("%security%"), Notification.title.like("%password%"))).all()

        self.session.query(Notification).delete()
        self.session.commit()

        for t in temp:
            t_dict = t.__dict__
            try:
                frank = Notification(url=t_dict['url'],title=t_dict['title'], speaker=t_dict['speaker'],
                                 time=t_dict['time'],venue=t_dict['venue'], college=t_dict['college'],
                                 notify_time=t_dict['notify_time'])
                self.session.add(frank)
                self.session.commit()
            except:
                self.session.rollback()
                pass
        for t in temp_Eng:
            t_dict = t.__dict__
            try:
                frank = Notification(title=t_dict['title'], speaker=t_dict['speaker'], time=t_dict['time'],
                                     venue=t_dict['venue'], college=t_dict['college'], url=t_dict['url'],
                                     notify_time=t_dict['notify_time'])
                self.session.add(frank)
                self.session.commit()
            except:
                self.session.rollback()
                pass

    def orderbyrelease(self):  # 按照发布时间排序，并且只选中近一年的数据
        # session = DBSession()
        self.session = DBSession()
        self.info_byrelease=[]
        temp = self.session.query(Notification).filter(
            Notification.notify_time >= datetime.datetime.now() - timedelta(days=365)).order_by(
            desc(Notification.notify_time)).all()
        print("按照通知发布时间由近及远排序：")
        for t in temp:
            t_dict = t.__dict__
            info={'title':t_dict['title'],'speaker':t_dict['speaker'],'time':t_dict['time'],
                  'venue':t_dict['venue'],'college':t_dict['college'],'url':t_dict['url']}
            self.info_byrelease.append(info)
        print(self.info_byrelease)
            # print("讲座标题:", t_dict['title'])
            # print("报告人:", t_dict['speaker'])
            # print("时间:", t_dict['time'])
            # print("地点:", t_dict['venue'])
            # print("大学:", t_dict['college'])
            # print("通知全文链接:", t_dict['url'])
            # print()


    def orderbytime(self):  # 按照举行时间排序，并且只选中近一年的数据
        self.session = DBSession()
        self.info_bytime=[]
        temp = self.session.query(Notification).filter(
            Notification.notify_time >= datetime.datetime.now() - timedelta(days=365)).order_by(
            desc(Notification.time)).all()
        print("按照报告举行时间由近及远排序：")
        for t in temp:
            t_dict = t.__dict__
            info = {'title': t_dict['title'], 'speaker': t_dict['speaker'], 'time': t_dict['time'],
                    'venue': t_dict['venue'], 'college': t_dict['college'], 'url': t_dict['url']}
            self.info_bytime.append(info)
        # print(self.info_bytime)
            # print("讲座标题:", t_dict['title'])
            # print("报告人:", t_dict['speaker'])
            # print("时间:", t_dict['time'])
            # print("地点:", t_dict['venue'])
            # print("大学:", t_dict['college'])
            # print("通知全文链接:", t_dict['url'])
            # print()
    def get_info_bytime(self):
        return self.info_bytime

    def get_info_byrelease(self):
        return self.info_byrelease

Base.metadata.create_all(engine)