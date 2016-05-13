#  coding: utf-8
#  author : Xiang
from PyQt4 import QtGui, QtCore
from initDatabase import SchoolDBSystem
from Homepage import MainWindow
from try_ import TryForm
import sys


class HITInformationManager(QtGui.QMainWindow, MainWindow, SchoolDBSystem):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        MainWindow.__init__(self)
        SchoolDBSystem.__init__(self)

        self.setupUi(self)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.exit_button.clicked.connect(QtCore.QCoreApplication.quit)

    def login(self):
        """
        登陆按钮
        :return:
        """
        username_input = self.Username_input.text()
        password_input = self.Password_input.text()
        self.cur.excute('select password from login where p_no = %s', username_input)
        password = self.cur.fetchone()
        if password == password_input:
            pass  # 跳转到登陆后的界面

    def register(self):
        """
        注册按钮
        :return:
        """
        self.hide()
        form_ = QtGui.QDialog()
        try_ = TryForm()
        try_.setupUi(form_)
        form_.show()
        self.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = HITInformationManager()
    window.show()
    sys.exit(app.exec_())
