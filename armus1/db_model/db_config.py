# coding=utf-8

from sqlalchemy import create_engine, Column, String, DATETIME, DATE, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import redis
import pymysql
pymysql.install_as_MySQLdb()
# 初始化数据库连接:
# engine = create_engine('mysql+pymysql://root:Tr120156317@localhost:3306/notice_information')
engine=create_engine('sqlite:///universitys.db')
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
    time = Column(DATETIME)                     #讲座时间
    notify_time = Column(DATE)

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

#设置seed表的默认数据
    def set_init_data(self,db):
        #默认需要爬取的5个学校的配置信息
        scut_se=Seed(start_url='http://www2.scut.edu.cn/sse/xshd/list.htm',college='华南理工大学软件学院',
                 url_xpath='.//*[@class="news_ul"]//li',
                nextpage_xpath='//*[@id="wp_paging_w67"]/ul/li[2]/a[3]',
                title_word='举办,举行',
                 notice_time_xpath='//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div/div/div/p/span[1]',
                title='汇报主题:,报告题目:,题目:,Title:,报告主题:',speaker='汇报人:,报告人:,Speaker',
                 venue='地点:,venue:,Address:',time='Time:,时间:',
                 text_xpath='//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div//p')
        jnu_xx=Seed(start_url='https://xxxy2016.jnu.edu.cn/Category_37/Index.aspx',
          college='暨南大学信息科学技术学院/网络空间安全学院',
          url_xpath='//*[@id="mainContent"]/div[2]/ul//li',
          nextpage_xpath='//*[@id="pe100_page_通用信息列表_普通式"]/div/a[9]',
          title_word='学术讲座',
          notice_time_xpath='//*[@id="mainContent"]/div[2]/div/div[1]/span[3]',
          title='题目',
          speaker='报告人:',
          venue='地点:',
          time='时间:',
          text_xpath='//*[@id="fontzoom"]//p')

        scau_info=Seed(start_url= 'https://info.scau.edu.cn/3762/list.htm',
                  college= '华南农业大学数学信息学院/软件学院',
                  url_xpath= '//*[@id="container"]/div[2]/div/div//tbody//tr',
                  nextpage_xpath= '//*[@id="wp_paging_w05"]/ul/li[2]/a[3]',
                  title_word= '学术报告:',
                  notice_time_xpath= '//*[@id="new-meta"]/span[2]',
                  title= '报告题目:,学术报告:,题目',
                  speaker= '报告人:,主讲人:',
                  venue= '地点:',
                  time= '时间:',
                  text_xpath= '//div[2]/div[2]/div/div[2]/div/div//p')

    # 特殊处理 ----->>清华大学交叉信息研究院
        thu_iiis=Seed(start_url= 'https://iiis.tsinghua.edu.cn/zh/seminars/',
                     college= '清华大学交叉信息研究院',
                     url_xpath= './/tbody//tr',
                     nextpage_xpath= '//ul[@class="pagination"]/li[last()-1]/a',
                     title_word= '',
                     notice_time_xpath= '',
                     title='标题:,Title:',
                     speaker= '演讲人:,Speaker',
                     venue= '地点:,venue',
                     time= '时间:,Time:',
                     text_xpath= '//div[6]/div/div/div[2]/div/div/div/p')

        sklois=Seed(start_url= 'http://sklois.iie.cas.cn/tzgg/tzgg_16520/',
                     college= '信息安全国家重点实验室',
                     url_xpath= '//table[@width="665"]//tr',
                     nextpage_xpath= '//*[contains(text(),"下一页")]',
                     title_word= '学术报告,学术讲座',
                     notice_time_xpath= '//*[@id="new-meta"]/span[2]',
                     title= '报告题目,学术报告,题目,Title:',
                     speaker= '报告人:,Speaker:',
                     venue= '地点:,Place:',
                     time= '时间:,Time,Address:',
                     text_xpath= '//td[@class="nrhei"]//p')
        db.add_all([scut_se,jnu_xx,scau_info,thu_iiis,sklois])
        db.commit()


    # def insert_data(self):
    #
Base.metadata.create_all(engine)

