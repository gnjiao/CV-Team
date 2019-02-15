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
        self.setWindowTitle('FittingLine Tool')
        #基础数据部分

        self.set_base_data()

        #Item 部分设置
        self.set_item()

        #结果数据部分
        self.output_result()
        #连接信号与槽




    #生成line_item矩形的角点坐标带入到计算中
    # 界面的基础数据部分
    def set_base_data(self):
        label = QLabel('this is test label')
        img_setting_gb= QGroupBox('image setting')
        img_setting_gb.setMaximumHeight(100)

        hlay=QHBoxLayout()
        input_label = QLabel('input image:')
        input_combobox = QComboBox()
        input_combobox.addItem('null')
        input_combobox.addItem('last')
        input_combobox.addItem('next')
        hlay.addWidget(input_label)
        hlay.addWidget(input_combobox)
        hlay.setAlignment(Qt.AlignVCenter)
        img_setting_gb.setLayout(hlay)


        calliper_para_gb = QGroupBox('Calliper Parameter')


        calliper_width_sl=QSlider()
        calliper_width_sl.setOrientation(Qt.Horizontal)
        calliper_width_sl.setMinimum(5)
        calliper_width_sl.setMaximum(30)
        calliper_width_sl.setValue(12)

        calliper_width_sb=QSpinBox()
        calliper_width_sb.setMinimum(5)
        calliper_width_sb.setMaximum(30)
        calliper_width_sb.setValue(12)


        hlay_calliper_width=QHBoxLayout()
        hlay_calliper_width.addWidget(calliper_width_sl)
        hlay_calliper_width.addWidget(calliper_width_sb)

        calliper_width_gb=QGroupBox('Calliper Width')
        calliper_width_gb.setLayout(hlay_calliper_width)

        #上面是calliper width 的相关设置，下面是calliper height 的相关设置
        calliper_height_sl=QSlider()
        calliper_height_sl.setOrientation(Qt.Horizontal)
        calliper_height_sl.setMinimum(5)
        calliper_height_sl.setMaximum(30)
        calliper_height_sl.setValue(12)

        calliper_height_sb=QSpinBox()
        calliper_height_sb.setMinimum(5)
        calliper_height_sb.setMaximum(30)
        calliper_height_sb.setValue(12)

        hlay_calliper_height=QHBoxLayout()
        hlay_calliper_height.addWidget(calliper_height_sl)
        hlay_calliper_height.addWidget(calliper_height_sb)
        calliper_height_gb=QGroupBox('Calliper Height')
        calliper_height_gb.setLayout(hlay_calliper_height)

        #分界线-------------------------------------------
        calliper_thresh_sl = QSlider()
        calliper_thresh_sl.setOrientation(Qt.Horizontal)
        calliper_thresh_sl.setMinimum(5)
        calliper_thresh_sl.setMaximum(50)
        calliper_thresh_sl.setValue(30)

        calliper_thresh_sb = QSpinBox()
        calliper_thresh_sb.setMinimum(5)
        calliper_thresh_sb.setMaximum(50)
        calliper_thresh_sb.setValue(30)

        hlay_calliper_thresh = QHBoxLayout()
        hlay_calliper_thresh.addWidget(calliper_thresh_sl)
        hlay_calliper_thresh.addWidget(calliper_thresh_sb)
        calliper_thresh_gb = QGroupBox('Calliper Threshold')
        calliper_thresh_gb.setLayout(hlay_calliper_thresh)


        calliper_polar_gb = QGroupBox('Polar')
        polar_cb=QComboBox()
        hlay_polar_cb=QHBoxLayout()
        hlay_polar_cb.addWidget(polar_cb)
        calliper_polar_gb.setLayout(hlay_polar_cb)

        calliper_result_type_gb = QGroupBox('Result Type')
        result_type_cb=QComboBox()
        hlay_result_type_cb=QHBoxLayout()
        hlay_result_type_cb.addWidget(result_type_cb)
        calliper_result_type_gb.setLayout(hlay_result_type_cb)

        hlay1=QHBoxLayout()
        hlay1.addWidget(calliper_polar_gb)
        hlay1.addWidget(calliper_result_type_gb)

        #以下是最外层groupbox 的设置
        vlay_calliper_para = QVBoxLayout()
        vlay_calliper_para.addLayout(hlay1)
        vlay_calliper_para.addWidget(calliper_width_gb)
        vlay_calliper_para.addWidget(calliper_height_gb)
        vlay_calliper_para.addWidget(calliper_thresh_gb)


        calliper_para_gb.setLayout(vlay_calliper_para)




        line_para_gb = QGroupBox('Line Parameter')
        hlay = QHBoxLayout()
        vlay=QVBoxLayout()
        vlay.addWidget(img_setting_gb)
        vlay.addWidget(calliper_para_gb)
        vlay.addWidget(line_para_gb)
        self.base_data.setLayout(vlay)

    def set_item(self):
        vlay = QVBoxLayout()
        item_setting_gb = QGroupBox('Item setting')
        #item_setting_gb.setMaximumHeight(250)
        vlay.addWidget(item_setting_gb)
        hlay = QHBoxLayout()
        start_point_lb = QLabel('Start Point:')
        start_point_x_le = QLineEdit()
        start_point_y_le = QLineEdit()
        hlay.addWidget(start_point_lb)
        hlay.addWidget(start_point_x_le)
        hlay.addWidget(start_point_y_le)

        hlay1 = QHBoxLayout()
        end_point_lb = QLabel('End   Point:')
        hlay1.addWidget(end_point_lb)
        end_point_x_le = QLineEdit()
        end_point_y_le = QLineEdit()
        hlay1.addWidget(end_point_x_le)
        hlay1.addWidget(end_point_y_le)
        comfirm_pb=QPushButton('confirm')

        horizontal_rb = QRadioButton(' Horizontal')
        vertical_rb = QRadioButton(' Vertical')
        degree45_rb = QRadioButton(' 45 Degree')
        degree_45_rb = QRadioButton(' -45 Degree')

        vlay3 = QVBoxLayout()
        vlay3.addLayout(hlay)
        vlay3.addLayout(hlay1)
        vlay3.addWidget(comfirm_pb)
        vlay3.addWidget(horizontal_rb)
        vlay3.addWidget(vertical_rb)
        vlay3.addWidget(degree45_rb)
        vlay3.addWidget(degree_45_rb)
        item_setting_gb.setLayout(vlay3)
        self.item_setting.setLayout(vlay)

        result_display_gb = QGroupBox('Result display')
        self.calliper_cb = QCheckBox(' Find Line Item')
        self.result_line_cb = QCheckBox(' Result Line')
        self.ok_points_cb = QCheckBox(' OK Points')
        self.ng_points_cb = QCheckBox(' NG Points')
        select_all = QCheckBox(' Select All')
        select_all.stateChanged.connect(self.on_select_all)

        vlay2 = QVBoxLayout()
        vlay2.addWidget(self.calliper_cb)
        vlay2.addWidget(self.result_line_cb)
        vlay2.addWidget(self.ok_points_cb)
        vlay2.addWidget(self.ng_points_cb)
        vlay2.addWidget(select_all)
        result_display_gb.setLayout(vlay2)
        vlay.addWidget(result_display_gb)

    def output_result(self):
        vlay = QVBoxLayout()
        line_result_gb = QGroupBox('Line result')
        line_result_gb.setMinimumHeight(400)
        function_word_lb=QLabel('Line Function: ')
        function_lb=QLabel('y = kx + b')
        function_lb.setFrameStyle(QFrame.Panel)
        function_lb.setMaximumHeight(25)
        function_lb.setFrameShadow(QFrame.Sunken)
        function_lb.setStyleSheet(
            "QLabel{background-color:lightgray}"
        )

        hlay_xy=QHBoxLayout()
        space_lb=QLabel('            ')
        x_lb=QLabel('X')
        x_lb.setAlignment(Qt.AlignCenter)
        y_lb=QLabel('Y')
        y_lb.setAlignment(Qt.AlignCenter)
        hlay_xy.addWidget(space_lb)
        hlay_xy.addWidget(x_lb)
        hlay_xy.addWidget(y_lb)


        start_point_lb=QLabel('Start Point:')
        end_point_lb=QLabel('End   Point:')
        mid_point_lb=QLabel('Mid   Point:')
        start_point_x_lb=QLabel('shuzi')
        start_point_y_lb=QLabel('shuzi')
        start_point_x_lb.setFrameStyle(QFrame.Panel)
        start_point_x_lb.setMaximumHeight(25)
        start_point_x_lb.setFrameShadow(QFrame.Sunken)
        start_point_x_lb.setStyleSheet("QLabel{background-color:lightgray}")

        start_point_y_lb.setFrameStyle(QFrame.Panel)
        start_point_y_lb.setMaximumHeight(25)
        start_point_y_lb.setFrameShadow(QFrame.Sunken)
        start_point_y_lb.setStyleSheet("QLabel{background-color:lightgray}")

        mid_point_x_lb=QLabel('shuzi')
        mid_point_y_lb=QLabel('shuzi')
        mid_point_x_lb.setFrameStyle(QFrame.Panel)
        mid_point_x_lb.setMaximumHeight(25)
        mid_point_x_lb.setFrameShadow(QFrame.Sunken)
        mid_point_x_lb.setStyleSheet("QLabel{background-color:lightgray}")

        mid_point_y_lb.setFrameStyle(QFrame.Panel)
        mid_point_y_lb.setMaximumHeight(25)
        mid_point_y_lb.setFrameShadow(QFrame.Sunken)
        mid_point_y_lb.setStyleSheet("QLabel{background-color:lightgray}")

        end_point_x_lb=QLabel('shuzi')
        end_point_y_lb=QLabel('shuzi')
        end_point_x_lb.setFrameStyle(QFrame.Panel)
        end_point_x_lb.setMaximumHeight(25)
        end_point_x_lb.setFrameShadow(QFrame.Sunken)
        end_point_x_lb.setStyleSheet("QLabel{background-color:lightgray}")

        end_point_y_lb.setFrameStyle(QFrame.Panel)
        end_point_y_lb.setMaximumHeight(25)
        end_point_y_lb.setFrameShadow(QFrame.Sunken)
        end_point_y_lb.setStyleSheet("QLabel{background-color:lightgray}")

        length_word_lb=QLabel('Length     :')
        length_lb = QLabel('100')
        length_lb.setMinimumWidth(153)
        length_lb.setFrameStyle(QFrame.Panel)
        length_lb.setMaximumHeight(25)
        length_lb.setFrameShadow(QFrame.Sunken)
        length_lb.setStyleSheet("QLabel{background-color:lightgray}")

        degree_word_lb=QLabel('Degree     :')
        degree_lb = QLabel('100')
        degree_lb.setMinimumWidth(153)
        degree_lb.setFrameStyle(QFrame.Panel)
        degree_lb.setMaximumHeight(25)
        degree_lb.setFrameShadow(QFrame.Sunken)
        degree_lb.setStyleSheet("QLabel{background-color:lightgray}")

        hlay_start=QHBoxLayout()
        hlay_start.addWidget(start_point_lb)
        hlay_start.addWidget(start_point_x_lb)
        hlay_start.addWidget(start_point_y_lb)

        hlay_end=QHBoxLayout()
        hlay_end.addWidget(end_point_lb)
        hlay_end.addWidget(end_point_x_lb)
        hlay_end.addWidget(end_point_y_lb)

        hlay_mid=QHBoxLayout()
        hlay_mid.addWidget(mid_point_lb)
        hlay_mid.addWidget(mid_point_x_lb)
        hlay_mid.addWidget(mid_point_y_lb)

        hlay_length=QHBoxLayout()
        hlay_length.addWidget(length_word_lb)
        hlay_length.addWidget(length_lb)

        hlay_degree=QHBoxLayout()
        hlay_degree.addWidget(degree_word_lb)
        hlay_degree.addWidget(degree_lb)

        ok_point_lb=QLabel('number of ok points:')
        ng_point_lb = QLabel('number of ng points:')
        ok_number_lb=QLabel('99')

        ok_number_lb.setFrameStyle(QFrame.Panel)
        ok_number_lb.setMaximumHeight(25)
        ok_number_lb.setFrameShadow(QFrame.Sunken)
        ok_number_lb.setStyleSheet("QLabel{background-color:lightgray}")

        ng_number_lb=QLabel('99')
        #ng_number_lb.setMaximumWidth(60)
        ng_number_lb.setFrameStyle(QFrame.Panel)
        ng_number_lb.setMaximumHeight(25)
        ng_number_lb.setFrameShadow(QFrame.Sunken)
        ng_number_lb.setStyleSheet("QLabel{background-color:lightgray}")

        hlay_ok=QHBoxLayout()
        hlay_ng=QHBoxLayout()
        hlay_ok.addWidget(ok_point_lb)
        hlay_ok.addWidget(ok_number_lb)

        hlay_ng.addWidget(ng_point_lb)
        hlay_ng.addWidget(ng_number_lb)


        vlay1=QVBoxLayout()
        vlay1.addWidget(function_word_lb)
        vlay1.addWidget(function_lb)
        vlay1.addLayout(hlay_xy)
        vlay1.addLayout(hlay_start)
        vlay1.addLayout(hlay_mid)
        vlay1.addLayout(hlay_end)
        hlay_space=QHBoxLayout()
        hlay_space.addWidget(space_lb)
        vlay1.addLayout(hlay_space)
        vlay1.addLayout(hlay_length)
        vlay1.addLayout(hlay_degree)
        vlay1.addLayout(hlay_ok)
        vlay1.addLayout(hlay_ng)
        line_result_gb.setLayout(vlay1)


        judgment_gb = QGroupBox('Parameter judgment')
        vlay_jug=QVBoxLayout()
        hlay_start = QHBoxLayout()
        start_point_cb = QCheckBox('Start Point:')
        start_point_x_le = QLineEdit()
        start_point_y_le = QLineEdit()
        start_point_x_le.setDisabled(True)
        start_point_y_le.setDisabled(True)
        hlay_start.addWidget(start_point_cb)
        hlay_start.addWidget(start_point_x_le)
        hlay_start.addWidget(start_point_y_le)

        hlay_end = QHBoxLayout()
        end_point_cb = QCheckBox('End   Point:')
        hlay_end.addWidget(end_point_cb)
        end_point_x_le = QLineEdit()
        end_point_y_le = QLineEdit()
        end_point_x_le.setDisabled(True)
        end_point_y_le.setDisabled(True)
        hlay_end.addWidget(end_point_x_le)
        hlay_end.addWidget(end_point_y_le)

        hlay_degree = QHBoxLayout()
        end_point_cb = QCheckBox('Degree:')
        hlay_degree.addWidget(end_point_cb)
        degree_le = QLineEdit()
        degree_le.setDisabled(True)
        hlay_degree.addWidget(degree_le)
        vlay_jug.addLayout(hlay_start)
        vlay_jug.addLayout(hlay_end)
        vlay_jug.addLayout(hlay_degree)

        judgment_gb.setLayout(vlay_jug)

        vlay.addWidget(line_result_gb)
        vlay.addWidget(judgment_gb)

        self.output.setLayout(vlay)

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
    def on_select_all(self,state):
        if state==Qt.Checked:
            self.calliper_cb.setChecked(True)
            self.result_line_cb.setChecked(True)
            self.ok_points_cb.setChecked(True)
            self.ng_points_cb.setChecked(True)
        else:
            self.calliper_cb.setChecked(False)
            self.result_line_cb.setChecked(False)
            self.ok_points_cb.setChecked(False)
            self.ng_points_cb.setChecked(False)

if __name__=='__main__':
    app = QApplication(sys.argv)
    fittingline = FittingLineTool()
    fittingline.resize(1000,750)
    fittingline.show()
    # img=QImage("../../image/cv_team.jpg")
    # calliper.view_widget.set_image(img)
    app.exec()

