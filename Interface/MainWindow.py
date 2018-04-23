from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

from Interface.GpsWindow import GpsWindow
from Interface.FileWindow import FileWindow
from Interface.ImgWindow import ImgWindow
from Interface.ParamWindow import ParamWindow

class MainWindow(QTabWidget):

    global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME

    def __init__(self):
        super(MainWindow, self).__init__()
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.resize(738, 521)
        self.move(qr.topLeft())

        self._gpswindow = GpsWindow()
        self.addTab(self._gpswindow,"Gps")
        self._filewindow = FileWindow()
        self._paramwindow = ParamWindow()
        self.addTab(self._filewindow, "数据处理")
        self.addTab(self._paramwindow, "参数设置")