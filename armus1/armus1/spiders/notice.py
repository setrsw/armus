# -*- coding: utf-8 -*-
import re
import time
from db_model.key_words import KeyWords
import scrapy
# from db_model import notifications
from armus1.items import Armus_Item

class NoticeSpider(scrapy.Spider):
    name = 'notice'

    def __init__(self, seed, title_urls, **kwargs):
        super().__init__(**kwargs)
        self.key_word=KeyWords()
        self.seed=seed
        self.title_urls=title_urls
        self.urls=list(title_urls.values())
        self.information={'title':self.key_word.title, 'speaker':self.key_word.speaker,
                          'time':self.key_word.time, 'venue':self.key_word.venue}

    def start_requests(self):
        urls=self.urls
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_url,meta={'url':url})

    def parse_url(self, response):
        #从self.urls中获取url
        url=response.meta['url']
        item={'url':'','college':'','title':'','speaker':'','time':'','venue':'','notify_time':''}
        texts=[]
        #爬取通知原文的发布时间
        if self.seed.notice_time_xpath !='':
            notify_time=response.xpath(self.seed.notice_time_xpath).xpath('.//text()').extract()
            notify_time=''.join(notify_time)
        else:
            notify_time=''
        # #根据xpath选择器爬取通知正文
        # contents=response.xpath(self.seed.text_xpath)
        # # item['notify_time']=notify_time
        # #爬取通知原文的每一行文本信息
        # for line in contents:
        #     content=line.xpath('.//text()').extract()
        #     content_=''.join(content)
        #     if content_.replace(' ','') !='':
        #         texts.append(content_.replace('\n',''))
        contents=response.xpath(self.seed.text_xpath).xpath('.//text()').extract()

        print('contents---->',contents)
        # test=contents.replace('\n',' --换行-- ')
        # print(test)
        content=''.join(contents).split('\n')
        for line in content:
            test = line.replace('\n', ' --换行-- ')
            print(test)
            if line.replace(' ','') !='':
                texts.append(line.replace('\n',''))
        print('texts-->',texts)
        #对原文信息与我们需要的信息进行匹配
        # for text in texts:
        #     text=text.replace('\xa0','').replace('：',':').replace('\n','').strip()
            #进行信息匹配
            # print(text)
        for (k,v) in self.information.items():
            #seed的v值部分有多个匹配字符，用‘，’隔开
            v_list=v.split(',')
            #对每个匹配模式进行匹配
            temp_list_k=[]
            for text in texts:
                text = text.replace('\xa0', '').replace('：', ':').replace('\r','').replace('\n', '').strip()
                if '简介' not in text.replace(' ',''):
                    for word in v_list:
                        if word in text.replace(' ',''):
                            temp=text
                            if len(text.replace(' ',''))>150:
                                if ':' in text:
                                    temp=text.split(':')[1]
                            #判断添加的内容是否与之前内容一样
                            if temp not in temp_list_k:
                                temp_list_k.append(temp)
            item[k]=','.join(temp_list_k)   #多个讲座时用‘,’隔开
        # item['url']=response.urljoin('')#获取当前url
        item['url']=url
        item['college']=self.seed.college#获取大学名称

        # 通知title位于主通知界面中的情况
        #实现过程有点困难
        if item['title'] =='':
            item['title']=list(self.title_urls.keys())[list(self.title_urls.values()).index(str(item['url']))]
        #标准通知时间     yyyy-mm-dd
        if notify_time=='':    #通知时间位于主通知界面中的情况
            notify_time=list(self.title_urls.keys())[list(self.title_urls.values()).index(item['url'])]
        nt=re.search(r'.*?(\d{4}).(\d+).(\d+)', notify_time)
        if nt is not None:
            # print(nt)
            notify_time=self.format_notice_time(nt)
        item['notify_time']=notify_time
        # print(notify_time)
        # print(item['time'])
        report_time=item['time']
        #标准讲座开始时间   yyyy-mm-dd hh:mm
        st=re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+).+(\d+)',report_time)
        if st is not None:
            item['time']=self.format_time(st,item['notify_time'])
        notification=Armus_Item(url=item['url'],college=item['college'],title=item['title'],
                                speaker=item['speaker'],venue=item['venue'],time=item['time'],notify_time=item['notify_time'])
        return notification

    def format_notice_time(self,notice_time):
        y=notice_time.group(1)
        m=notice_time.group(2)
        d=notice_time.group(3)
        if len(y)==2:
            y='20'+y
        if len(m)==1:
            m='0'+m
        if len(d)==1:
            d='0'+d
        print(y+'-'+m+"-"+d,'<---------通知时间')

        return y+'-'+m+"-"+d

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
        return y+'-'+mon+'-'+d+' '+h+":"+min