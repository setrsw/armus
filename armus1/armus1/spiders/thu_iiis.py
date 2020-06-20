# -*- coding: utf-8 -*-
#清华大学交互信息学院

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from armus1.items import Armus_Item

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
    def parse_item(self, response):

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        reports=response.xpath('.//tbody//tr')
        for report in reports:
            notify_time=''
            title=report.xpath('./td/a/text()').getall()
            title = ' '.join(''.join(title).split())
            # print(notice_url)
            speaker=report.xpath('./td[2]//text()').getall()
            speaker=' '.join(''.join(speaker).split())
            time=report.xpath('./td[3]//text()').get()
            venue=report.xpath('./td[4]//text()').get()
            notice_url = self.domain_url + report.xpath('./td/a/@href').get()
            item=Armus_Item(title=title,speaker=speaker,venue=venue,
                          time=time,url=notice_url,college=self.college,notify_time=notify_time)
            yield item
        next_page = response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_item)