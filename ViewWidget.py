#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from View import View
from RectItem import RectItem
from Geometry.FindLineItem import FindLineItem
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
class ViewWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.image=None
        self.scene=QGraphicsScene()
        self.view=View(self)
        self.pix_map=None

        hbox=QHBoxLayout()
        vbox=QVBoxLayout()
        #适应屏幕按钮
        tool_button_fit=QToolButton(self)
        tool_button_fit.setIcon(QIcon(QPixmap('./image/cv_team.jpg')))
        hbox.addWidget(tool_button_fit)
        #放大缩小按钮
        tool_button_zoom_in=QToolButton(self)
        tool_button_zoom_in.setIcon(QIcon(QPixmap('./image/cv_team.jpg')))
        hbox.addWidget(tool_button_zoom_in)
        tool_button_zoom_out=QToolButton(self)
        tool_button_zoom_out.setIcon(QIcon(QPixmap('./image/cv_team.jpg')))
        hbox.addWidget(tool_button_zoom_out)

        #设置layout
        a=self.view.scene_pos.x()
        b='%d' %a
        label=QLabel('location label')
        label.setText(b)

        vbox.addWidget(self.view)
        hbox.addWidget(label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def set_image(self,image):
        pix_map_item = QGraphicsPixmapItem(QPixmap(img))
        self.scene.addItem(pix_map_item)
        #pix_map_item.setZValue(0)
        self.view.setScene(self.scene)
        #self.pix_map = QPixmap("./image/cv_team.jpg")

    def add_item(self,item):
        self.scene.addItem(item)
        #item.setZvalue(100)

if __name__=='__main__':
    app=QApplication(sys.argv)
    #window=ViewWidget()
    #window.show()
    point1 = myPoint(40, 50)
    width = 50
    height = 30
    dir = myPoint(3, 4)
    rect = myRect(point1, width, height, dir)
    rect_item = FindLineItem()#RectItem(rect)
    view_widget=ViewWidget()
    img=QImage("./image/cv_team.jpg")
    view_widget.set_image(img)
    view_widget.add_item(rect_item)
    view_widget.show()
    #window.resize(800,600)
    #window.showMaximized()
    app.exec()