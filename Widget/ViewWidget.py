#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from Widget.View import View
from Item.RectItem import RectItem

from Geometry.FindLineItem import FindLineItem
from Geometry.myLine import myLine
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect

class ViewWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.image=None
        self.scene=QGraphicsScene()
        self.view=View(self)
        self.pix_map=None
        self.pix_map_item = None
        hbox=QHBoxLayout()
        vbox=QVBoxLayout()

        #适应屏幕按钮
        tool_button_fit=QToolButton(self)
        tool_button_fit.setIcon(QIcon(QPixmap("C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.jpg")))
        tool_button_fit.clicked.connect(self.fit)
        hbox.addWidget(tool_button_fit)

        #放大缩小按钮
        tool_button_zoom_in=QToolButton(self)
        tool_button_zoom_in.setIcon(QIcon(QPixmap("C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.jpg")))
        hbox.addWidget(tool_button_zoom_in)
        tool_button_zoom_in.clicked.connect(self.zoom_in)

        tool_button_zoom_out=QToolButton(self)
        tool_button_zoom_out.setIcon(QIcon(QPixmap("C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.jpg")))
        hbox.addWidget(tool_button_zoom_out)
        tool_button_zoom_out.clicked.connect(self.zoom_out)

        #设置layout
        self.label=QLabel('location label')
        self.label.setAlignment(Qt.AlignRight)
        self.label.setText('x=0      y=0   ')

        vbox.addWidget(self.view)
        hbox.addWidget(self.label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # self.setStyleSheet(
        #     "QWidget{color:black}"
        #     "QWidget:hover{color:red}"
        #     "QWidget{background-color:lightgray}"
        #     "QWidget{border:0px}"
        #     "QWidget{border-radius:5px}"
        # )


        #信号与槽函数
        self.view.signal_mouse_move[int,int].connect(self.on_mouse_move)

    def set_image(self,image):
        self.scene.removeItem(self.pix_map_item)
        self.pix_map_item = QGraphicsPixmapItem(QPixmap(image))
        self.scene.addItem(self.pix_map_item)
        self.pix_map_item.setPos(0,0)
        self.scene.setSceneRect(-10,-10,self.pix_map_item.pixmap().width()+20,self.pix_map_item.pixmap().height()+20)
        self.view.setScene(self.scene)
        print(self.view.viewport().width(),self.view.viewport().height())
        self.adapt_window()
        #self.pix_map = QPixmap("./image/cv_team.jpg")

    def add_item(self,item):
        self.scene.addItem(item)
        #item.setZvalue(100)
    def fit(self):
        self.adapt_window()
        self.repaint()
    def zoom_in(self):
        self.view.on_zoom_in(6)
        self.repaint()
    def zoom_out(self):
        self.view.on_zoom_out(6)
        self.repaint()
    def on_mouse_move(self,val1,val2):
        a=val1
        a_='%d' %a
        b=val2
        b_='%d' %b
        self.label.setText('x = '+a_+'   '+'y = '+b_)
    def adapt_window(self):
        trans = QTransform()
        scale=pow(2,(self.view.zoom_slider.value()-250)*0.02)
        scene_rect=self.scene.sceneRect()
        x_ration=self.view.viewport().width()/scene_rect.width()
        y_ration=self.view.viewport().height()/scene_rect.height()
        if x_ration<y_ration:
            y_ration=x_ration
        trans.scale(y_ration,y_ration)
        self.view.reset_view()
        self.view.setTransform(trans)


if __name__=='__main__':
    app=QApplication(sys.argv)
    #window=ViewWidget()
    #window.show()
    point1 = myPoint(40, 50)
    width = 50
    height = 30
    dir = myPoint(3, 4)
    rect = myRect(point1, width, height, dir)
    line=myLine(myPoint(50,50),myPoint(146,50))
    rect_item = RectItem(rect)#RectItem(rect)
    view_widget=ViewWidget()
    img=QImage("../image/cv_team.jpg")
    view_widget.set_image(img)
    view_widget.add_item(rect_item)
    view_widget.show()
    view_widget.resize(800,600)
    #window.showMaximized()
    app.exec()