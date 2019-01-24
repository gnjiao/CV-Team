from ToolBox.Calliper.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect

from enum import Enum


from Widget.OperatorBaseWidget import OperatorBaseWidget
from Item.RectItem import RectItem

import sys
import cv2

class State(Enum):
    Fail=0
    Success=1
    Idle=2
    Running=3

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
        self.output_points_enable=0

    def init_output(self):
        self.output_midpoint=myPoint()

    def register_output(self):
        if self.src_img is None:
            self.reset_output()

    def reset_output(self):
        if self.output_points_enable==1:
            
    def exec_calliper(self):
        if self.calliper.src_img is None:
            return State.Fail.value
        self.input_points.append(self.rect.A)
        self.input_points.append(self.rect.B)
        self.input_points.append(self.rect.C)
        self.input_points.append(self.rect.D)
        self.calliper.src_img=self.src_img
        self.calliper.set_corePara()
    def test(self,src_img,rect):
        if src_img.shape[2]>1:
            cv2.cvtColor(src_img,self.src_img,cv2.COLOR_BGR2GRAY)
        else:
            src_img.copyTo(self.src_img)
        self.state=self.test_(self.src_img,self.rect)
    def test_(self,src_img,rect):
        if src_img is  None:
            return State.Fail.value
        input_points=list()
        input_points.append(rect.A)
        input_points.append(rect.B)
        input_points.append(rect.C)
        input_points.append(rect.D)
        self.calliper.set_img(src_img)
        self.calliper.set_corePara()
        if self.calliper.Exec(input_points,self.output_points):
            return State.Fail.value
        return State.Success.value
