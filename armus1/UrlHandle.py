import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class UrlHandle:
    def __init__(self):
        self.start_url=None     #start_url是指学校或学院学术通知的网页
        self.nextpage_xpath='.//*[contain(text(),"下一页")]'
        self.title_urls={}      #设置  通知标题——网址字典
        self.existed_urls=[]
        self.title_word=''
        self.urls=[]    #待爬取的通知网站
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,service_args=['--ignore-ssl-errors=true'])
        self.wait = WebDriverWait(self.driver, 10)

    def set_start_url(self,start_url):
        self.start_url=start_url

    #设置Notification中已经存在的通知网站
    def set_existed_urls(self,existed_urls):
        self.existed_urls=existed_urls

    #设置获取每个具体通知网站的xpath语句
    def set_url_xpath(self,url_xpath):
        self.url_xpath=url_xpath

    #设置需要爬取的通知关键字,设置成为列表
    def set_title_word(self,title_word):
        self.title_word=title_word

    #设置通知爬取下一页的标签
    def set_nextpage_xpath(self,nextpage_xpath):
        self.nextpage_xpath=nextpage_xpath

    def parse_urls(self):
        if self.url_xpath==None:
            # print('请先设置url_xpath参数：')
            self.url_xpath=str(input('请先设置url_xpath参数：'))
        print(self.driver.page_source)
        # html = self.driver.execute_script("return document.documentElement.outerHTML")
        # print(html)
        # html = self.driver.find_element_by_xpath("//*" ).get_attribute("outerHTML")
        # print(html)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.nextpage_xpath)))
        print(self.driver.page_source)
        elements=self.driver.find_elements_by_xpath(self.url_xpath)
        print(elements)
        print('test',len(elements))

        for element in elements:    #find_element_by_xpath('.//a').
            try:
                print('erw')
                self.title_urls[element.text]=element.find_element_by_xpath('.//a').get_attribute('href')     #获取具体通知的url与通知title     {titles ：urls}
                print('test---->',self.title_urls[element.text])
            except Exception as e:
                print(e)
                pass
    def get_next_page(self,pre_page):
        try:
            # print(self.nextpage_xpath)
            # wait.until(EC.presence_of_element_located((By.XPATH, self.nextpage_xpath)))
            next_page=self.driver.find_element_by_xpath(self.nextpage_xpath)
            next_page.click()
            # time.sleep(1)           #加上定时才能实现翻页
            # self.driver.execute_script('arguments[0].click();', next_page)
            if pre_page==self.driver.page_source:   #判断是否是最后一页资源
                return False
            return True
        except Exception as e:
            return False

    #以字典 {title : url} 形式获取所有通知
    def get_all_url(self):
        self.driver.get(self.start_url)
        self.parse_urls()
        page=1
        while self.get_next_page(self.driver.page_source):
            self.parse_urls()
            if page<=70:
                page+=1
            else:
                break
    # 过滤不包含关键字的通知网站
    def filte_word_url(self):
        if self.title_word == '':
            print('title_word is none')
            return
        for title in list(self.title_urls.keys()):  #遍历时不能修改字典元素
            key_words=self.title_word.split(',')
            # print(key_words)
            for word in key_words:
                if word in title.replace('：',':'):
                    is_report=True
                    # print(title)
                    break
                else:
                    is_report=False
            if not is_report:
                del self.title_urls[title]

    #过滤已经爬取的网站
    # def filte_existed_url(self):
    #     for url in self.title_urls.values():
    #         if url not in self.existed_urls:
    #             self.urls.append(url)
    def filte_existed_url(self):
        # temp_title_urls=self.title_urls
        for title in list(self.title_urls.keys()):
            if self.title_urls[title] in self.existed_urls:
                print(self.title_urls[title])
                del self.title_urls[title]

    # def get_filte_urls(self):
    #     self.get_all_url()
    #     self.filte_word_url()
    #     self.filte_existed_url()
    #     #过滤后的需要爬取的urls
    #     return self.urls
    def get_filte_urls(self):
        self.get_all_url()
        self.filte_word_url()
        self.filte_existed_url()
        #过滤后的需要爬取的urls
        return self.title_urls