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
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setColumnCount(3)
        self.setColumnWidth(0,120)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 60)
        self.setHeaderLabels(['tools','time','status'])

        self.pop_menu=None
        self.flag=False
        self.current_item=None
        self.index = 0
        self.edit_item_flag=False
        self.last_item=0

        self.pop_menu = QMenu(self)
        self.delete_action = QAction(self)
        self.delete_action.setText('delete')
        self.delete_action.setIcon(QIcon('icon\Start_50px.png'))

        self.rename_action = QAction(self)
        self.rename_action.setText('rename')
        self.rename_action.setIcon(QIcon('icon\Start_50px.png'))

        self.pop_menu.addAction(self.delete_action)
        self.pop_menu.addAction(self.rename_action)

        self.delete_action.triggered.connect(self.delete_item)
        self.rename_action.triggered.connect(self.rename_item)

    def mousePressEvent(self,event):
        if event.button() == Qt.RightButton:
            self.current_item=self.itemAt(event.pos())
            if  self.current_item is not None:
                self.current_item = self.itemAt(event.pos())
                #self.current_item.setFlags(Qt.ItemIsEditable | self.current_item.flags())
                self.setCurrentItem(self.current_item)
                self.index=self.indexOfTopLevelItem(self.current_item)
                self.flag = True
            else:
                self.flag=False
                return
        else:
            self.current_item = self.itemAt(event.pos())
            if self.current_item is not None:
                self.current_item=self.itemAt(event.pos())
                self.setCurrentItem(self.current_item)
                #self.current_item.setFlags(Qt.ItemIsUserCheckable | self.current_item.flags())
        self.closePersistentEditor(self.topLevelItem(self.last_item), 0)
        QTreeWidget.mousePressEvent(self,event)

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
        item.setText(0,event.mimeData().text())
        item.setIcon(0, QIcon('icon\Start_50px.png'))
        #item.setFlags(Qt.ItemIsUserCheckable | item.flags())

    def contextMenuEvent(self,event):
        if self.flag is True:
            self.pop_menu.exec(QCursor.pos())
            event.accept()
        else:
            return
    def delete_item(self):
        self.takeTopLevelItem(self.index)
    def rename_item(self):
        self.last_item= self.indexOfTopLevelItem(self.current_item)
        self.openPersistentEditor(self.current_item)
        self.editItem(self.current_item)


        #self.closePersistentEditor(self.current_item,0)
        #self.current_item.setFlags(self.current_item.flags())
    # def closeEditor(self, *args, **kwargs):
    #     self.setCurrentItem(self.current_item)
    #     self.closePersistentEditor(self.current_item,0)
    #     print('d')





def a():
    print('s')


if __name__=='__main__':
    app = QApplication(sys.argv)
    drag=DragTreeWidget()
    drop=DropTreeWidget()
    drop.itemDoubleClicked.connect(a)
    window=QWidget()
    hlay=QHBoxLayout()
    hlay.addWidget(drag)
    hlay.addWidget(drop)
    window.setLayout(hlay)
    window.show()
    app.exec()
