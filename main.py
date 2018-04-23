from Interface import LoginWidget
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer

import sys
import os
import pickle

if __name__ == '__main__':
    if sys.platform.startswith('linux'):
        from OpenGL import GL
    global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
    app = QApplication(sys.argv)
    t = LoginWidget.TabWidget()
    t.show()
    #ex = Example()

    sys.exit(app.exec_())
