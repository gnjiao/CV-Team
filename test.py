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

app = QApplication(sys.argv)


window = MainWindow()
# window.show()
# window.resize(800,600)
window.showMaximized()

app.exec()