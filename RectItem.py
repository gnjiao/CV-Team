from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class RectItem(QGraphicsItem):
    def __init__(self, center=0, width=0, height=0, direction=0, parent=None):
        super(RectItem, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setSelected(True)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 167, 183))
        painter.drawEllipse(0, 0, 90, 90)

    def boundingRect(self):
        return QRectF(0, 0, 95, 95)

    def mouseMoveEvent(self, event):
        print('this is item')
        QGraphicsItem.mouseMoveEvent(event)
    def hoverMoveEvent(self, event):
        print('this is item')
        QGraphicsItem.hoverMoveEvent(event)
