# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cemberG.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
import cv2
from MainScripts.circleClass import Circle

state = True


class Ui_Circle(object):
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.pushButton.clicked.connect(self.controlTimer)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Çember Geçme"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "Başla"))

    def viewCam(self):
        global state
        
        if state == True:
            retOn, imageOn = self.cap.read()
            circles = circle.detect(imageOn)
            if circles is not None:
                x,y,r = circles
                if r != 0:
                    cv2.circle(imageOn, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(imageOn, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 2)
                    state = False

            imageOn = cv2.cvtColor(imageOn, cv2.COLOR_BGR2RGB)
            heightOn, widthOn, channelOn = imageOn.shape
            stepOn = channelOn * widthOn
            qImgOn = QImage(imageOn.data, widthOn, heightOn, stepOn, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qImgOn))

        else:
            #self.cap.release()
            #zaman = time.time()
            #while 1:
            #    if time.time() - zaman > 1:
            state = True
            #self.cap = cv2.VideoCapture(0)
            #        break
            #    else:
            #        pass

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
    circle = Circle()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Circle()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
