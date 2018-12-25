#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DragTreeWidget import DragTreeWidget
import sys
class ToolWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowFlag(Qt.FramelessWindowHint)

        #设置窗口工具栏
        tool_bar=QToolBar()
        tool_bar.setIconSize(QSize(24, 24))
        self.addToolBar(tool_bar)
        action_connection=QAction(QIcon(QPixmap("./image/cv_team.jpg")),self.tr(u'connection'),self)
        tool_bar.addAction(action_connection)

        #窗口添加树形窗
        tool_tree_widget=DragTreeWidget()
        self.setCentralWidget(tool_tree_widget)






if __name__=='__main__':

    app=QApplication(sys.argv)
    window=ToolWindow()
    window.resize(200,600)
    window.show()
    #window.showMaximized()
    app.exec()


