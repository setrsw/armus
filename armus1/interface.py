import time

from PySide2 import QtGui

from PySide2 import QtCore
from PySide2.QtCore import Qt
    # (QCoreApplication, QDate, QDateTime, QMetaObject,
    # QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
#                            QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
#                            QPixmap, QRadialGradient, QStandardItemModel, QStandardItem)
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide2.QtWidgets import QApplication, QMessageBox

from DataSpiderr import Data_Spider
from db_model.notifications import *

from db_model.seeds import Seed
from mainWindow import Ui_armus
# from db_model.notifications import Notification

class Stats(Ui_armus):
    def __init__(self):
        # 从文件中加载UI定义
        # qfile=QFile(r'E:\Pycharm\armus1\ui\armus1.ui')
        # qfile.open(QFile.ReadOnly)
        # # qfile_stats.close()
        # # 从 UI 定义中动态 创建一个相应的窗口对象
        # # 注意：里面的控件对象也成为窗口对象的属性了
        # # 比如 self.ui.button , self.ui.textEdit
        # # loader=QUiLoader()
        # self.ui=QUiLoader().load(qfile)
        # self.ui.show()
        super(Stats,self).__init__()
        # self.ui=Ui_armus()

        # self.tableView.setModel()
        db=QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('universitys.db')
        self.spider=Data_Spider()#爬虫连接
        self.session=DBSession()#数据库连接
        self.setupUi(self)
        # self.query=QSqlQuery(db)
        self.init_connect_db()
        # self.model = QStandardItemModel()  # 存储任意结构数据
        # self.model=QSqlQueryModel()
        self.comboBox.activated[str].connect(self.orderinfo)
        self.pushButton.clicked.connect(self.add_college)
        self.pushButton_2.clicked.connect(self.update_college)
        self.pushButton_4.clicked.connect(self.spider_info)
        # self.pushButton_3.clicked.connect(self.help_info)
        self.comboBox_2.activated[str].connect(self.link_collegeurl)

    #初始化连接数据库
    def init_connect_db(self):
        self.model = QSqlTableModel()
        self.tableView.setModel(self.model)
        self.model.setTable('notifications')
        self.model.setHeaderData(0, Qt.Horizontal, "全文链接")
        self.model.setHeaderData(1, Qt.Horizontal, "讲座标题")
        self.model.setHeaderData(2, Qt.Horizontal, "报告大学")
        self.model.setHeaderData(3, Qt.Horizontal, "报告人")
        self.model.setHeaderData(4, Qt.Horizontal, "报告地点")
        self.model.setHeaderData(5, Qt.Horizontal, "举办时间")
        self.model.setHeaderData(6, Qt.Horizontal, "发布时间")
        # self.model.setFilter('college="华南理工大学软件学院"')
        self.model.select()

    #排序筛选信息
    def orderinfo(self,text):
        if text=="按举办时间排序":
            # print('按举办时间排序')
            self.model.setFilter('title like "%%密码%" or title like "%%安全%" or title like "%security%"')
            self.model.setSort(5,Qt.DescendingOrder)
            self.model.select()

        elif text=='按发布时间排序':
            # print('按发布时间排序')
            self.model.setFilter('title like "%%密码%" or title like "%%安全%" or title like "%security%"')
            self.model.setSort(6, Qt.DescendingOrder)
            self.model.select()
        else:
            self.model.setFilter('url like "%%"')
            self.model.select()

            # QMessageBox.critical(NULL, "critical", "Content", QMessageBox.Yes, QMessageBox.Yes) #带按键


    def add_college(self):  #添加学校网页
        url=self.lineEdit_6.text()
        college=self.lineEdit.text()
        nextpage=self.lineEdit_2.text()
        url_xpath=self.lineEdit_3.text()
        text_xpath=self.lineEdit_4.text()
        notify_time=self.lineEdit_5.text()
        time.sleep(1)
        self.spider.set_college_url(url)
        self.spider.set_college(college)
        self.spider.set_next_xpath(nextpage)
        self.spider.set_url_xpath(url_xpath)
        self.spider.set_text_xpath(text_xpath)
        self.spider.set_notify_time_xpath(notify_time)
        self.spider.set_title_word()
        self.spider.insert_seed()

    def update_college(self):
        list_college=self.session.query(Seed).all()
        num=self.comboBox_2.count()
        colleges=[]
        for i in range(num):
            colleges.append(self.comboBox_2.itemText(i))
        for row in list_college:
            if row.college not in colleges:
                self.comboBox_2.addItem(row.college)

    def link_collegeurl(self,text):
        college=self.session.query(Seed).filter(Seed.college==text).first()
        if college!=None:
            self.lineEdit_6.setText(college.start_url)
            self.model.setFilter('college="%s"'%(text))
            self.model.select()
        else:
            self.lineEdit_6.setText('')
            self.model.select()
    def spider_info(self):
        self.spider.universities_spider()
        MESSAGE = "更新/爬取学术信息完成"
        msgBox = QMessageBox(QMessageBox.Question,
                             "提示", MESSAGE,
                             QMessageBox.NoButton, self)
        msgBox.addButton("确定", QMessageBox.AcceptRole)
        msgBox.exec_()

if __name__=='__main__':
    app=QApplication([])
    stats=Stats()
    stats.show()
    app.exec_()

