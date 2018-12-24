#导入QT组件
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import math

class View(QGraphicsView):
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
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene_pos=QPoint()



    def wheelEvent(self,event):
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
        view_point=self.transform().map(scene_pos)

        vert_bar=self.verticalScrollBar()
        a=int(view_point.x()-view_width*horz_scale)
        self.horizontalScrollBar().setSliderPosition(a)
        b=int(view_point.y()-view_height*vert_scale)
        vert_bar.setSliderPosition(b)

    def mouseDoubleClickEvent(self,event):
        pass
    def mouseMoveEvent(self,event):
        print('cur pos:',event.pos().x(),event.pos().y())
        scene_pos=self.mapToScene(event.pos())
        self.scene_pos=scene_pos
        print('scene pos:',scene_pos.x(),scene_pos.y())


    def reset_view(self):
        pass
    def set_image(self):
        pass
    def adapt_window(self):
        pass
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
        print('value changed')
        scale=math.pow(2,(self.zoom_slider.value()-250)*0.02)
        transform=QTransform()
        transform.scale(scale,scale)
        self.setTransform(transform)
    def on_adapt_window(self):
        pass
    def on_drag_mouse(self):
        pass


if __name__=='__main__':
    pass






