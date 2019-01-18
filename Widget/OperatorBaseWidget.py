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
        page_in=QFrame(tab_widget)
        tab_widget.addTab(page_in,self.tr(u'tab1'))
        page_out=QFrame(tab_widget)
        tab_widget.addTab(page_out,self.tr(u'tab2'))
        tool_bar=QToolBar()
        tool_bar.setStyleSheet("QToolBar{color:black}" 
                               "QToolBar:hover{color:red}"
                               "QToolBar{background-color:lightgray}"
                               "QToolBar{border:2px}"
                               "QToolBar{border-radius:5px}"
                               "QToolBar{padding:2px 4px}"
                               )

        tool_bar.setIconSize(QSize(24, 24))
        action_load_img = QAction(QIcon(QPixmap("../image/cv_team.jpg")), self.tr(u'load img'), self)
        tool_bar.addAction(action_load_img)
        action_exec = QAction(QIcon(QPixmap("../image/cv_team.jpg")), self.tr(u'exec'), self)
        tool_bar.addAction(action_exec)
        action_stop = QAction(QIcon(QPixmap("../image/cv_team.jpg")), self.tr(u'stop'), self)
        tool_bar.addAction(action_stop)
        action_load_video = QAction(QIcon(QPixmap("../image/cv_team.jpg")), self.tr(u'load video'), self)
        tool_bar.addAction(action_load_video)

        hlay=QHBoxLayout()
        vlay=QVBoxLayout()
        # vlay1 = QVBoxLayout()
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

        vlay2=QVBoxLayout()
        vlay2.addWidget(splitter)
        vlay3=QVBoxLayout()
        vlay3.addLayout(vlay2)
        vlay3.addWidget(label)
        self.setLayout(vlay3)



if __name__=='__main__':
    app = QApplication(sys.argv)
    point1 = myPoint(40, 50)
    width = 50
    height = 30
    dir=myPoint(1,0)
    rect = myRect(point1, width, height, dir)
    line=myLine(myPoint(50,50),myPoint(146,50))
    rect_item = RectItem(rect)#RectItem(rect)
    operater_base=OperatorBaseWidget()
    img=QImage("../image/hh.bmp")
    operater_base.view_widget.set_image(img)
    operater_base.view_widget.add_item(rect_item)
    operater_base.show()
    operater_base.resize(800,600)
    #window.showMaximized()
    app.exec()