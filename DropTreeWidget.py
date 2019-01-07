from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from DragTreeWidget import DragTreeWidget
class DropTreeWidget(QTreeWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle('DropTreeWidget')
        self.setAcceptDrops(True)
        self.pop_menu=None
        self.flag=False

    def mousePressEvent(self,event):
        if event.button() == Qt.RightButton:
            item=self.itemAt(event.pos())
            print(item)
            if  item is None:
                self.flag=False
                return
            else:
                self.setCurrentItem(self.itemAt(event.pos()))
                self.pop_menu = QMenu(self)
                delete_action = QAction(self)
                delete_action.setText('delete')
                delete_action.setIcon(QIcon('icon\Start_50px.png'))
                self.pop_menu.addAction(delete_action)
                self.flag = True
            print('a')
    def mouseMoveEvent(self,event):
        pass
    def mouseReleaseEvent(self,event):
        pass
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    def dragMoveEvent(self,event):
        pass
    def dropEvent(self, event):
        item=QTreeWidgetItem(self)
        item.setText(0,self.tr(u'pretreatment'))
        item.setIcon(0, QIcon('icon\Start_50px.png'))

    def contextMenuEvent(self,event):
        pass
        if self.flag is True:
            self.pop_menu.exec(QCursor.pos())
            event.accept()
        else:
            return










if __name__=='__main__':
    app = QApplication(sys.argv)
    drag=DragTreeWidget()
    drop=DropTreeWidget()
    window=QWidget()
    hlay=QHBoxLayout()
    hlay.addWidget(drag)
    hlay.addWidget(drop)
    window.setLayout(hlay)
    window.show()
    app.exec()
