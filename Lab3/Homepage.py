# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Homepage.ui'
#
# Created: Thu May 12 22:27:15 2016
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(606, 374)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(160, 130, 291, 70))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.Username_table = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.Username_table.setMargin(0)
        self.Username_table.setObjectName(_fromUtf8("Username_table"))
        self.Username_text = QtGui.QLabel(self.horizontalLayoutWidget)
        self.Username_text.setObjectName(_fromUtf8("Username_text"))
        self.Username_table.addWidget(self.Username_text)
        spacerItem = QtGui.QSpacerItem(58, 68, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Username_table.addItem(spacerItem)
        self.Username_input = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.Username_input.setObjectName(_fromUtf8("Username_input"))
        self.Username_table.addWidget(self.Username_input)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(160, 180, 291, 51))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.Password_table = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.Password_table.setMargin(0)
        self.Password_table.setObjectName(_fromUtf8("Password_table"))
        self.Password_text = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.Password_text.setObjectName(_fromUtf8("Password_text"))
        self.Password_table.addWidget(self.Password_text)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Password_table.addItem(spacerItem1)
        self.Password_input = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.Password_input.setObjectName(_fromUtf8("Password_input"))
        self.Password_input.setEchoMode(QtGui.QLineEdit.Password)
        self.Password_table.addWidget(self.Password_input)
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(110, 30, 391, 81))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.Title_lable = QtGui.QHBoxLayout(self.layoutWidget)
        self.Title_lable.setMargin(0)
        self.Title_lable.setObjectName(_fromUtf8("Title_lable"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Title_lable.addItem(spacerItem2)
        self.title = QtGui.QLabel(self.layoutWidget)
        self.title.setStyleSheet(_fromUtf8("font: 65 20pt \"Levenim MT\";"))
        self.title.setObjectName(_fromUtf8("title"))
        self.Title_lable.addWidget(self.title)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Title_lable.addItem(spacerItem3)
        self.layoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(110, 250, 389, 41))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.Option_table = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.Option_table.setMargin(0)
        self.Option_table.setObjectName(_fromUtf8("Option_table"))
        self.login_button = QtGui.QPushButton(self.layoutWidget_3)
        self.login_button.setStyleSheet(_fromUtf8("font: 75 10pt \"Segoe Print\";"))
        self.login_button.setObjectName(_fromUtf8("login_button"))
        self.Option_table.addWidget(self.login_button)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Option_table.addItem(spacerItem4)
        self.register_button = QtGui.QPushButton(self.layoutWidget_3)
        self.register_button.setStyleSheet(_fromUtf8("font: 75 10pt \"Segoe Print\";"))
        self.register_button.setObjectName(_fromUtf8("register_button"))
        self.Option_table.addWidget(self.register_button)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Option_table.addItem(spacerItem5)
        self.exit_button = QtGui.QPushButton(self.layoutWidget_3)
        self.exit_button.setStyleSheet(_fromUtf8("font: 75 10pt \"Segoe Print\";注册\n"
""))
        self.exit_button.setObjectName(_fromUtf8("exit_button"))
        self.Option_table.addWidget(self.exit_button)
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(40, 150, 101, 41))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 606, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Username_text.setText(_translate("MainWindow", "用户名", None))
        self.Password_text.setText(_translate("MainWindow", "密  码", None))
        self.title.setText(_translate("MainWindow", "工大师生信息管理系统", None))
        self.login_button.setText(_translate("MainWindow", "登录", None))
        self.register_button.setText(_translate("MainWindow", "注册", None))
        self.exit_button.setText(_translate("MainWindow", "退出", None))

