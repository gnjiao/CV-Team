from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import sys
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        widget = QWidget(self,Qt.Widget)
        pushbutton = QPushButton(widget)
        pushbutton.setText('push')
        line_edit = QLineEdit(widget)
        label = QLabel(widget)
        label.setText('this is label')
        self.pushButton=QPushButton(self)
        self.pushButton.setGeometry(50,50,50,50)
        self.pushButton.setIcon(QIcon(".\image\cv_team.jpg"))
        self.pushButton.setStyleSheet("QPushButton{color:black}"
                                      #"QPushButton:hover{color:red}"
                                      "QPushButton{background-color:lightgreen}"
                                      #"QPushButton{border:2px}"
                                      #"QPushButton{border-radius:10px}"
                                      #"QPushButton{padding:2px 4px}"
        )

app = QApplication(sys.argv)


window = MainWindow()
# window.show()
# window.resize(800,600)
window.showMaximized()

app.exec()