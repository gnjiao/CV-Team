#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from View import View
from RectItem import RectItem
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
class ViewWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        #设置layout
        hbox=QHBoxLayout()
        vbox=QVBoxLayout()

        label=QLabel('this is msg label')


        scene=QGraphicsScene()
        view = View(self)
        print('ok')
        self.pixmap = QPixmap("./image/cv_team.jpg")

        pixmap_item=QGraphicsPixmapItem(QPixmap('./image/cv_team.jpg'))
        scene.addItem(pixmap_item)

        point1=myPoint(40,50)
        width=50
        height=30
        dir=myPoint(3,4)
        rect=myRect(point1,width,height,dir)
        rect_item=RectItem(rect)
        scene.addItem(rect_item)


        view.setScene(scene)
        vbox.addWidget(view)
        hbox.addWidget(label)
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

        #
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        a=view.scene_pos.x()
        b='%d' %a
        label.setText(b)

        #设置







app=QApplication(sys.argv)
window=ViewWidget()
window.show()
#window.resize(800,600)
#window.showMaximized()
app.exec()