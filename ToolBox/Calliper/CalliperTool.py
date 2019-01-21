from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolBox.Calliper.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from Widget.OperatorBaseWidget import OperatorBaseWidget
from Item.RectItem import RectItem

import sys
class CalliperTool(OperatorBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect=myRect(myPoint(50,50),100,50)
        self.rect_items=list()
        self.rect_items.append(RectItem(self.rect))
        self.view_widget.add_item(self.rect_items[0])
        rect_corn=list()
        rect_corn.append(self.rect_items[0].rect.A)
        rect_corn.append(self.rect_items[0].rect.B)
        rect_corn.append(self.rect_items[0].rect.C)
        rect_corn.append(self.rect_items[0].rect.D)
        self.calliper=Calliper(rect_corn)

        self.rect_items[0].setZValue(100)
        self.selected_item=None

    def on_load_image(self):
        file_name,_=QFileDialog.getOpenFileName(None,'载入图片',r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image")
        img=QImage()
        img.load(file_name)
        self.view_widget.set_image(img)

    def on_add_item(self):
        self.rect_items.append(RectItem(self.rect))
        self.view_widget.add_item(self.rect_items[-1])
        self.rect_items[-1].setZValue(100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for i in range(len(self.rect_items)):
                item = self.rect_items[i]
                if item.isSelected() is True:
                    self.selected_item = self.rect_items[i]
                    self.rect_items.remove(self.rect_items[i])
                    break
            self.view_widget.scene.removeItem(self.selected_item)



if __name__=='__main__':
    app = QApplication(sys.argv)
    calliper = CalliperTool()
    calliper.show()
    img=QImage("../../image/cv_team.jpg")
    calliper.view_widget.set_image(img)
    calliper.resize(800,600)

    app.exec()