
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

process=CrawlerProcess(get_project_settings())

db=DBSession()
# scut_se=Seed(start_url='http://www2.scut.edu.cn/sse/xshd/list.htm',college='华南理工大学软件学院',
#              url_xpath='.//*[@class="news_ul"]//li',
#             nextpage_xpath='//*[@id="wp_paging_w67"]/ul/li[2]/a[3]',
#             title_word='举办,举行',
#              notice_time_xpath='//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div/div/div/p/span[1]',
#             title='汇报主题:,报告题目:,题目:,Title:,报告主题:',speaker='汇报人:,报告人:,Speaker',
#              venue='地点:,venue:,Address:',time='Time:,时间:',
#              text_xpath='//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div//p')
#
# jnu_xx=Seed(start_url='https://xxxy2016.jnu.edu.cn/Category_37/Index.aspx',
#       college='暨南大学信息科学技术学院/网络空间安全学院',
#       url_xpath='//*[@id="mainContent"]/div[2]/ul//li',
#       nextpage_xpath='//*[@id="pe100_page_通用信息列表_普通式"]/div/a[9]',
#       title_word='学术讲座',
#       notice_time_xpath='//*[@id="mainContent"]/div[2]/div/div[1]/span[3]',
#       title='题目',
#       speaker='报告人:',
#       venue='地点:',
#       time='时间:',
#       text_xpath='//*[@id="fontzoom"]//p')
#
# scau_info=Seed(start_url= 'https://info.scau.edu.cn/3762/list.htm',
#               college= '华南农业大学数学信息学院/软件学院',
#               url_xpath= '//*[@id="container"]/div[2]/div/div//tbody//tr',
#               nextpage_xpath= '//*[@id="wp_paging_w05"]/ul/li[2]/a[3]',
#               title_word= '学术报告:',
#               notice_time_xpath= '//*[@id="new-meta"]/span[2]',
#               title= '报告题目:,学术报告:,题目',
#               speaker= '报告人:,主讲人:',
#               venue= '地点:',
#               time= '时间:',
#               text_xpath= '//div[2]/div[2]/div/div[2]/div/div//p')
#
# # 特殊处理 ----->>清华大学交叉信息研究院
# thu_iiis=Seed(start_url= 'https://iiis.tsinghua.edu.cn/zh/seminars/',
#                  college= '清华大学交叉信息研究院',
#                  url_xpath= './/tbody//tr',
#                  nextpage_xpath= '//ul[@class="pagination"]/li[last()-1]/a',
#                  title_word= '',
#                  notice_time_xpath= '',
#                  title='标题:,Title:',
#                  speaker= '演讲人:,Speaker',
#                  venue= '地点:,venue',
#                  time= '时间:,Time:',
#                  text_xpath= '//div[6]/div/div/div[2]/div/div/div/p')
#
# sklois=Seed(start_url= 'http://sklois.iie.cas.cn/tzgg/tzgg_16520/',
#                  college= '信息安全国家重点实验室',
#                  url_xpath= '//table[@width="665"]//tr',
#                  nextpage_xpath= '//*[contains(text(),"下一页")]',
#                  title_word= '学术报告,学术讲座',
#                  notice_time_xpath= '//*[@id="new-meta"]/span[2]',
#                  title= '报告题目,学术报告,题目,Title:',
#                  speaker= '报告人:,Speaker:',
#                  venue= '地点:,Place:',
#                  time= '时间:,Time,Address:',
#                  text_xpath= '//td[@class="nrhei"]//p')
# db.add_all([scut_se,jnu_xx,scau_info,thu_iiis,sklois])
# db.commit()
college_url=input('请输入需要爬取的学校的通知网址：')   #start_url
# seeds=db.query(Seed)      #爬取seed中全部学校的信息
# print(seeds)

seed=db.query(Seed).filter(Seed.start_url==college_url).all()     #爬取一个学校
print(seed)
# except Exception as e:
if len(seed)==0:
    college=str(input('请输入需要爬取的学校（学院）的名称：'))
    next_xpath=str(input('请输入通知网站下一页的xpath选择器路径：'))
    url_xpath=str(input('请输入通知网站下每个具体网站超链接的xpath路径：'))
    text_xpath=str(input('请输入具体通知页面下，爬取通知正文的xpath选择器规则：'))
    notice_time_xpath=str(input('请输入具体通知页面下，爬取通知时间的xpath选择器规则,默认为空：'))
    title_word=str(input('请输入学术讲座通知的匹配关键字：'))
    #上述四个内容必须输入！
    title = '报告题目:,学术报告:,题目,报告主题:,Title'
    speaker = '报告人:,主讲人:,汇报人:,Speaker'
    venue = '地点:,Address,Venue'
    time = '时间:,Time'
    uni=Seed(start_url= college_url,
                  college= college,
                 url_xpath= url_xpath,
                 nextpage_xpath= next_xpath,
                 title_word= title_word,
                 notice_time_xpath= notice_time_xpath,
                 title= title,
                 speaker= speaker,
                 venue= venue,
                 time= time,
                 text_xpath= text_xpath)
    db.add(uni)
    db.commit()
    seed=uni

#所有学校学术信息爬取
# for seed in seeds:
#     urlHandle=UrlHandle()
#     existed_urls=get_existed_urls(seed)
#     urlHandle.set_start_url(seed.start_url)
#     urlHandle.set_existed_urls(existed_urls)
#     urlHandle.set_next_xpath(seed.nextpage_xpath)
#     urlHandle.set_url_xpath(seed.url_xpath)
#     urls=urlHandle.get_filte_urls()
#     process.crawl(NoticeSpider,seed,urls)
#     print((urls))
#单个指定学校爬取

def get_existed_urls(seed):
    existed_urls = []
    try:
        print('ds')
        urls = db.query(Notification.url).filter(seed.college == Notification.college).all()
        # existed_urls=[]
        for url in urls:
            existed_urls.append(url[0])
        # return existed_urls
    except Exception as e:
        print('初始爬虫')
    finally:
        return existed_urls
def common_spider(seed):
    urlHandle=UrlHandle()
    existed_urls=get_existed_urls(seed)
    urlHandle.set_start_url(seed.start_url)
    urlHandle.set_title_word(seed.title_word)
    urlHandle.set_existed_urls(existed_urls)
    urlHandle.set_nextpage_xpath(seed.nextpage_xpath)
    urlHandle.set_url_xpath(seed.url_xpath)
    title_urls=urlHandle.get_filte_urls()
    print(title_urls,'dskjh')
    process.crawl(NoticeSpider,seed,title_urls)
    process.start()

if college_url=='https://iiis.tsinghua.edu.cn/zh/seminars/':
    process.crawl(ThuIiisSpider)
    process.start()

else:
    common_spider(seed[0])