from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PointsItem(QGraphicsItem):
    def __init__(self, points, parent=None):
        super(PointsItem, self).__init__(parent)
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        #self.setFlag(QGraphicsItem.ItemIsMovable,True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(100)
        self.points=points

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self.isSelected():
            painter.setPen(Qt.yellow)
        else:
            painter.setPen(Qt.red)
        for i in range(len(self.points)):
            painter.drawPoint(self.points[i].x,self.points[i].y)

    def boundingRect(self):
        x_list=list()
        y_list=list()
        for i in range(len(self.points)):
            x_list.append(self.points[i].x)
            y_list.append(self.points[i].y)
        x_list.sort()
        y_list.sort()
        return QRectF(x_list[0],y_list[0], x_list[-1]-x_list[0]+5,y_list[-1]-y_list[0]+5)
    # def shape(self):
    #     path=QPainterPath()
    #     return path

