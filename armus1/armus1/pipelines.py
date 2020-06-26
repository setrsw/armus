# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#db_model
import re
from scrapy.exceptions import DropItem
# from db_model.db_config import Notification
from db_model.notifications import Notification
from db_model.db_config import DBSession

class ArmusPipeline:

    def open_spider(self,spider):
        self.session=DBSession()
    def process_item(self, item, spider):
        self.reset_data(item)
        try:
            notification=Notification(url=item['url'],title=item['title'],college=item['college'],
                    speaker=item['speaker'],venue=item['venue'],time=item['time'],notify_time=item['notify_time'])
            #存入数据库Notification
            self.session.add(notification)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            pass
        return item

    def reset_data(self,item):
        #url为通知信息主码
        if 'url' not in item:
            raise DropItem('Invalid item found: %s'% item)

        if 'title' not in item:
            item['title']=''

        if 'college' not in item:
            item['college'] = ''

        if 'speaker' not in item:
            item['speaker'] = ''

        if 'venue' not in item:
            item['venue'] = ''

        if 'time' not in item:
            item['time'] = ''

        if item['notify_time']=='':
            if re.search('\d{4}\D{1,2}\d{1,2}\D{1,2}\d{1,2}',item['time']):
                nt=re.search('(\d{4})\D{1,2}(\d{1,2})\D{1,2}(\d{1,2})',item['time'])
                y=nt.group(1)
                m=nt.group(2)
                d=nt.group(3)
                item['notify_time']=y+'-'+m+'-'+d
            # item['notify_time'] = item['time']