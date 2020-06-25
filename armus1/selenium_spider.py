import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#db_model
from db_model.notifications import Notification
from db_model.key_words import KeyWords
# from db_model.notifications import Notification
from db_model.db_config import DBSession
#连接chrome浏览器
chrome_options=Options()
chrome_options.add_argument('--headless')
browser=webdriver.Chrome(options=chrome_options)
wait=WebDriverWait(browser,1)

class SeleniumSpider:
    def __init__(self, seed, title_urls):
        self.session = DBSession()
        self.key_word=KeyWords()    #匹配关键字
        self.seed = seed
        self.title_urls = title_urls
        self.urls = list(title_urls.values())
        self.information = {'title': self.key_word.title, 'speaker': self.key_word.speaker,
                            'time': self.key_word.time, 'venue': self.key_word.venue}
    def start_selenium(self):
        for url in self.urls:
            try:
                item=self.url_parse(url)
                self.save_data(item)
            except Exception as e:
                print (e)
                pass
    def url_parse(self,url):
        browser.get(url)
        item = {'url': '', 'college': '', 'title': '', 'speaker': '', 'time': '', 'venue': '', 'notify_time': ''}
        texts = []
        # 爬取通知原文的发布时间
        if self.seed.notice_time_xpath != '':
            notify_time = browser.find_element_by_xpath(self.seed.notice_time_xpath).text
        else:
            notify_time = ''
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,self.seed.text_xpath)))
            contents=browser.find_element_by_xpath(self.seed.text_xpath).text
            print('contents---->', contents)
            # test=contents.replace('\n',' --换行-- ')
            # print(test)
            content =contents.split('\n')
            for line in content:
                if line.replace(' ', '') != '':
                    texts.append(line)
            print('texts-->', texts)
            # 对原文信息与我们需要的信息进行匹配
            # 进行信息匹配
            for (k, v_list) in self.information.items():
                # 对每个匹配模式进行匹配
                temp_list_k = []
                for text in texts:
                    text = text.replace('\xa0', '').replace('：', ':').replace('\r', '').replace('\n', '').strip()
                    if '简介' not in text.replace(' ', '') or '介绍' not in text.replace(' ', ''):
                        for word in v_list:
                            if word in text.replace(' ', ''):
                                temp = text
                                if len(text.replace(' ', '')) > 150:
                                    if ':' in text:
                                        temp = text.split(':')[1]
                                # 判断添加的内容是否与之前内容一样
                                if temp not in temp_list_k:
                                    temp_list_k.append(temp)
                item[k] = ','.join(temp_list_k)  # 多个讲座时用‘,’隔开
        except Exception as e:
            print(e)
            pass
        # item['url']=response.urljoin('')#获取当前url
        item['url'] = url
        item['college'] = self.seed.college  # 获取大学名称

        # 通知title位于主通知界面中的情况
        # 实现过程有点困难
        if item['title'] == '':
            item['title'] = list(self.title_urls.keys())[list(self.title_urls.values()).index(str(item['url']))]
        # 标准通知时间     yyyy-mm-dd
        if notify_time == '':  # 通知时间位于主通知界面中的情况
            notify_time = list(self.title_urls.keys())[list(self.title_urls.values()).index(item['url'])]
        nt = re.search(r'.*?(\d{4}).(\d+).(\d+)', notify_time)
        if nt is not None:
            notify_time = self.format_notice_time(nt)
        item['notify_time'] = notify_time
        # print(notify_time)
        # print(item['time'])
        report_time = item['time']
        # 标准讲座开始时间   yyyy-mm-dd hh:mm
        st = re.search(r'.*?(\d{4}).(\d+).(\d+)..*?(\d+).+(\d+)', report_time)
        if st is not None:
            item['time'] = self.format_time(st)
        notification = item
        return notification
        # if not contents:
        #     contents=contents.find_element_by_xpath('..')
        #     print(contents.text)
        # else:
        #     print('contents')
        # print(contents.text.replace('\n','换行'))
        # content=contents.text.split('\n')
        # print(content)

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
        notice_date=y+'-'+m+"-"+d
        # notice_time_=datetime.strptime(notice_date,'%Y-%m-%d')
        return notice_date

    def format_time(self,time):
        date=self.format_notice_time(time)
        h=time.group(4)
        m=time.group(5)
        if len(h)==1:
            h='0'+h
        if len(m)==1:
            m='0'+m
        print(date+' '+h+':'+m,'<---------讲座时间')
        return date+' '+h+':'+m

    def save_data(self,item):
        self.reset_data(item)
        if '-' not in item['time']:
            item['time']=self.format_time_again(item['time'],item['notify_time'])
        try:
            # time=self.format_time_again(item['time'],item['notify_time'])
            # item['time']=time
            if '-' not in item['time']:
                item['time'] = self.format_time_again(item['time'], item['notify_time'])
            notification = Notification(url=item['url'], title=item['title'], college=item['college'],
                                        speaker=item['speaker'], venue=item['venue'], time=item['time'],
                                        notify_time=item['notify_time'])
            # 存入数据库Notification
            self.session.add(notification)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            pass
    def reset_data(self, item):
        # url为通知信息主码
        if 'url' not in item:
            print('Invalid item found: %s' % item)

        if 'title' not in item:
            item['title'] = ''

        if 'college' not in item:
            item['college'] = ''

        if 'speaker' not in item:
            item['speaker'] = ''

        if 'venue' not in item:
            item['venue'] = ''

        if 'time' not in item:
            item['time'] = ''

        if item['notify_time'] == '':
            item['notify_time'] = item['time']

    def format_time_again(self,time,notify_time):
        if re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})',time):
            # if re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?',time):
            st=re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})',time)
            y=notify_time.split('-')[0]
            mon=st.group(1)
            d=st.group(2)
            h=st.group(3)
            if '下午' in time:
                if int(h)<12:
                    h+=12
            if re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?(\d{1,2})',time):
                st=re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?(\d{1,2})',time)
                min=st.group(4)
            else:
                min='00'
            report_time=y+'-'+mon+'-'+d+' '+h+':'+min
            return report_time
        elif re.search(r'\D*?(\d{4})年(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})',time):
            # if re.search(r'\D*?(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?',time):
            st=re.search(r'\D*?(\d{4})年(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})',time)
            y=st.group(1)
            mon=st.group(2)
            d=st.group(3)
            h=st.group(4)
            if '下午' in time:
                if int(h)<12:
                    h+=12
            if re.search(r'\D*?(\d{4})年(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?(\d{1,2})',time):
                st=re.search(r'\D*?(\d{4})年(\d{1,2})月(\d{1,2})日\D*?(\d{1,2})\D+?(\d{1,2})',time)
                min=st.group(5)
            else:
                min='00'
            report_time=y+'-'+mon+'-'+d+' '+h+':'+min
            return report_time

    # def format_time_again(self,time,notify_time):
    #     #匹配****年**月**日(下午)HH:MM
    #     if re.search(r'.*?(\d{4}).(\d{1,2}).(\d{1,2}).*?(\d{1,2}).(\d{1,2})\D', time):
    #         st=re.search(r'.*?(\d{4}).(\d+).(\d+).*?(\d{1,2}).+(\d{1,2})\D', time)
    #         y = st.group(1)
    #         mon = st.group(2)
    #         d = st.group(3)
    #         if len(y) == 2:
    #             y = '20' + y
    #         if len(mon) == 1:
    #             mon = '0' + mon
    #         if len(d) == 1:
    #             d = '0' + d
    #         h = st.group(4)
    #         if re.search(r'.*?(\d{4}).(\d+).(\d+).*?下午(\d{1,2}).+(\d{1,2})\D', time):
    #             if int(h)<12:
    #                 h=str(int(h)+12)
    #         min = st.group(5)
    #         if len(h) == 1:
    #             h = '0' + h
    #         if len(min) == 1:
    #             min = '0' + min
    #     # 匹配****年**月**日(下午)HH
    #     elif re.search(r'.*?(\d{4}).(\d+).(\d{1,2}).*?(\d{1,2})\D', time):
    #         st=re.search(r'.*?(\d{4}).(\d+).(\d{1,2}).*?(\d{1,2})\D', time)
    #         y = st.group(1)
    #         mon = st.group(2)
    #         d = st.group(3)
    #         if len(y) == 2:
    #             y = '20' + y
    #         if len(mon) == 1:
    #             mon = '0' + mon
    #         if len(d) == 1:
    #             d = '0' + d
    #         h = st.group(4)
    #         if re.search(r'.*?(\d{4}).(\d+).(\d{1,2}).*?下午(\d{1,2})\D', time):
    #             h=str(int(h)+12)
    #         if len(h) == 1:
    #             h = '0' + h
    #         min='00'
    #     # 匹配**月**日(下午)HH:MM
    #     elif re.search(r'.*?(\d{1,2}).(\d+).*?(\d+).+(\d{1,2})\D',time):
    #         st=re.search(r'.*?(\d{1,2}).(\d+).*?(\d+).+(\d{1,2})\D',time)
    #         y=notify_time.split('-')[0]
    #         mon=st.group(1)
    #         d=st.group(2)
    #         h=st.group(3)
    #         min=st.group(4)
    #         if re.search(r'.*?(\d{1,2}).(\d+).*?下午(\d+).+(\d{1,2})\D',time):
    #             h=str(int(h)+12)
    #         if len(y)==1:
    #             y='0'+y
    #         if len(mon) == 1:
    #             mon = '0' + mon
    #         if len(d) == 1:
    #             d = '0' + d
    #         if len(h) == 1:
    #             h = '0' + h
    #         if len(min) == 1:
    #             min = '0' + min
    #     # 匹配**月**日(下午)HH
    #     elif re.search(r'.*?(\d{1,2}).(\d+).*?(\d{1,2})\D',time):
    #         st=re.search(r'.*?(\d{1,2}).(\d+).*?(\d{1,2})\D',time)
    #         y=notify_time.split('-')[0]
    #         mon=st.group(1)
    #         d=st.group(2)
    #         h=st.group(3)
    #         if re.search(r'.*?(\d{1,2}).(\d+).*?下午(\d{1,2})\D',time):
    #             h=str(int(h)+12)
    #         if len(y)==1:
    #             y='0'+y
    #         if len(mon) == 1:
    #             mon = '0' + mon
    #         if len(d) == 1:
    #             d = '0' + d
    #         if len(h) == 1:
    #             h = '0' + h
    #         min='00'
    #         #(r'.*?(\d+).(\d+)..*?(\d+).+(\d*)')
    #         # (r'.*?(\d+).(\d+)..*?下午(\d+).*?+(\d*)')
    #     elif re.search(r'.*?(\d{4}).(\d{1,2}).(\d{1,2})'):
    #         y = time.group(1)
    #         m = time.group(2)
    #         d = time.group(3)
    #         if len(y) == 2:
    #             y = '20' + y
    #         if len(m) == 1:
    #             m = '0' + m
    #         if len(d) == 1:
    #             d = '0' + d
    #         notice_date = y + '-' + m + "-" + d
    #         # notice_time_ = datetime.strptime(notice_date, '%Y-%m-%d')
    #         return notice_date
    #     else:
    #         y='2000'
    #         mon='01'
    #         d='01'
    #         h='00'
    #         min='00'
    #     report_time_=y+'-'+mon+'-'+d+' '+h+":"+min
    #     # time_=datetime.strptime(report_time_,'%Y-%m-%d %H:%M')
    #     return report_time_