from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolBox.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect


class CalliperTool(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Rect=myRect(myPoint(50,50),100,50)


