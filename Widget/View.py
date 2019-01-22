#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class View(QGraphicsView):
    signal_mouse_move=pyqtSignal(int,int)

    def __init__(self,*args):
        super().__init__(*args)
        #设置一个滑动条
        self.zoom_slider=QSlider(Qt.Vertical,self)
        self.zoom_slider.setMinimum(0)
        self.zoom_slider.setMaximum(500)
        self.zoom_slider.setValue(250)
        self.zoom_slider.setTickPosition(QSlider.TicksRight)
        self.zoom_slider.valueChanged.connect(self.on_set_matrix)
        self.zoom_slider.setVisible(False)
        self.setRenderHint(QPainter.Antialiasing,False)
        #self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene_pos=QPoint()
        self.key_press=False
        self.setStyleSheet(
            "QGraphicsView{color:black}"
            "QGraphicsView:hover{color:red}"
            "QGraphicsView{background-color:lightgray}"
            "QGraphicsView{border:0px}"
            "QGraphicsView{border-radius:5px}"
        )


    # def keyPressEvent(self, event):
    #     if event.key()==Qt.Key_0:
    #         print('a')
    #         self.key_press=True
    #         return
    #     # else:
    #     #     self.key_press=False
    #     QGraphicsView.keyPressEvent(event)
    # def keyReleaseEvent(self, event):
    #     if event.key()==Qt.Key_0:
    #         print('a')
    #         self.key_press=False
    #         return
    #     # else:
    #     #     self.key_press=False
    #     QGraphicsView.keyReleaseEvent(event)

    def wheelEvent(self,event):
        scene_pos = self.mapToScene(event.pos())
        self.signal_mouse_move.emit(scene_pos.x(), scene_pos.y())
        if self.key_press:
            QGraphicsView.wheelEvent(self, event)
        else:
            cursor_pos=event.pos()
            scene_pos=self.mapToScene(cursor_pos)
            view_width=self.viewport().width()
            view_height=self.viewport().height()
            horz_scale=cursor_pos.x()/view_width
            vert_scale=cursor_pos.y()/view_height
            wheel_delta=event.angleDelta()
            if wheel_delta.y()>0:
                self.on_zoom_in(6)
            else:
                self.on_zoom_out(6)
            view_point = self.transform().map(scene_pos)
            a=int(view_point.x()-view_width*horz_scale)
            self.horizontalScrollBar().setSliderPosition(a)
            b=int(view_point.y()-view_height*vert_scale)
            self.verticalScrollBar().setSliderPosition(b)


    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Control:
    #         self.key_press=True
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.key_press=False


    def mouseDoubleClickEvent(self,event):
        pass
    def mouseMoveEvent(self,event):
        scene_pos=self.mapToScene(event.pos())
        self.scene_pos=scene_pos
        self.signal_mouse_move.emit(scene_pos.x(), scene_pos.y())
        QGraphicsView.mouseMoveEvent(self,event)




    def set_scene(self):
        pass
    def get_mat(self):
        pass
    def cvmat_qimage(self):
        pass
    def qimage_cvmat(self):
        pass

    def on_zoom_in(self,value):
        self.zoom_slider.setValue(self.zoom_slider.value() + value)
    def on_zoom_out(self,value):
        self.zoom_slider.setValue(self.zoom_slider.value() - value)
    def on_set_matrix(self):
        scale=pow(2,(self.zoom_slider.value()-250)*0.02)
        transform=QTransform()
        transform.scale(scale,scale)
        self.setTransform(transform)
    def reset_view(self):
        self.zoom_slider.setValue(250)
        self.on_set_matrix()
        self.ensureVisible(0, 0, 0, 0)


if __name__=='__main__':
    app = QApplication(sys.argv)
    view = View()
    scene = QGraphicsScene()
    pix_map_item = QGraphicsPixmapItem(QPixmap('../image/cv_team.jpg'))
    scene.addItem(pix_map_item)

    view.setScene(scene)
    view.show()
    app.exec()





