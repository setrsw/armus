
#数据库
# from db_model.seeds import Seed
from db_model.db_config import DBSession
# from db_model.notifications import Notification
from db_model.db_config import Seed
from db_model.db_config import Notification
from UrlHandle import UrlHandle

from armus1.spiders.notice import NoticeSpider
from armus1.spiders.thu_iiis import ThuIiisSpider
# scrapy api
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class Data_Spider:
    def __init__(self):
        self.process=CrawlerProcess(get_project_settings())
        self.db=DBSession()
        self.init_seed_data()
        #设置默认值
        # self.title_word=str(input('请输入学术讲座通知的匹配关键字：'))
        self.title = '报告题目:,学术报告:,题目,报告主题:,Title'        #(默认值)
        self.speaker = '报告人:,主讲人:,汇报人:,Speaker,报告专家'
        self.venue = '地点:,Address,Venue,Place'
        self.time = '日期:,时间:,Time'

    # 初始化seed表格数据
    def init_seed_data(self):
        init=self.db.query(Seed).all()
        if len(init)==0:
            init_data=Seed()
            init_data.set_init_data(self.db)

    def set_college_url(self,college_url):
        # self.college_url=input('请输入需要爬取的学校的通知网址：')   #start_url
        self.college_url =college_url
    def set_college(self,college):
        self.college=college

    def set_next_xpath(self,next_xpath):
        self.next_xpath=next_xpath

    def set_url_xpath(self,url_xpath):
        self.url_xpath=url_xpath

    def set_text_xpath(self,text_xpath):
        self.text_xpath=text_xpath

    #多个关键词用","隔开
    def set_title_word(self,title_word):
        self.title_word=title_word

    def set_notify_time_xpath(self,notify_time_xpath):
        if len(notify_time_xpath)>0:
            self.notify_time_xpath=notify_time_xpath
        else:
            self.notify_time_xpath=''

    def set_title(self,title):
        if len(title)>0:
            self.title=self.title+','+title
        self.title=self.title.replace('，',',')
    def set_speaker(self,speaker):
        if len(speaker)>0:
            self.speaker=self.speaker+','+speaker
        self.speaker=self.speaker.replace('，',',')
    def set_venue(self,venue):
        if len(venue)>0:
            self.venue=self.venue+','+venue
        self.venue = self.venue.replace('，', ',')
    def set_time(self,time):
        if len(time)>0:
            self.time=self.time+','+time
        self.time = self.time.replace('，', ',')

    def insert_seed(self,college_url):
        # college_url=str(input('请输入需要爬取的学校的通知网址：'))
        self.set_college_url(college_url)
        college = str(input('请输入需要爬取的学校（学院）的名称：'))
        self.set_college(college)
        next_xpath=str(input('请输入通知网站下一页的xpath选择器路径：'))
        self.set_next_xpath(next_xpath)
        url_xpath=str(input('请输入通知网站下每个具体网站超链接的xpath路径：'))
        self.set_url_xpath(url_xpath)
        text_xpath=str(input('请输入具体通知页面下，爬取通知正文每行文字的xpath路径：'))
        self.set_text_xpath(text_xpath)
        notify_time_xpath=str(input('请输入具体通知页面下，爬取通知时间的xpath路径,默认为空(不存在就不必输入)：'))
        self.set_notify_time_xpath(notify_time_xpath)
        #上述五条信息必须输入，下面的信息可以选择性输入
        title_word=str(input('请输入总通知页面下通知标题的字符匹配规则：（可选择不输入）'))
        self.title_word=title_word
        title=str(input('请输入报告标题的字符匹配规则：（可选择不输入）'))
        self.set_title(title)
        speaker = str(input('请输入报告人的字符匹配规则：（可选择不输入）'))
        self.set_speaker(speaker)
        venue = str(input('请输入报告地点的字符匹配规则：（可选择不输入）'))
        self.set_venue(venue)
        time = str(input('请输入报告时间的字符匹配规则：（可选择不输入）'))
        self.set_time(time)
        seed=Seed(start_url= self.college_url,college= self.college,url_xpath= self.url_xpath,
                     nextpage_xpath= self.next_xpath,title_word= self.title_word,notice_time_xpath= self.notify_time_xpath,
                     title= self.title,speaker= self.speaker,venue= self.venue,time= self.time,text_xpath= self.text_xpath)
        self.db.add(seed)
        self.db.commit()
        return seed

    #单个指定学校爬取
    def get_existed_urls(self,seed):
        existed_urls = []
        urls = self.db.query(Notification.url).filter(seed.college == Notification.college).all()
        # existed_urls=[]
        if len(urls)>0:
            for url in urls:
                existed_urls.append(url[0])
        return existed_urls

    #爬取学校学术信息通用流程
    def common_spider(self,seed):
        urlHandle=UrlHandle()
        existed_urls=self.get_existed_urls(seed)
        urlHandle.set_start_url(seed.start_url)
        urlHandle.set_title_word(seed.title_word)
        urlHandle.set_existed_urls(existed_urls)
        urlHandle.set_nextpage_xpath(seed.nextpage_xpath)
        urlHandle.set_url_xpath(seed.url_xpath)
        title_urls=urlHandle.get_filte_urls()
        self.process.crawl(NoticeSpider,seed,title_urls)
        self.process.start()

    #单个学校学术信息爬取
    def university_spider(self,seed):
        # college_url=self.set_college_url()
        # seed = self.db.query(Seed).filter(Seed.start_url == college_url).one()
        if seed.start_url=='https://iiis.tsinghua.edu.cn/zh/seminars/':    #清华大学
            self.process.crawl(ThuIiisSpider)
            self.process.start()
        else:
            self.common_spider(seed)

    # 所有学校学术信息爬取，一次性爬取所有学校会出错
    def universities_spider(self):
        seeds=self.db.query(Seed).all()
        for seed in seeds:
            #对于每个学校直接调用单个学校爬取函数
            self.university_spider(seed)

    def start_spider(self):
        is_one_spider=str(input('爬取一个学校学术信息(y),多个学校学术信息（n）？y/n'))
        while True:
            print(is_one_spider)
            if is_one_spider in ['y','Y','yes','Yes']:
                college_url = str(input('请输入需要爬取的学校的通知网址：'))
                seed = self.db.query(Seed).filter(Seed.start_url == college_url).all()
                if len(seed)==0:
                    seed=self.insert_seed(college_url)
                    self.university_spider(seed)
                else:
                    self.university_spider(seed[0])
                is_continue=str(input(('爬取完成，是否继续？y/n')))
                if is_continue in ['y','Y','yes','Yes']:
                    is_one_spider = str(input('爬取一个学校学术信息(y),多个学校学术信息（n）？y/n'))
                else:
                    break
            elif is_one_spider in ['n','no','No','N']:
                self.universities_spider()
                print('所有信息爬取完成！')
                break
            else:
                print('你的输入错误，请重新输入：')
                is_one_spider=str(input('爬取一个学校学术信息(y),多个学校学术信息（n）？y/n'))

#放在主程序执行
spider=Data_Spider()
spider.start_spider()

#请输入需要爬取的学校的通知网址：http://sist.swjtu.edu.cn/list.do?action=news&navId=40
# 请输入需要爬取的学校（学院）的名称：西南交通大学信息科学与技术学院
# 请输入通知网站下一页的xpath选择器路径：//div[@class="tableFootLeft"]//a[text()="下一页"]
# 请输入通知网站下每个具体网站超链接的xpath路径：//*[@id="rightPageContent"]/dl//dd
# 请输入具体通知页面下，爬取通知正文每行文字的xpath路径：//*[@id="newsBody"]//p
# 请输入具体通知页面下，爬取通知时间的xpath路径,默认为空(不存在就不必输入)：//*[@id="newsInfo"]