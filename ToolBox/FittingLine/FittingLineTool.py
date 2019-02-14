from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Geometry.myPoint import myPoint
from Geometry.myLine import myLine
from Geometry.myRect import myRect

from Widget.OperatorBaseWidget import OperatorBaseWidget
from Item.RectItem import RectItem
from Item.PointsItem import PointsItem

from Item.FindLineItem import FindLineItem
from ToolBox.FittingLine.FittingLineOperator import FittingLineOperator

from AuxiliaryFile.State import State
import sys
import cv2

class FittingLineTool(OperatorBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #数据部分
        self.state=State.Idle.value
        #self.rect= myRect(myPoint(40,40),10,20,myPoint(1,0))
        self.src_img=None
        self.line=myLine(myPoint(50,50),myPoint(100,100))
        self.line_item=FindLineItem(self.line)
        self.operator=FittingLineOperator()
        self.line_item.setZValue(100)
        self.points_item=None
        self.file_name=None
        self.rects=list()
        #界面部分
        self.setWindowTitle('Calliper Tool')
        group=QGroupBox('this group')
        vlay=QVBoxLayout()
        vlay.addWidget(group)
        self.base_data.setLayout(vlay)


        label=QLabel('this is label')
        label.setAlignment(Qt.AlignTop|Qt.AlignLeft)

        hlay=QHBoxLayout()
        input_label=QLabel('input image:')
        input_combobox=QComboBox()
        input_combobox.addItem('null')
        input_combobox.addItem('last')
        input_combobox.addItem('next')
        hlay.addWidget(input_label)
        hlay.addWidget(input_combobox)
        hlay.setAlignment(Qt.AlignTop)

        vlay1=QVBoxLayout()
        vlay1.addWidget(label)
        vlay1.addLayout(hlay)
        group.setLayout(vlay1)



        #连接信号与槽




        #
    #生成line_item矩形的角点坐标带入到计算中



    def on_load_image(self):
        file_name,_=QFileDialog.getOpenFileName(None,'载入图片',r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image",'Image files(*.jpg *.bmp *.jpeg)')
        if file_name :
            self.file_name=file_name
            if self.file_name is None:
                return
            qimg=QImage()
            qimg.load(self.file_name)
            self.view_widget.set_image(qimg)       #设置界面图片
            if qimg is None:
                return
            #self.view_widget.scene.removeItem(self.rect_item)
            if self.points_item is not None:
                self.view_widget.scene.removeItem(self.points_item)
            #self.rect=myRect(myPoint(qimg.width()/2,qimg.height()/2),qimg.width()/10,qimg.height()/10,myPoint(1,0))
            #self.rect_item=RectItem(self.rect)
            self.view_widget.scene.removeItem(self.line_item)
            self.line_item=FindLineItem(self.line)
            self.view_widget.add_item(self.line_item)

            cv_img=cv2.imread(self.file_name)
            self.operator.calliper.set_img(cv_img)  #设置卡尺图片


    def on_exec(self):
        self.rects=self.line_item.get_rects()
        self.operator.rects=self.rects
        self.operator.exec_fitting()
        print(self.operator.OK,self.operator.NG)

        # if self.points_item is not None:
        #     self.view_widget.scene.removeItem(self.points_item)
        # # if self.line is not None:
        # #     self.view_widget.scene.removeItem(self.line)
        # self.state=self.operator.calliper.exec_calliper()
        # if self.state != 0:
        #     #self.line=QGraphicsPointItem(self.calliper.points_out[0].x,self.calliper.points_out[0].y,self.calliper.points_out[1].x,self.calliper.points_out[1].y)
        #
        self.points_item=PointsItem(self.operator.OK)
        #     pen=QPen(Qt.red)
        #     # self.line.setPen(pen)
        #     # self.view_widget.add_item(self.line)
        self.view_widget.add_item(self.points_item)


    #槽函数定义
    # def on_add_item(self):
    #     self.rect_item.append(RectItem(self.rect))
    #     self.view_widget.add_item(self.rect_items[-1])
    #     self.rect_items[-1].setZValue(100)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Delete:
    #         for i in range(len(self.rect_items)):
    #             item = self.rect_items[i]
    #             if item.isSelected() is True:
    #                 self.selected_item = self.rect_items[i]
    #                 self.rect_items.remove(self.rect_items[i])
    #                 break
    #         self.view_widget.scene.removeItem(self.selected_item)


if __name__=='__main__':
    app = QApplication(sys.argv)
    fittingline = FittingLineTool()
    fittingline.resize(1000,750)
    fittingline.show()
    # img=QImage("../../image/cv_team.jpg")
    # calliper.view_widget.set_image(img)
    app.exec()