import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.button = QDoublePushButton("Test", self)
        self.button.clicked.connect(self.on_click)
        self.button.doubleClicked.connect(self.on_doubleclick)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.resize(120, 50)
        self.show()

    @pyqtSlot()
    def on_click(self):
        print("Click")

    @pyqtSlot()
    def on_doubleclick(self):
        print("Doubleclick")

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())