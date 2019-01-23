from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolBox.Calliper.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from Widget.OperatorBaseWidget import OperatorBaseWidget
from Item.RectItem import RectItem

import sys
import cv2

class CalliperTool(OperatorBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect=myRect(myPoint(40,40),20,10,myPoint(0.6,0.8))
        self.rect_item=RectItem(self.rect)
        self.rect_item.setZValue(100)
        self.view_widget.add_item(self.rect_item)
        self.rect_corn=list()
        self.rect_corn.append(self.rect.A)
        self.rect_corn.append(self.rect.B)
        self.rect_corn.append(self.rect.C)
        self.rect_corn.append(self.rect.D)
        self.selected_item=None
        self.line=None
        self.calliper = Calliper(self.rect_corn)

    def on_load_image(self):
        file_name,_=QFileDialog.getOpenFileName(None,'载入图片',r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image")
        img=QImage()
        cv_img=cv2.imread(file_name)
        self.calliper.src_img=cv_img
        self.calliper.convert()
        img.load(file_name)
        self.view_widget.set_image(img)
    # def on_add_item(self):
    #     self.rect_item.append(RectItem(self.rect))
    #     self.view_widget.add_item(self.rect_items[-1])
    #     self.rect_items[-1].setZValue(100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for i in range(len(self.rect_items)):
                item = self.rect_items[i]
                if item.isSelected() is True:
                    self.selected_item = self.rect_items[i]
                    self.rect_items.remove(self.rect_items[i])
                    break
            self.view_widget.scene.removeItem(self.selected_item)

    def on_exec(self):
        self.rect=self.rect_item.get_rect()
        print('rect:', self.rect.A.x, self.rect.A.y, self.rect.B.x, self.rect.B.y,
                            self.rect.C.x, self.rect.C.y, self.rect.D.x, self.rect.D.y)
        self.rect_corn.clear()
        self.rect_corn.append(self.rect.A)
        self.rect_corn.append(self.rect.B)
        self.rect_corn.append(self.rect.C)
        self.rect_corn.append(self.rect.D)

        if self.line is not None:
            self.view_widget.scene.removeItem(self.line)
        self.calliper.Exec()
        self.line=QGraphicsLineItem(self.calliper.points_out[0].x,self.calliper.points_out[0].y,self.calliper.points_out[1].x,self.calliper.points_out[1].y)
        pen=QPen(Qt.red)
        self.line.setPen(pen)
        self.view_widget.scene.addItem(self.line)
        self.update()



if __name__=='__main__':
    app = QApplication(sys.argv)
    calliper = CalliperTool()
    calliper.resize(1000,750)
    calliper.show()
    img=QImage("../../image/cv_team.jpg")
    calliper.view_widget.set_image(img)
    app.exec()