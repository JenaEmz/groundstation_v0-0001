# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImgWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import rospy
import threading
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImgWindow(QtWidgets.QTableWidget):
    def __init__(self):
        super(ImgWindow, self).__init__()
        self.setupUi(self)
        self.IOinit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(725, 527)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 100, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(60, 40, 113, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 50, 67, 17))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "接收图像"))
        self.label.setText(_translate("Form", "飞机ID"))

    def IOinit(self):
        self.cv_bridge = CvBridge()
        self.camera_msg = 'uav1/camera/rgb/image_raw'
        rospy.Subscriber(self.camera_msg, Image, self.getImg)

    def getImg(self,raw_image):
        frame = self.cv_bridge.imgmsg_to_cv2(raw_image)
        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
