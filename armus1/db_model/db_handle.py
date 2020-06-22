from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import datetime
from datetime import timedelta

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/notice_information')
#=create_engine('sqlite:///universitys.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

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


def delete():#进行筛选操作，选出标题中含有密码学和信息安全的数据，清空表格，再插入选中的数据
    session = DBSession()
    
    temp = session.query(Notification).filter(or_(Notification.title.like("%密码学%"),Notification.title.like("%信息安全%"))).all()   
    temp_Eng = session.query(Notification).filter(or_(Notification.title.like("%security%"),Notification.title.like("%password%"))).all()
    
    session.query(Notification).delete()
    session.commit()    
    
    for t in temp:
        t_dict = t.__dict__
        frank = Notification(title = t_dict['title'], speaker = t_dict['speaker'], time = t_dict['time'], venue = t_dict['venue'], college = t_dict['college'], url = t_dict['url'], notify_time = t_dict['notify_time'])
        session.add(frank)
        session.commit()    
    for t in temp_Eng:
        t_dict = t.__dict__
        frank = Notification(title = t_dict['title'], speaker = t_dict['speaker'], time = t_dict['time'], venue = t_dict['venue'], college = t_dict['college'], url = t_dict['url'], notify_time = t_dict['notify_time'])
        session.add(frank)
        session.commit()        
    
def orderbyrelease():#按照发布时间排序，并且只选中近一年的数据
    session = DBSession()
    temp = session.query(Notification).filter(Notification.notify_time >= datetime.datetime.now() - timedelta(days=365)).order_by(desc(Notification.notify_time)).all()
    print("按照通知发布时间由近及远排序：")
    for t in temp:
        t_dict = t.__dict__
        print("讲座标题:",t_dict['title'])
        print("报告人:",t_dict['speaker'])
        print("时间:",t_dict['time'])
        print("地点:",t_dict['venue'])
        print("大学:",t_dict['college'])
        print("通知全文链接:",t_dict['url'])
        print()

def orderbytime():#按照举行时间排序，并且只选中近一年的数据
    session = DBSession()
    temp = session.query(Notification).filter(Notification.notify_time >= datetime.datetime.now() - timedelta(days=365)).order_by(desc(Notification.time)).all()
    print("按照报告举行时间由近及远排序：")
    for t in temp:
        t_dict = t.__dict__
        print("讲座标题:",t_dict['title'])
        print("报告人:",t_dict['speaker'])
        print("时间:",t_dict['time'])
        print("地点:",t_dict['venue'])
        print("大学:",t_dict['college'])
        print("通知全文链接:",t_dict['url'])
        print()

delete()
orderbytime()