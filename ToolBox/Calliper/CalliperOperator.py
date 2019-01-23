from ToolBox.Calliper.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from Widget.OperatorBaseWidget import OperatorBaseWidget
from Item.RectItem import RectItem

import sys
import cv2

class CalliperOperator:
    def __init__(self):
        self.name='calliper'
        self.state=0                #状态标志位 0 Idle,1 Success 2 Fail
        self.calliper=Calliper()
        self.rect=myRect(myPoint(40,40),10,20,myPoint(1,0))
        self.src_img=None
        self.output_midpoint=None
        self.input_points = list()
        self.output_points=list()

    def init_output(self):
        self.output_midpoint=myPoint()

    def register_output(self):
        if self.src_img is None:
            self.reset_output()

    def reset_output(self):

    def exec_calliper(self):
        if self.src_img is None:
            return 2
        self.input_points.append(self.rect.A)
        self.input_points.append(self.rect.B)
        self.input_points.append(self.rect.C)
        self.input_points.append(self.rect.D)
        self.calliper.src_img=self.src_img
        self.calliper.set_corePara()

