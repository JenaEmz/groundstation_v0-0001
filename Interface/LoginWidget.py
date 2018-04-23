from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from Interface.MainWindow import MainWindow

import pickle
global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
class TabWidget(QTabWidget):

    def __init__(self, parent=None):

        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        ALLUSER = {}
        USRNAME = []
        try:
            with open('USRNAME.pickle', 'rb+') as f:
                USRNAME = pickle.load(f)
        except EOFError:  # 捕获异常EOFError 后返回None
            pass
        try:
            with open('ALLUSER.pickle', 'rb+') as f:
                ALLUSER = pickle.load(f)
        except EOFError:  # 捕获异常EOFError 后返回None
            pass

        tempUsrName = {}

        super(TabWidget, self).__init__(parent)
        self.setWindowTitle('无人机地面站v0.01')
        self.resize(400, 260)
        self.center()
        palette=QPalette()
        icon=QPixmap('background.jpg').scaled(400, 260)
        palette.setBrush(self.backgroundRole(), QBrush(icon)) #添加背景图片
        self.setPalette(palette)
        self.initUI()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        #self.setGeometry(0, 0, 450, 300)
        self.signUpButton = QPushButton( 'Sign up', self)
        self.signUpButton.move(300, 200)
        self.signInButton = QPushButton( 'Sign in', self)
        self.signInButton.move(200, 200)
        self.usrNameLine = QLineEdit( self )
        self.usrNameLine.setPlaceholderText('User Name')
        self.usrNameLine.setFixedSize(200, 30)
        self.usrNameLine.move(100, 50)
        self.passWordLine = QLineEdit(self)
        self.passWordLine.setEchoMode(QLineEdit.Password)
        self.passWordLine.setPlaceholderText('Pass Word')
        self.passWordLine.setFixedSize(200, 30)
        self.passWordLine.move(100, 120)
        self.signInButton.clicked.connect(self.signIn)
        self.signUpButton.clicked.connect(self.signUp)

    def signIn(self):
        global CURUSER, tempUsrName, ALLUSER, USRNAME
        if self.usrNameLine.text() not in ALLUSER:
            QMessageBox.information(self,"Information","用户不存在，请注册")
        elif ALLUSER[self.usrNameLine.text()] == self.passWordLine.text():
            QMessageBox.information(self,"Information","你登录了!")
            CURUSER = self.usrNameLine.text()
            self.hide()
            self.w1= MainWindow()
            self.w1.show()
        else:
            QMessageBox.information(self,"Information","密码错误!")

    def signUp(self):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        if self.usrNameLine.text() in ALLUSER:
            QMessageBox.information(self,"Information","用户已存在!")
        elif len(self.passWordLine.text()) < 3:
            QMessageBox.information(self,"Information","密码太短!")
        else:
            tempUsrName.clear()
            tempUsrName[self.usrNameLine.text()] = self.passWordLine.text()
            for key, value in tempUsrName.items():
                ALLUSER[key] = value
                USRNAME.append(key)
                with open('ALLUSER.pickle', 'rb+') as f:
                    pickle.dump(ALLUSER, f)
                with open('USRNAME.pickle', 'rb+') as f:
                    pickle.dump(USRNAME, f)
                QMessageBox.information(self, "Information", "Success!")



