# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'harfT.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import cv2
class Ui_Letter(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1270, 748)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(270, 10, 911, 531))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(570, 560, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(170, 650, 161, 51))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(330, 650, 161, 51))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")


        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.pushButton.clicked.connect(self.controlTimer)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Harf Tanıma"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "Başla"))
        self.label_2.setText(_translate("Form", "Tanımlanan Harfler : "))

    
    def viewCam(self):
        retOn, imageOn = self.cap.read()
        imageOn = cv2.cvtColor(imageOn, cv2.COLOR_BGR2RGB)
        heightOn, widthOn, channelOn = imageOn.shape
        stepOn = channelOn * widthOn
        qImgOn = QImage(imageOn.data, widthOn, heightOn, stepOn, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qImgOn))
    
    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            print("Dönüyor")
            self.timer.start(20)
            self.pushButton.setText("Durdur")
        else:
            self.timer.stop()
            self.cap.release()
            self.pushButton.setText("Başla")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Letter()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
