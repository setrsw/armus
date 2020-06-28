# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_armus(QWidget):
    def setupUi(self, armus):
        if not armus.objectName():
            armus.setObjectName(u"armus")
        armus.resize(1109, 839)
        armus.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"background-color: rgb(245, 245, 245);")
        self.gridLayout_2 = QGridLayout(armus)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 2, 3, 1, 1)

        self.splitter = QSplitter(armus)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.comboBox_2 = QComboBox(self.splitter)
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(10)
        self.comboBox_2.setFont(font)
        self.splitter.addWidget(self.comboBox_2)
        self.lineEdit_6 = QLineEdit(self.splitter)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.splitter.addWidget(self.lineEdit_6)

        self.gridLayout_2.addWidget(self.splitter, 1, 5, 1, 1)

        self.splitter_4 = QSplitter(armus)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter_4)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_4 = QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFont(font)

        self.gridLayout.addWidget(self.pushButton_4, 5, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_3 = QSplitter(self.layoutWidget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.label_2 = QLabel(self.splitter_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 12pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.splitter_3.addWidget(self.label_2)
        self.pushButton_3 = QPushButton(self.splitter_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.splitter_3.addWidget(self.pushButton_3)

        self.verticalLayout_2.addWidget(self.splitter_3)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer_7)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.verticalLayout.addWidget(self.label_8)

        self.lineEdit_7 = QLineEdit(self.layoutWidget)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.verticalLayout.addWidget(self.lineEdit_7)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout.addWidget(self.lineEdit_3)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout.addWidget(self.label_6)

        self.lineEdit_4 = QLineEdit(self.layoutWidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout.addWidget(self.lineEdit_4)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout.addWidget(self.label_7)

        self.lineEdit_5 = QLineEdit(self.layoutWidget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.verticalLayout.addWidget(self.lineEdit_5)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.splitter_2 = QSplitter(self.layoutWidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.pushButton = QPushButton(self.splitter_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.splitter_2.addWidget(self.pushButton)
        self.pushButton_2 = QPushButton(self.splitter_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.splitter_2.addWidget(self.pushButton_2)

        self.verticalLayout_2.addWidget(self.splitter_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 4, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 11pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout_3.addWidget(self.label)

        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setStyleSheet(u"\n"
"font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.verticalLayout_3.addWidget(self.comboBox)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)


        self.gridLayout.addLayout(self.verticalLayout_3, 2, 0, 1, 1)

        self.splitter_4.addWidget(self.layoutWidget)

        self.gridLayout_2.addWidget(self.splitter_4, 2, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 4, 1, 1)

        self.tableView = QTableView(armus)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout_2.addWidget(self.tableView, 2, 5, 1, 1)

        self.label_9 = QLabel(armus)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout_2.addWidget(self.label_9, 0, 5, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 3, 5, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.pushButton_5 = QPushButton(armus)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_2.addWidget(self.pushButton_5, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 2, 1, 1)


        self.retranslateUi(armus)

        QMetaObject.connectSlotsByName(armus)
    # setupUi

    def retranslateUi(self, armus):
        armus.setWindowTitle(QCoreApplication.translate("armus", u"学术讲座信息表", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("armus", u"\u5168\u90e8\u5927\u5b66/\u5b66\u9662", None))

        self.pushButton_4.setText(QCoreApplication.translate("armus", u"\u722c\u53d6\u5168\u90e8\u4fe1\u606f/\u66f4\u65b0", None))
        self.label_2.setText(QCoreApplication.translate("armus", u"\u6dfb\u52a0\u65b0\u7f51\u5740", None))
        self.pushButton_3.setText(QCoreApplication.translate("armus", u"\u8bf4\u660e", None))
        self.label_8.setText(QCoreApplication.translate("armus", u"\u5b66\u6821/\u5b66\u9662\u7f51\u5740:", None))
        self.label_3.setText(QCoreApplication.translate("armus", u"\u722c\u53d6\u5b66\u6821/\u5b66\u9662\u540d\uff1a", None))
        self.lineEdit.setText("")
        self.label_4.setText(QCoreApplication.translate("armus", u"\u4e0b\u4e00\u9875\u6807\u7b7expath\u8def\u5f84\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("armus", u"\u5177\u4f53\u901a\u77e5\u7f51\u7ad9xpath\u8def\u5f84\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("armus", u"\u901a\u77e5\u6b63\u6587\u7684xpath\u8def\u5f84\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("armus", u"\u901a\u77e5\u65f6\u95f4\u7684xpath\uff1a(\u9ed8\u8ba4\u4e3a\u7a7a)", None))
        self.pushButton.setText(QCoreApplication.translate("armus", u"\u6dfb\u52a0", None))
        self.pushButton_2.setText(QCoreApplication.translate("armus", u"\u66f4\u65b0\u5b66\u6821\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("armus", u"\u6392\u5e8f\u65b9\u5f0f\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("armus", u"\u521d\u59cb\u663e\u793a", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("armus", u"\u6309\u4e3e\u529e\u65f6\u95f4\u6392\u5e8f", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("armus", u"\u6309\u53d1\u5e03\u65f6\u95f4\u6392\u5e8f", None))

        self.label_9.setText(QCoreApplication.translate("armus", u"\u5b66\u6821\u901a\u77e5\u7f51\u7ad9:", None))
        self.pushButton_5.setText(QCoreApplication.translate("armus", u"\u722c\u53d6/\u66f4\u65b0", None))
    # retranslateUi

