from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from Geometry.myLine import myLine
import math

class FindLineItem(QGraphicsItem):
    def __init__(self, start=myPoint(50,50),end=myPoint(146,50), parent=None):
        super(FindLineItem, self).__init__(parent)
        self.in_area=0
        self.start=start
        self.end=end
        self.line=myLine(self.start,self.end)

        self.rect_count=8
        self.rects=list()
        self.rect_width=5
        self.rect_height=10
        self.generate_rect()

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable,True)
        self.setAcceptHoverEvents(True)
        #self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.red)
        painter.setPen(pen)
        for i in range(self.rect_count):
            self.draw_rect(painter,self.rects[i])
        painter.drawLine(self.start.x,self.start.y,self.end.x,self.end.y)


    def boundingRect(self):
        x_list = [self.rects[0].A.x,  self.rects[0].D.x, self.rects[-1].A.x, self.rects[-1].D.x]
        y_list = [self.rects[0].A.y,  self.rects[0].D.y, self.rects[-1].A.y, self.rects[-1].D.y]
        x_list.sort()
        y_list.sort()
        return QRectF(x_list[0]-5,y_list[0]-5,x_list[3]-x_list[0]+10,y_list[3]-y_list[0]+10)

    def mousePressEvent(self, event):
        if self.is_in_area(event.pos(), self.start, 5):
            self.in_area=1
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        elif self.is_in_area(event.pos(), self.end, 5):
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

        # if self.in_area==1:
        #     self.rect=self.rect.resize_by_A(myPoint(event.pos().x(),event.pos().y()))
        #     self.prepareGeometryChange()
        #     self.update()
        # if self.in_area==2:
        #     self.rect=self.rect.resize_by_B(myPoint(event.pos().x(),event.pos().y()))
        #     self.prepareGeometryChange()
        #     self.update()
        # if self.in_area==3:
        #     self.rect=self.rect.resize_by_C(myPoint(event.pos().x(),event.pos().y()))
        #     self.prepareGeometryChange()
        #     self.update()
        # if self.in_area==4:
        #     self.rect=self.rect.resize_by_D(myPoint(event.pos().x(),event.pos().y()))
        #     self.prepareGeometryChange()
        #     self.update()
        # if self.in_area==5:
        #     self.rect = self.rect.rotate_to(myPoint(event.pos().x(), event.pos().y()))
        #     self.prepareGeometryChange()
        #     self.update()

        #print('mouse move')
        QGraphicsItem.mouseMoveEvent(self,event)

    def hoverMoveEvent(self, event):
        if self.is_in_area(event.pos(), self.start, 5) or self.is_in_area(event.pos(), self.end, 5):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)


    def generate_rect(self):
        gap=self.line.length/(self.rect_count-1)
        for i in range(self.rect_count):
            self.rects.append(myRect(myPoint(self.start.x+gap*i,self.start.y),self.rect_width,self.rect_height))
        print(self.rects.count(myRect))


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