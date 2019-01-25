from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
import math

class RectItem(QGraphicsItem):
    def __init__(self, rect, parent=None):
        super(RectItem, self).__init__(parent)
        self.rect=rect
        self.in_area=0

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable,True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)
        #self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self.isSelected():
            painter.setPen(Qt.yellow)
        else:
            painter.setPen(Qt.red)
        painter.drawLine(self.rect.A.x, self.rect.A.y, self.rect.B.x, self.rect.B.y)
        painter.drawLine(self.rect.B.x, self.rect.B.y, self.rect.C.x, self.rect.C.y)
        painter.drawLine(self.rect.C.x, self.rect.C.y, self.rect.D.x, self.rect.D.y)
        painter.drawLine(self.rect.D.x, self.rect.D.y, self.rect.A.x, self.rect.A.y)
        BC=(self.rect.B+self.rect.C)/2
        p=QPointF(BC.x,BC.y)
        painter.drawEllipse(p,5,5)

    def boundingRect(self):
        x_list=[self.rect.A.x,self.rect.B.x,self.rect.C.x,self.rect.D.x]
        y_list=[self.rect.A.y,self.rect.B.y,self.rect.C.y,self.rect.D.y]
        x_list.sort()
        y_list.sort()
        return QRectF(x_list[0]-5, y_list[0]-5, x_list[3]-x_list[0]+10, y_list[3]-y_list[0]+10)
    def shape(self):
        path=QPainterPath()
        points=list()
        points.append(QPointF(self.rect.A.x, self.rect.A.y))
        points.append(QPointF(self.rect.B.x, self.rect.B.y))
        points.append(QPointF(self.rect.C.x, self.rect.C.y))
        points.append(QPointF(self.rect.D.x, self.rect.D.y))
        points.append(QPointF(self.rect.A.x, self.rect.A.y))
        poly=QPolygonF(points)
        path.addPolygon(poly)
        return path

    def mousePressEvent(self, event):
        if self.is_in_area(event.pos(), self.rect.A, 5):
            self.in_area=1
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), self.rect.B, 5):
            self.in_area=2
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), self.rect.C, 5):
            self.in_area=3
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), self.rect.D, 5):
            self.in_area=4
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), (self.rect.B+self.rect.C)/2, 10):
            self.in_area=5
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            self.in_area=0
            self.setFlag(QGraphicsItem.ItemIsMovable, True)

        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):

        if self.in_area==1:
            self.rect=self.rect.resize_by_A(myPoint(event.pos().x(),event.pos().y()))
            self.prepareGeometryChange()
            self.update()
        if self.in_area==2:
            self.rect=self.rect.resize_by_B(myPoint(event.pos().x(),event.pos().y()))
            self.prepareGeometryChange()
            self.update()
        if self.in_area==3:
            self.rect=self.rect.resize_by_C(myPoint(event.pos().x(),event.pos().y()))
            self.prepareGeometryChange()
            self.update()
        if self.in_area==4:
            self.rect=self.rect.resize_by_D(myPoint(event.pos().x(),event.pos().y()))
            self.prepareGeometryChange()
            self.update()
        if self.in_area==5:
            self.rect = self.rect.rotate_to(myPoint(event.pos().x(), event.pos().y()))
            self.prepareGeometryChange()
            self.update()
        QGraphicsItem.mouseMoveEvent(self,event)

    def hoverMoveEvent(self, event):
        if self.is_in_area(event.pos(), self.rect.A, 5) or self.is_in_area(event.pos(), self.rect.B, 5) \
                or self.is_in_area(event.pos(), self.rect.C, 5) or self.is_in_area(event.pos(), self.rect.D, 5):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        QGraphicsItem.hoverMoveEvent(self,event)

    def get_rect(self):
        center_=self.rect.center
        scene_center=self.mapToScene(QPointF(center_.x,center_.y))
        return myRect(myPoint(scene_center.x(),scene_center.y()),self.rect.width,self.rect.height,self.rect.direction)

    @staticmethod
    def is_in_area(pos,other,tolerance):
        if math.sqrt(pow(other.x-pos.x(),2)+pow(other.y-pos.y(),2))<tolerance:
            return True
        else:
            return False
