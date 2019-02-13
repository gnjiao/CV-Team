from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from Geometry.myLine import myLine
import math

class FindLineItem(QGraphicsItem):
    def __init__(self, line, parent=None):
        super(FindLineItem, self).__init__(parent)
        self.in_area=0
        self.start=line.start_point
        self.end=line.end_point
        self.line=line

        self.rect_count=8
        self.rects=list()
        self.rect_width=5
        self.rect_height=10
        self.generate_rect()

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable,True)
        #self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setAcceptHoverEvents(True)
        #self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.drawLine(self.line.start_point.x,self.line.start_point.y,self.line.end_point.x,self.line.end_point.y)
        for i in range(self.rect_count):
            self.draw_rect(painter,self.rects[i])

    def boundingRect(self):
        x_list = [self.rects[0].A.x,  self.rects[0].D.x, self.rects[-1].A.x, self.rects[-1].D.x]
        y_list = [self.rects[0].A.y,  self.rects[0].D.y, self.rects[-1].A.y, self.rects[-1].D.y]
        x_list.sort()
        y_list.sort()
        return QRectF(x_list[0]-5,y_list[0]-5,x_list[3]-x_list[0]+10,y_list[3]-y_list[0]+10)


    def shape(self):
        path = QPainterPath()
        points = list()
        points.append(QPointF(self.rects[0].A.x, self.rects[0].A.y))
        points.append(QPointF(self.rects[-1].B.x, self.rects[-1].B.y))
        points.append(QPointF(self.rects[-1].C.x, self.rects[-1].C.y))
        points.append(QPointF(self.rects[0].D.x, self.rects[0].D.y))
        points.append(QPointF(self.rects[0].A.x, self.rects[0].A.y))
        poly = QPolygonF(points)
        path.addPolygon(poly)
        return path

    def mousePressEvent(self, event):
        if self.is_in_area(event.pos(), self.line.start_point, 5):
            self.in_area=1
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), self.line.end_point, 5):
            self.in_area=2
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.rect_height/2-5<self.line.to_point(myPoint(event.pos().x(),event.pos().y()))<self.rect_height/2+5:
            self.in_area=3
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            self.in_area=0
            self.setFlag(QGraphicsItem.ItemIsMovable, True)

        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):


        if self.in_area==1:
            self.line=self.line.resize_by_start(myPoint(event.pos().x(),event.pos().y()))
            self.generate_rect()
            self.prepareGeometryChange()
            self.update()
        if self.in_area==2:
            self.line=self.line.resize_by_end(myPoint(event.pos().x(),event.pos().y()))
            self.generate_rect()
            self.prepareGeometryChange()
            self.update()
        if self.in_area==3:
            self.rect_height=self.line.to_point(myPoint(event.pos().x(),event.pos().y()))*2
            self.generate_rect()
            self.prepareGeometryChange()
            self.update()

        QGraphicsItem.mouseMoveEvent(self,event)

    def hoverMoveEvent(self, event):
        if self.is_in_area(event.pos(), self.line.start_point, 5) or self.is_in_area(event.pos(), self.line.end_point, 5) \
                or self.rect_height/2-5<self.line.to_point(myPoint(event.pos().x(),event.pos().y()))<self.rect_height/2+5:
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    # def wheelEvent(self,event):
    #     if event.delta() > 0:
    #         self.setScale(self.scale() * 1.1)
    #     else:
    #         self.setScale(self.scale()*0.9)
    #     QGraphicsItem.wheelEvent(self,event)

    def generate_rect(self):
        gap=self.line.length/(self.rect_count-1)
        self.rects.clear()
        for i in range(self.rect_count):
            self.rects.append(myRect(self.line.start_point+self.line.direction*gap*i,self.rect_width,self.rect_height,self.line.direction))


    @staticmethod
    def is_in_area(pos,other,tolerance):
        if math.sqrt(pow(other.x-pos.x(),2)+pow(other.y-pos.y(),2))<tolerance:
            return True
        else:
            return False





    @staticmethod
    def draw_rect(painter, rect):
        painter.drawLine(rect.A.x, rect.A.y, rect.B.x, rect.B.y)
        painter.drawLine(rect.B.x, rect.B.y, rect.C.x, rect.C.y)
        painter.drawLine(rect.C.x, rect.C.y, rect.D.x, rect.D.y)
        painter.drawLine(rect.D.x, rect.D.y, rect.A.x, rect.A.y)

        # painter.drawLine(A.x, A.y, B.x, B.y)
        #         # painter.drawLine(B.x, B.y, C.x, C.y)
        #         # painter.drawLine(C.x, C.y, D.x, D.y)
        #         # painter.drawLine(D.x, D.y, A.x, A.y)