# 导入QT组件
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolWindow import ToolWindow

import sys


# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle(self.tr(u'CV-Team'))
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
        # 设置菜单栏
        mb = self.menuBar()
        mb.setNativeMenuBar(False)
        file_menu = mb.addMenu('&File')
        camera_menu = mb.addMenu('&Camera')
        inspection_menu = mb.addMenu(self.tr(u'&Inspection'))
        settings_menu = mb.addMenu(self.tr(u'&Settings'))
        about_menu = mb.addMenu(self.tr(u'&About'))

        # 设置二级菜单
        save_menu = file_menu.addAction(QIcon('icon\Start_50px.png'), self.tr(u'Save'))
        about = about_menu.addAction(self.tr(u'About'))

        # 设置状态栏
        spacer = QWidget(self,Qt.Widget)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        status_bar = QStatusBar(self)
        status_bar.addWidget(spacer)

        label = QLabel(status_bar)
        label.setAlignment(Qt.AlignCenter)
        date_time = QDateTime.currentDateTime()
        date = date_time.toString('yyyy-MM-dd hh:mm:ss dddd')
        label.setText(date)
        status_bar.addWidget(label)

        self.setStatusBar(status_bar)

        # 设置工具栏
        tool_bar = QToolBar()
        tool_bar.setIconSize(QSize(32, 32))

        # tool_button=QToolButton(tool_bar)
        # tool_button.setText('this button')
        action_load_img = QAction(QIcon(QPixmap("./image/cv_team.jpg")), self.tr(u'load img'), self)
        action_load_video = QAction(QIcon(QPixmap("./image/cv_team.jpg")), self.tr(u'load img'), self)
        tool_bar.addAction(action_load_img)
        tool_bar.addSeparator()
        tool_bar.addAction(action_load_video)
        tool_bar.addSeparator()



        self.addToolBar(tool_bar)

        # 设置树形窗口
        dock_tool = QDockWidget(self.tr(u'tool library'))
        tool_window = ToolWindow()
        dock_tool.setWidget(tool_window)  # 添加一个主窗口作为工具窗口
        dock_tool.setAllowedAreas(Qt.LeftDockWidgetArea)
        dock_tool.setMinimumWidth(300)
        # self.addDockWidget(Qt.LeftDockWidgetArea,dock_tool)

        # 编辑窗口
        edit_widget = QWidget(self,Qt.Widget)
        # edit_widget.acceptDrops()
        # line_edit=QLineEdit(edit_widget)
        # line_edit.setGeometry(500,100,100,200)
        # self.setCentralWidget(edit_widget)

        # 命令输出窗口

        command_widget = QWidget(self,Qt.Widget)
        command_label = QLabel(command_widget)
        command_label.setText('this is command label')
        # command_widget.setGeometry(400,400,200,200)

        # 原始图像显示窗口
        dock_src_img = QDockWidget('dock src')
        dock_src_img.setMinimumWidth(800)
        img_widget = QWidget(self,Qt.Widget)
        dock_src_img.setWidget(img_widget)

        # 图像输出窗口
        self.dock_dst_img = QDockWidget('dock dst')
        self.dock_dst_img.setMinimumWidth(800)

        img_widget = QWidget(self,Qt.Widget)
        self.dock_dst_img.setWidget(img_widget)

        # 结果显示窗口
        # dock_result=QDockWidget(self)
        result_widget = QWidget(self,Qt.Widget)
        label=QLabel('this is result widget',result_widget)

        # 自定义信号

        # 连接信号与槽


        # 窗口的布局管理
        center_widget = QWidget(self,Qt.Widget)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(edit_widget)
        splitter.addWidget(result_widget)
        splitter.addWidget(command_widget)
        splitter.setSizes([500, 200, 120])

        vlay = QVBoxLayout()
        vlay.addWidget(splitter)
        center_widget.setLayout(vlay)
        self.setCentralWidget(center_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_tool)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_src_img)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_dst_img)

        # splitter_all=QSplitter(Qt.Horizontal)
        # splitter_center=QSplitter(Qt.Vertical)
        # splitter_right=QSplitter(Qt.Vertical)
        #
        # splitter_center.addWidget(edit_widget)
        # splitter_center.addWidget(command_widget)
        # #splitter_center.setStretchFactor(3,1)
        # splitter_center.setSizes([500,100])
        #
        # splitter_right.addWidget(dock_src_img)
        # splitter_right.addWidget(dock_dst_img)
        # splitter_right.addWidget(dock_result)
        # splitter_right.setSizes([250,250,100])
        #
        # splitter_all.addWidget(dock_tool)
        # splitter_all.addWidget(splitter_center)
        # splitter_all.addWidget(splitter_right)
        # #splitter_all.setStretchFactor(1,150)
        # splitter_all.setSizes([200,500,500])
        #
        # grid=QGridLayout()
        # grid.addWidget(splitter_all)
        # #self.setLayout(grid)
        # main_widget=QWidget(self)
        # main_widget.setLayout(grid)
        # self.setCentralWidget(main_widget)

        # layout=QHBoxLayout()
        # for i in range(5):
        # close_button = QPushButton('ok')
        # close_button.released.connect( lambda x=i : self._my_fun(x))
        # layout.addWidget(close_button)
        # #label.setAlignment(Qt.AlignCenter)
        # widget=QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)

     #下面是槽函数实例
    def on_load_img_pressed(self):
        pass


app = QApplication(sys.argv)
window = MainWindow()
# window.show()
# window.resize(800,600)
window.showMaximized()
app.exec()


