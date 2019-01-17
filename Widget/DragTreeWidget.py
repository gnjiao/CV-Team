from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class DragTreeWidget(QTreeWidget):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selectedItem=0
        self.drag_position=0
        self.add_tree_widget_item()
        self.setAcceptDrops(False)
        self.setDragEnabled(True)
        self.setStyle(QStyleFactory.create('windows'))
    # def mouseMoveEvent(self,event):
    #     #print('move:',self.drag_position)
    #     if (event.pos()-self.drag_position).manhattanLength() > QApplication.startDragDistance():
    #         if True:
    #             drag=QDrag(self)
    #             mime_data=QMimeData()
    #             mime_data.setText('selected item')
    #             drag.setMimeData(mime_data)
    #             print('drag ok')
    #             drag.exec(Qt.MoveAction)
    #     QTreeWidget.mouseMoveEvent(self,event)
    #
    def mousePressEvent(self,event):
        #if event.button() == Qt.LeftButton:
        current_item=self.itemAt(event.pos())
        if current_item is not None:
            #current_item.setFlags(current_item.flags()|)
            self.setCurrentItem(current_item)
            text=current_item.text(0)
            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setText(text)
            drag.setMimeData(mimedata)
            drag.exec_()

        QTreeWidget.mousePressEvent(self, event)

    def add_tree_widget_item(self):
        root_pretreatment=QTreeWidgetItem(self)
        root_pretreatment.setText(0,self.tr(u'pretreatment'))
        root_pretreatment.setIcon(0,QIcon('..\image\cv_team.png'))
        root_pretreatment.setExpanded(True)
        #root_pretreatment.setFlags(Qt.ItemIsDragEnabled)
        child_gauss=QTreeWidgetItem(root_pretreatment)
        child_gauss.setText(0,self.tr(u'gauss'))
        root_pretreatment.addChild(child_gauss)
        child_gauss.setIcon(0,QIcon('..\icon\Start_50px.png'))
        child_calliper=QTreeWidgetItem(root_pretreatment)
        child_calliper.setText(0,self.tr(u'calliper'))
        root_pretreatment.addChild(child_calliper)
        child_calliper.setIcon(0,QIcon('..\icon\Start_50px.png'))
        #child_calliper.setFlags(Qt.ItemIsUserCheckable | child_calliper.flags())
    def itemDoubleClicked(self, item, p_int):
        print('a')
    # def mouseReleaseEvent(self,event):
    #     pass
    # def doSelect(self):
    #     pass
    #
    # def dragLeaveEvent(self,event):
    #     pass
    #
    # def dropEvent(self,event):
    #     event.setDropAction(Qt.MoveAction)
    #     event.accept()
    # def dragEnterEvent(self,event):
    #     event.accept()


if __name__== '__main__':

    app=QApplication(sys.argv)
    window=DragTreeWidget()

    window.resize(200,600)
    window.show()
    #window.showMaximized()
    app.exec()
