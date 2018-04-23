# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GpsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets,QtWebChannel

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,QMessageBox
from Utils.GpsPoints import GpsPoints
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from Utils.RosIO.Rosio import RosIO
import threading,time

class GpsWindow(QtWidgets.QTableWidget):
    def __init__(self):
        super(GpsWindow, self).__init__()
        self.IO = RosIO()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(758, 511)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 101, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_1.setObjectName("button_1")
        self.verticalLayout.addWidget(self.button_1)
        self.button_1.clicked.connect(self.setTakeoff)
        self.button_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_2.setObjectName("button_2")
        self.button_2.clicked.connect(self.receiveTarget)
        self.verticalLayout.addWidget(self.button_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.setHeight)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.setLand)

        self.gpsWindow = QtWebEngineWidgets.QWebEngineView(self)
        self.gpsWindow.setGeometry(QtCore.QRect(90, 10, 641, 481))
        self.gpsWindow.setUrl(QtCore.QUrl("file:///home/jena/PycharmProjects/ProgrammeDesign/final/map.html"))

        self.gpspoint = GpsPoints(31.145317,121.424048,31.145317, 121.424048)
        self.gpstarget = GpsPoints(31.145317,121.424048,31.145317, 121.424048 )

        self.getposThread = threading.Thread(target=self.updateUAVpos)
        self.getposThread.start()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "作业1"))
        self.button_1.setText(_translate("Form", "起飞"))
        self.button_2.setText(_translate("Form", "设定目标点"))
        self.pushButton_3.setText(_translate("Form", "设高度"))
        self.pushButton.setText(_translate("Form", "降落"))

    def IoInit(self):
        pass

    def updateUAVpos(self):
        while(1):
            self.gpspoint.x,self.gpspoint.y = self.IO.uav.returnPosToParent()
            self.gpspoint.LocaltoWgs84()
            self.gpsWindow.page().runJavaScript("updateUAV({0},{1})".format(round(self.gpspoint.lon,8),round(self.gpspoint.lat,8)))
            time.sleep(0.5)

    def receiveTarget(self):
        self.gpsWindow.page().runJavaScript("addWaypoint()",self.getTargetgps)

    def getTargetgps(self,latlon):
        if(latlon[0] is not None):
            print(latlon)
            self.gpstarget.lat = latlon[0]
            self.gpstarget.lon = latlon[1]
            self.gpstarget.Wgs84toLocal()
            self.IO.uav.SetPose(self.gpstarget.x,self.gpstarget.y)
            print(self.gpstarget.x,self.gpstarget.y)
        else:
            warning = QMessageBox.information(self,
                                    "等等",
                                    "高德地图未加载完成",
                                    QMessageBox.Yes)

    def setTakeoff(self):
        self.IO.Motorservice(True)
        self.IO.uav.SetPose(z=3)

    def setHeight(self):
        if(self.lineEdit.text().isdigit()):
            self.IO.uav.SetPose(z=float(self.lineEdit.text()))
        else:
            QMessageBox.information(self,"警告","高度必须是数字",QMessageBox.yes)

    def setLand(self):
        self.IO.uav.SetPose(z=0)
        self.IO.Motorservice(False)