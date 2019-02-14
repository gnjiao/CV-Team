from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Widget.ViewWidget import ViewWidget
import sys

from Geometry.myRect import myRect
from Geometry.myLine import myLine
from Geometry.myPoint import myPoint
from Item.RectItem import RectItem


class OperatorBaseWidget(QDialog):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle('BaseWidget')
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        tab_widget=QTabWidget()
        tab_widget.setStyleSheet(
                                "QTabWidget{color:black}"
                                "QTabWidget:hover{color:red}"
                                "QTabWidget{background-color:lightgray}"
                                "QTabWidget{border:0px}"
                                "QTabWidget{border-radius:10px}"
                                "QTabWidget{padding:2px 4px}"
                                )
        tab_widget.setTabPosition(QTabWidget.South)
        self.base_data=QFrame(tab_widget)
        tab_widget.addTab(self.base_data,self.tr(u'base data'))
        self.item_setting=QFrame(tab_widget)
        tab_widget.addTab(self.item_setting,self.tr(u'item setting'))
        self.output=QFrame(tab_widget)
        tab_widget.addTab(self.output,self.tr(u'output data '))
        tool_bar=QToolBar()
        tool_bar.setStyleSheet("QToolBar{color:black}" 
                               "QToolBar:hover{color:red}"
                               "QToolBar{background-color:lightgray}"
                               "QToolBar{border:2px}"
                               "QToolBar{border-radius:5px}"
                               "QToolBar{padding:2px 4px}"
                               )

        tool_bar.setIconSize(QSize(24, 24))
        self.action_load_img = QAction(QIcon(QPixmap(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.jpg")), self.tr(u'load img'), self)
        tool_bar.addAction(self.action_load_img)
        action_exec = QAction(QIcon(QPixmap(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.jpg")), self.tr(u'exec'), self)
        tool_bar.addAction(action_exec)
        action_stop = QAction(QIcon(QPixmap(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\Start_50px.png")), self.tr(u'stop'), self)
        tool_bar.addAction(action_stop)
        action_load_video = QAction(QIcon(QPixmap(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\icon\\Process_50px.png")), self.tr(u'load video'), self)
        tool_bar.addAction(action_load_video)
        action_add_item = QAction(QIcon(QPixmap("C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\Geo.ico")), self.tr(u'add item'), self)
        tool_bar.addAction(action_add_item)
        self.action_load_img.triggered.connect(self.on_load_image)
        action_exec.triggered.connect(self.on_exec)
        action_stop.triggered.connect(self.on_stop)
        action_load_video.triggered.connect(self.on_load_video)
        action_add_item.triggered.connect(self.on_add_item)
        vlay=QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        self.view_widget=ViewWidget()
        self.view_widget.setStyleSheet(
            "QWidget{color:black}"
            "QWidget:hover{color:red}"
            "QWidget{background-color:lightgray}"
            "QWidget{border:0px}"
            "QWidget{border-radius:5px}"
            #"QWidget{padding:2px 4px}"
        )

        label=QLabel(self)
        label.setText('this is label')
        label.setFrameStyle(QFrame.Panel)
        label.setMaximumHeight(25)
        label.setFrameShadow(QFrame.Sunken)

        vlay.addWidget(tool_bar)
        vlay.addWidget(self.view_widget)
        # vlay1.addLayout(hlay)
        # vlay1.addWidget(label)
        splitter.addWidget(tab_widget)
        right_widget=QWidget()
        right_widget.setLayout(vlay)
        splitter.addWidget(right_widget)
        splitter.setSizes([315, 685])

        vlay2=QVBoxLayout()
        vlay2.addWidget(splitter)
        vlay3=QVBoxLayout()
        vlay3.addLayout(vlay2)
        vlay3.addWidget(label)
        self.setLayout(vlay3)
        # 连接信号与槽
    def on_load_image(self):
        pass
    def on_exec(self):
        pass
    def on_stop(self):
        pass
    def on_load_video(self):
        pass
    def on_add_item(self):
        pass

if __name__=='__main__':
    app = QApplication(sys.argv)
    point1 = myPoint(40, 50)
    width = 50
    height = 30
    dir=myPoint(1,0)
    rect = myRect(point1, width, height, dir)
    line=myLine(myPoint(50,50),myPoint(146,50))
    rect_item = RectItem(rect)#RectItem(rect)
    operator_base=OperatorBaseWidget()
    img=QImage("../image/cv_team.jpg")
    operator_base.view_widget.set_image(img)
    operator_base.view_widget.add_item(rect_item)
    operator_base.show()
    operator_base.resize(800,600)
    #window.showMaximized()
    app.exec()