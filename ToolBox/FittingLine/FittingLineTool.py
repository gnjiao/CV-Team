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
        #界面部分
        self.setWindowTitle('FittingLine Tool')
        #基础数据部分
        self.set_base_data()

        #Item 部分设置
        self.set_item()

        #结果数据部分
        self.output_result()
        #连接信号与槽

        # 数据部分
        self.state = State.Idle.value
        # self.rect= myRect(myPoint(40,40),10,20,myPoint(1,0))
        self.src_img = None
        self.line = myLine(myPoint(50, 50), myPoint(150, 150))
        self.line_item = FindLineItem(self.line)
        self.operator = FittingLineOperator()
        self.line_item.setZValue(100)
        self.points_item = None
        self.file_name = None
        self.rects = list()
        self.connect_UI()


    #生成line_item矩形的角点坐标带入到计算中
    # 界面的基础数据部分
    def set_base_data(self):
        img_setting_gb= QGroupBox('image setting')
        img_setting_gb.setMaximumHeight(70)

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


        self.calliper_width_sl=QSlider()
        self.calliper_width_sl.setOrientation(Qt.Horizontal)
        self.calliper_width_sl.setMinimum(5)
        self.calliper_width_sl.setMaximum(30)
        self.calliper_width_sl.setValue(12)

        self.calliper_width_sb=QSpinBox()
        self.calliper_width_sb.setMinimum(5)
        self.calliper_width_sb.setMaximum(30)
        self.calliper_width_sb.setValue(12)
        self.calliper_width_sl.valueChanged.connect(self.on_width_sl_change)
        self.calliper_width_sb.valueChanged.connect(self.on_width_sb_change)

        hlay_calliper_width=QHBoxLayout()
        hlay_calliper_width.addWidget(self.calliper_width_sl)
        hlay_calliper_width.addWidget(self.calliper_width_sb)

        calliper_width_gb=QGroupBox('Calliper Width')
        calliper_width_gb.setLayout(hlay_calliper_width)

        #上面是calliper width 的相关设置，下面是calliper height 的相关设置
        self.calliper_height_sl=QSlider()
        self.calliper_height_sl.setOrientation(Qt.Horizontal)
        self.calliper_height_sl.setMinimum(5)
        self.calliper_height_sl.setMaximum(30)
        self.calliper_height_sl.setValue(12)

        self.calliper_height_sb=QSpinBox()
        self.calliper_height_sb.setMinimum(5)
        self.calliper_height_sb.setMaximum(30)
        self.calliper_height_sb.setValue(12)
        self.calliper_height_sl.valueChanged.connect(self.on_height_sl_change)
        self.calliper_height_sb.valueChanged.connect(self.on_height_sb_change)

        hlay_calliper_height=QHBoxLayout()
        hlay_calliper_height.addWidget(self.calliper_height_sl)
        hlay_calliper_height.addWidget(self.calliper_height_sb)
        calliper_height_gb=QGroupBox('Calliper Height')
        calliper_height_gb.setLayout(hlay_calliper_height)

        #分界线-------------------------------------------
        self.calliper_thresh_sl = QSlider()
        self.calliper_thresh_sl.setOrientation(Qt.Horizontal)
        self.calliper_thresh_sl.setMinimum(5)
        self.calliper_thresh_sl.setMaximum(50)
        self.calliper_thresh_sl.setValue(30)

        self.calliper_thresh_sb = QSpinBox()
        self.calliper_thresh_sb.setMinimum(5)
        self.calliper_thresh_sb.setMaximum(50)
        self.calliper_thresh_sb.setValue(30)

        self.calliper_thresh_sl.valueChanged.connect(self.on_thresh_sl_change)
        self.calliper_thresh_sb.valueChanged.connect(self.on_thresh_sb_change)

        hlay_calliper_thresh = QHBoxLayout()
        hlay_calliper_thresh.addWidget(self.calliper_thresh_sl)
        hlay_calliper_thresh.addWidget(self.calliper_thresh_sb)
        calliper_thresh_gb = QGroupBox('Calliper Threshold')
        calliper_thresh_gb.setLayout(hlay_calliper_thresh)


        calliper_polar_gb = QGroupBox('Polar')
        self.polar_cb=QComboBox()
        hlay_polar_cb=QHBoxLayout()
        hlay_polar_cb.addWidget(self.polar_cb)
        calliper_polar_gb.setLayout(hlay_polar_cb)

        calliper_result_type_gb = QGroupBox('Result Type')
        self.result_type_cb=QComboBox()
        hlay_result_type_cb=QHBoxLayout()
        hlay_result_type_cb.addWidget(self.result_type_cb)
        calliper_result_type_gb.setLayout(hlay_result_type_cb)

        hlay1=QHBoxLayout()
        hlay1.addWidget(calliper_polar_gb)
        hlay1.addWidget(calliper_result_type_gb)

        #以下是最外层groupbox 的设置
        vlay_calliper_para = QVBoxLayout()
        vlay_calliper_para.addLayout(hlay1)
        vlay_calliper_para.addWidget(calliper_thresh_gb)
        vlay_calliper_para.addWidget(calliper_width_gb)
        vlay_calliper_para.addWidget(calliper_height_gb)

        calliper_para_gb.setLayout(vlay_calliper_para)

        #分界
        line_para_gb = QGroupBox('Line Parameter')
        vlay_line_para=QVBoxLayout()

        self.iterate_count_sl = QSlider()
        self.iterate_count_sl.setOrientation(Qt.Horizontal)
        self.iterate_count_sl.setMinimum(5)
        self.iterate_count_sl.setMaximum(50)
        self.iterate_count_sl.setValue(30)

        self.iterate_count_sb = QSpinBox()
        self.iterate_count_sb.setMinimum(5)
        self.iterate_count_sb.setMaximum(50)
        self.iterate_count_sb.setValue(30)

        self.iterate_count_sl.valueChanged.connect(self.on_iterate_sl_change)
        self.iterate_count_sb.valueChanged.connect(self.on_iterate_sb_change)

        hlay_iterate_count = QHBoxLayout()
        hlay_iterate_count.addWidget(self.iterate_count_sl)
        hlay_iterate_count.addWidget(self.iterate_count_sb)
        iterate_count_gb = QGroupBox('Iterate Count')
        iterate_count_gb.setLayout(hlay_iterate_count)

        #上面部分是迭代次数代码
        #下面部分是卡尺数量设置代码
        self.calliper_count_sl = QSlider()
        self.calliper_count_sl.setOrientation(Qt.Horizontal)
        self.calliper_count_sl.setMinimum(5)
        self.calliper_count_sl.setMaximum(99)
        self.calliper_count_sl.setValue(12)

        self.calliper_count_sb = QSpinBox()
        self.calliper_count_sb.setMinimum(5)
        self.calliper_count_sb.setMaximum(99)
        self.calliper_count_sb.setValue(12)

        self.calliper_count_sl.valueChanged.connect(self.on_calliper_count_sl_change)
        self.calliper_count_sb.valueChanged.connect(self.on_calliper_count_sb_change)

        hlay_calliper_count = QHBoxLayout()
        hlay_calliper_count.addWidget(self.calliper_count_sl)
        hlay_calliper_count.addWidget(self.calliper_count_sb)
        calliper_count_gb = QGroupBox('Calliper Count')
        calliper_count_gb.setLayout(hlay_calliper_count)

        #上面是卡尺数量代码
        #下面是距离阈值代码
        self.dist_thresh_sl = QSlider()
        self.dist_thresh_sl.setOrientation(Qt.Horizontal)
        self.dist_thresh_sl.setMinimum(1)
        self.dist_thresh_sl.setMaximum(20)
        self.dist_thresh_sl.setValue(5)

        self.dist_thresh_sb = QSpinBox()
        self.dist_thresh_sb.setMinimum(1)
        self.dist_thresh_sb.setMaximum(20)
        self.dist_thresh_sb.setValue(5)

        self.dist_thresh_sl.valueChanged.connect(self.on_dist_thresh_sl_change)
        self.dist_thresh_sb.valueChanged.connect(self.on_dist_thresh_sb_change)

        hlay_dist_thresh = QHBoxLayout()
        hlay_dist_thresh.addWidget(self.dist_thresh_sl)
        hlay_dist_thresh.addWidget(self.dist_thresh_sb)
        dist_thresh_gb = QGroupBox('Distance thresh')
        dist_thresh_gb.setLayout(hlay_dist_thresh)

        #上面的是距离阈值代码
        #下面的是剔除点数代码
        self.delete_count_sl = QSlider()
        self.delete_count_sl.setOrientation(Qt.Horizontal)
        self.delete_count_sl.setMinimum(0)
        self.delete_count_sl.setMaximum(20)
        self.delete_count_sl.setValue(0)

        self.delete_count_sb = QSpinBox()
        self.delete_count_sb.setMinimum(0)
        self.delete_count_sb.setMaximum(20)
        self.delete_count_sb.setValue(0)

        self.delete_count_sl.valueChanged.connect(self.on_delete_count_sl_change)
        self.delete_count_sb.valueChanged.connect(self.on_delete_count_sb_change)

        hlay_delete_count = QHBoxLayout()
        hlay_delete_count.addWidget(self.delete_count_sl)
        hlay_delete_count.addWidget(self.delete_count_sb)
        delete_count_gb = QGroupBox('Delete Count')
        delete_count_gb.setLayout(hlay_delete_count)



        vlay_line_para.addWidget(iterate_count_gb)
        vlay_line_para.addWidget(calliper_count_gb)
        vlay_line_para.addWidget(dist_thresh_gb)
        vlay_line_para.addWidget(delete_count_gb)

        line_para_gb.setLayout(vlay_line_para)
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
        start_point_xmin_le = QLineEdit()
        start_point_xmax_le = QLineEdit()
        hlay.addWidget(start_point_lb)
        hlay.addWidget(start_point_xmin_le)
        hlay.addWidget(start_point_xmax_le)

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
        hlay_start_x = QHBoxLayout()
        start_point__x_cb = QCheckBox('Start Point X:')
        self.start_point_xmin_le = QLineEdit()
        self.start_point_xmax_le = QLineEdit()
        self.start_point_xmin_le.setDisabled(True)
        self.start_point_xmax_le.setDisabled(True)
        hlay_start_x.addWidget(start_point__x_cb)
        hlay_start_x.addWidget(self.start_point_xmin_le)
        hlay_start_x.addWidget(self.start_point_xmax_le)
        start_point__x_cb.stateChanged.connect(self.on_start_point_x)


        hlay_start_y = QHBoxLayout()
        start_point_y_cb = QCheckBox('Start Point Y:')
        hlay_start_y.addWidget(start_point_y_cb)
        self.start_point_ymin_le = QLineEdit()
        self.start_point_ymax_le = QLineEdit()
        self.start_point_ymin_le.setDisabled(True)
        self.start_point_ymax_le.setDisabled(True)
        hlay_start_y.addWidget(self.start_point_ymin_le)
        hlay_start_y.addWidget(self.start_point_ymax_le)
        start_point_y_cb.stateChanged.connect(self.on_start_point_y)

        hlay_end_x = QHBoxLayout()
        end_point_x_cb = QCheckBox('End   Point X:')
        self.end_point_xmin_le = QLineEdit()
        self.end_point_xmax_le = QLineEdit()
        self.end_point_xmin_le.setDisabled(True)
        self.end_point_xmax_le.setDisabled(True)
        hlay_end_x.addWidget(end_point_x_cb)
        hlay_end_x.addWidget(self.end_point_xmin_le)
        hlay_end_x.addWidget(self.end_point_xmax_le)
        end_point_x_cb.stateChanged.connect(self.on_end_point_x)

        hlay_end_y = QHBoxLayout()
        end_point_y_cb = QCheckBox('End   Point Y:')
        hlay_end_y.addWidget(end_point_y_cb)
        self.end_point_ymin_le = QLineEdit()
        self.end_point_ymax_le = QLineEdit()
        self.end_point_ymin_le.setDisabled(True)
        self.end_point_ymax_le.setDisabled(True)
        hlay_end_y.addWidget(self.end_point_ymin_le)
        hlay_end_y.addWidget(self.end_point_ymax_le)
        end_point_y_cb.stateChanged.connect(self.on_end_point_y)

        hlay_degree = QHBoxLayout()
        degree_cb = QCheckBox('Degree:       ')
        hlay_degree.addWidget(degree_cb)
        self.degree_min_le = QLineEdit()
        self.degree_max_le = QLineEdit()
        self.degree_min_le.setDisabled(True)
        self.degree_max_le.setDisabled(True)
        hlay_degree.addWidget(self.degree_min_le)
        hlay_degree.addWidget(self.degree_max_le)
        degree_cb.stateChanged.connect(self.on_degree)

        hlay_xy=QHBoxLayout()
        space_lb=QLabel('                 ')
        space_lb.setMaximumHeight(20)
        x_lb=QLabel('Min')
        x_lb.setAlignment(Qt.AlignCenter)
        y_lb=QLabel('Max')
        x_lb.setMaximumHeight(20)
        y_lb.setMaximumHeight(20)
        y_lb.setAlignment(Qt.AlignCenter)
        hlay_xy.addWidget(space_lb)
        hlay_xy.addWidget(x_lb)
        hlay_xy.addWidget(y_lb)

        vlay_jug.addLayout(hlay_xy)
        vlay_jug.addLayout(hlay_start_x)
        vlay_jug.addLayout(hlay_start_y)
        vlay_jug.addLayout(hlay_end_x)
        vlay_jug.addLayout(hlay_end_y)
        vlay_jug.addLayout(hlay_degree)

        judgment_gb.setLayout(vlay_jug)

        vlay.addWidget(line_result_gb)
        vlay.addWidget(judgment_gb)

        self.output.setLayout(vlay)

    def connect_UI(self):
        self.operator.calliper.polar_property=self.polar_cb.currentIndex()
        self.operator.calliper.result=self.result_type_cb.currentIndex()
        self.operator.calliper.threshold=self.calliper_thresh_sb.value()
        self.line_item.rect_width=self.calliper_width_sb.value()
        self.line_item.rect_height=self.calliper_height_sb.value()

        self.operator.fitting_line.iter=self.iterate_count_sb.value()
        self.line_item.rect_count=self.calliper_count_sb.value()
        self.operator.fitting_line.dist=self.dist_thresh_sb.value()
        self.operator.fitting_line.delete_count=self.delete_count_sb.value()
        self.view_widget.update()






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
            if self.points_item is not None:
                self.view_widget.scene.removeItem(self.points_item)
            self.view_widget.scene.removeItem(self.line_item)
            self.line_item=FindLineItem(self.line)
            self.connect_UI()                                   #设置参数
            self.line_item.generate_rect()                      #重新生成矩形
            self.line_item.update()                                                 #绘制
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

    def on_width_sl_change(self,value):
        self.calliper_width_sb.setValue(value)
    def on_width_sb_change(self,value):
        self.calliper_width_sl.setValue(value)
    def on_height_sl_change(self,value):
        self.calliper_height_sb.setValue(value)
    def on_height_sb_change(self,value):
        self.calliper_height_sl.setValue(value)
    def on_thresh_sl_change(self,value):
        self.calliper_thresh_sb.setValue(value)
    def on_thresh_sb_change(self,value):
        self.calliper_thresh_sl.setValue(value)
    def on_iterate_sl_change(self,value):
        self.iterate_count_sb.setValue(value)
    def on_iterate_sb_change(self,value):
        self.iterate_count_sl.setValue(value)
    def on_calliper_count_sl_change(self,value):
        self.calliper_count_sb.setValue(value)
    def on_calliper_count_sb_change(self,value):
        self.calliper_count_sl.setValue(value)
    def on_dist_thresh_sl_change(self,value):
        self.dist_thresh_sb.setValue(value)
    def on_dist_thresh_sb_change(self,value):
        self.dist_thresh_sl.setValue(value)
    def on_delete_count_sl_change(self,value):
        self.delete_count_sb.setValue(value)
    def on_delete_count_sb_change(self,value):
        self.delete_count_sl.setValue(value)

    def on_start_point_x(self,state):
        if state == Qt.Checked:
            self.start_point_xmin_le.setDisabled(False)
            self.start_point_xmax_le.setDisabled(False)
        else:
            self.start_point_xmin_le.setDisabled(True)
            self.start_point_xmax_le.setDisabled(True)
    def on_start_point_y(self,state):
        if state == Qt.Checked:
            self.start_point_ymin_le.setDisabled(False)
            self.start_point_ymax_le.setDisabled(False)
        else:
            self.start_point_ymin_le.setDisabled(True)
            self.start_point_ymax_le.setDisabled(True)
    def on_end_point_x(self,state):
        if state == Qt.Checked:
            self.end_point_xmin_le.setDisabled(False)
            self.end_point_xmax_le.setDisabled(False)
        else:
            self.end_point_xmin_le.setDisabled(True)
            self.end_point_xmax_le.setDisabled(True)
    def on_end_point_y(self,state):
        if state == Qt.Checked:
            self.end_point_ymin_le.setDisabled(False)
            self.end_point_ymax_le.setDisabled(False)
        else:
            self.end_point_ymin_le.setDisabled(True)
            self.end_point_ymax_le.setDisabled(True)
    def on_degree(self,state):
        if state == Qt.Checked:
            self.degree_min_le.setDisabled(False)
            self.degree_max_le.setDisabled(False)
        else:
            self.degree_min_le.setDisabled(True)
            self.degree_max_le.setDisabled(True)

if __name__=='__main__':
    app = QApplication(sys.argv)
    fittingline = FittingLineTool()
    fittingline.resize(1000,750)
    fittingline.show()
    # img=QImage("../../image/cv_team.jpg")
    # calliper.view_widget.set_image(img)
    app.exec()

