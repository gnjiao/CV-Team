from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class RectItem(QGraphicsItem):
    def __init__(self, rect, parent=None):
        super(RectItem, self).__init__(parent)
        self.rect=rect
        self.in_area=0

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)


    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 167, 183))
        painter.drawLine(self.rect.A.x, self.rect.A.y, self.rect.B.x, self.rect.B.y)
        painter.drawLine(self.rect.B.x, self.rect.B.y, self.rect.C.x, self.rect.C.y)
        painter.drawLine(self.rect.C.x, self.rect.C.y, self.rect.D.x, self.rect.D.y)
        painter.drawLine(self.rect.D.x, self.rect.D.y, self.rect.A.x, self.rect.A.y)


    def boundingRect(self):
        x_list=[self.rect.A.x,self.rect.B.x,self.rect.C.x,self.rect.D.x]
        y_list=[self.rect.A.y,self.rect.B.y,self.rect.C.y,self.rect.D.y]
        x_list.sort()
        y_list.sort()
        return QRectF(x_list[0]-5, y_list[0]-5, x_list[3]-x_list[0]+10, y_list[3]-y_list[0]+10)


    def mousePressEvent(self, event):
        pass

        QGraphicsItem.mousePressEvent(self, event)
    def mouseMoveEvent(self, event):
        print('mouse move')
        QGraphicsItem.mouseMoveEvent(self,event)
    def hoverMoveEvent(self, event):
        print(self.is_in_area(event.pos(), self.rect.A, 10),'is that in a')
        if self.is_in_area(event.pos(), self.rect.A, 5) or self.is_in_area(event.pos(), self.rect.B, 5) \
                or self.is_in_area(event.pos(), self.rect.C, 5) or self.is_in_area(event.pos(), self.rect.D, 5):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        QGraphicsItem.hoverMoveEvent(self,event)

    @staticmethod
    def is_in_area(pos,other,tolerance):
        if math.sqrt(pow(other.x-pos.x(),2)+pow(other.y-pos.y(),2))<tolerance:
            return True
        else:
            return False
