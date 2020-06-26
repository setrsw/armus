# -*- coding: utf-8 -*-

#清华大学交互信息学院
import re
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from armus1.items import Armus_Item
# from db_model.db_config import Notification
from db_model.notifications import Notification
from db_model.db_config import DBSession

class ThuIiisSpider(CrawlSpider):
    name = 'thu_iiis'
    allowed_domains = ['iiis.tsinghua.edu.cn']
    start_urls = ['https://iiis.tsinghua.edu.cn/list-265-1.html']
    domain_url='https://iiis.tsinghua.edu.cn'
    # custom_settings = {
    #     'ITEM_PIPELINES': {'armus1.pipelines.ArmusPipeline': 300}
    # }

    rules = (
        Rule(LinkExtractor(allow=r'https://iiis.tsinghua.edu.cn/list-265-\d{1,2}.html'), callback='parse_item', follow=None),
        # Rule(LinkExtractor(restrict_xpaths='.//ul[@class="pagination"]/li[last()-1]/a'),callback=None,follow=True)
    )
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.college='清华大学交叉信息研究院'
        self.db=DBSession()
    def parse_item(self, response):

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        reports=response.xpath('.//tbody//tr')
        for report in reports:
            notice_url = self.domain_url + report.xpath('./td/a/@href').get()
            if self.is_existed_urls(notice_url):
                continue
            else:
                notify_time=''
                title=report.xpath('./td/a/text()').getall()
                title = ' '.join(''.join(title).split())
                # print(notice_url)
                speaker=report.xpath('./td[2]//text()').getall()
                speaker=' '.join(''.join(speaker).split())
                time=report.xpath('./td[3]//text()').get()
                # time=self.format_time(time,notify_time)
                venue=report.xpath('./td[4]//text()').get()
                item=Armus_Item(title=title,speaker=speaker,venue=venue,
                              time=time,url=notice_url,college=self.college,notify_time=notify_time)
                yield item
        next_page = response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_item)

    def is_existed_urls(self,notice_url):
        url = self.db.query(Notification.url).filter(notice_url == Notification.college).all()
        # existed_urls=[]
        if len(url):
            return True
        else:
            return False

    def format_time(self,time,notify_time):
        #匹配****年**月**日(下午)HH:MM
        if re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+).+(\d+)', time):
            st=re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+).+(\d+)', time)
            y = st.group(1)
            mon = st.group(2)
            d = st.group(3)
            if len(y) == 2:
                y = '20' + y
            if len(mon) == 1:
                mon = '0' + mon
            if len(d) == 1:
                d = '0' + d
            h = st.group(4)
            if re.search(r'.*?(\d{4}).(\d+).(\d+)..*?下午(\d+).+(\d+)', time):
                h=str(int(h)+12)
            min = st.group(5)
            if len(h) == 1:
                h = '0' + h
            if len(min) == 1:
                min = '0' + min
        # 匹配****年**月**日(下午)HH
        elif re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+)', time):
            st=re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+)', time)
            y = st.group(1)
            mon = st.group(2)
            d = st.group(3)
            if len(y) == 2:
                y = '20' + y
            if len(mon) == 1:
                mon = '0' + mon
            if len(d) == 1:
                d = '0' + d
            h = st.group(4)
            if re.search(r'.*?(\d{4}).(\d+).(\d+)..*?下午(\d+).', time):

                h=str(int(h)+12)
            if len(h) == 1:
                h = '0' + h
            min='00'
        # 匹配**月**日(下午)HH:MM
        elif re.search(r'.*?(\d{1,2}).(\d+)..*?(\d+).+(\d*)',time):
            st=re.search(r'.*?(\d{1,2}).(\d+)..*?(\d+).+(\d*)',time)
            y=notify_time.split('-')[0]
            mon=st.group(1)
            d=st.group(2)
            h=st.group(3)
            min=st.group(4)
            if re.search(r'.*?(\d{1,2}).(\d+)..*?下午(\d+).+(\d*)',time):
                h=str(int(h)+12)
            if len(y)==1:
                y='0'+y
            if len(mon) == 1:
                mon = '0' + mon
            if len(d) == 1:
                d = '0' + d
            if len(h) == 1:
                h = '0' + h
            if len(min) == 1:
                min = '0' + min
        # 匹配**月**日(下午)HH
        elif re.search(r'.*?(\d{1,2}).(\d+)..*?(\d+).',time):
            st=re.search(r'.*?(\d{1,2}).(\d+)..*?(\d+).',time)
            y=notify_time.split('-')[0]
            mon=st.group(1)
            d=st.group(2)
            h=st.group(3)
            if re.search(r'.*?(\d{1,2}).(\d+)..*?下午(\d+).',time):
                h=str(int(h)+12)
            if len(y)==1:
                y='0'+y
            if len(mon) == 1:
                mon = '0' + mon
            if len(d) == 1:
                d = '0' + d
            if len(h) == 1:
                h = '0' + h
            min='00'
            #(r'.*?(\d+).(\d+)..*?(\d+).+(\d*)')
            # (r'.*?(\d+).(\d+)..*?下午(\d+).*?+(\d*)')
        else:
            y='2000'
            mon='01'
            d='01'
            h='00'
            min='00'
        report_time_=y+'-'+mon+'-'+d+' '+h+":"+min
        # time_=datetime.strptime(report_time_,'%Y-%m-%d %H:%M')
        return report_time_