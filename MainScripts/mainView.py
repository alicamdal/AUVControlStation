from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMainWindow

from MainScripts.newCam import *
from MainScripts.cemberG import *
from MainScripts.harfT import *
from MainScripts.konumlanma import *
from MainScripts.escClass import *


manipState = False
Verticalvalue = 1000
ForwardValue = 1000
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.motors = ESC()
        
        self.timerOn = QTimer()
        self.timerOn.timeout.connect(self.viewCamOn)
        self.ui.pushButton.clicked.connect(self.controlTimer)
        self.ui.pushButton_3.clicked.connect(self.otonomCember)
        self.ui.pushButton_4.clicked.connect(self.otonomHarf)
        self.ui.pushButton_5.clicked.connect(self.otonomKonumlanma)


    def otonomKonumlanma(self):
        self.window = QMainWindow()
        self.ui = Ui_locate()
        self.ui.setupUi(self.window)
        self.window.show()

    def otonomHarf(self):
        self.window = QMainWindow()
        self.ui = Ui_Letter()
        self.ui.setupUi(self.window)
        self.window.show()

    def otonomCember(self):
        self.window = QMainWindow()
        self.ui = Ui_Circle()
        self.ui.setupUi(self.window)
        self.window.show()


    def viewCamOn(self):
        retOn, imageOn = self.capOn.read()
        imageOn = cv2.cvtColor(imageOn, cv2.COLOR_BGR2RGB)
        heightOn, widthOn, channelOn = imageOn.shape
        stepOn = channelOn * widthOn
        qImgOn = QImage(imageOn.data, widthOn, heightOn, stepOn, QImage.Format_RGB888)
        self.ui.label_11.setPixmap(QPixmap.fromImage(qImgOn))
    

    def controlTimer(self):
        if not self.timerOn.isActive():
            self.capOn = cv2.VideoCapture(0)
            print("Dönüyor")
            self.timerOn.start(20)
            self.ui.pushButton.setText("Durdur")
        else:
            self.timerOn.stop()
            self.capOn.release()
            self.ui.pushButton.setText("Başla")
    
    def keyPressEvent(self, event):
        global Verticalvalue
        global ForwardValue
        global manipState

        if event.key() == QtCore.Qt.Key_E:
            self.motors.up(speed=Verticalvalue)
        elif event.key() == QtCore.Qt.Key_Q:
            self.motors.down(speed=Verticalvalue)
        elif event.key() == QtCore.Qt.Key_W:
            self.motors.forward(speed=ForwardValue)
        elif event.key() == QtCore.Qt.Key_S:
            self.motors.stop()
        elif event.key() == QtCore.Qt.Key_A:
            self.motors.leftfor(speed=ForwardValue)
        elif event.key() == QtCore.Qt.Key_D:
            self.motors.rightfor(speed=ForwardValue)
        elif event.key() == QtCore.Qt.Key_Left:
            ForwardValue -= 145
            self.ui.progressBar.setValue(ForwardValue/14.5)
        elif event.key() == QtCore.Qt.Key_Right:
            ForwardValue += 145
            self.ui.progressBar.setValue(ForwardValue/14.5)
        elif event.key() == QtCore.Qt.Key_Up:
            Verticalvalue += 145
            self.ui.progressBar.setValue(Verticalvalue/14.5)
        elif event.key() == QtCore.Qt.Key_Down:
            Verticalvalue -= 145
            self.ui.progressBar.setValue(Verticalvalue/14.5)
        elif event.key() == QtCore.Qt.Key_F:
            if manipState is False:
                manipState = True
                self.ui.label_10.setText("Açık")
            else:
                manipState = False
                self.ui.label_10.setText("Kapalı")
        else:
            self.motors.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())