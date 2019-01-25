from ToolBox.Calliper.Calliper import Calliper
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from AuxiliaryFile.State import State

import cv2

class CalliperOperator:
    def __init__(self):
        self.name='calliper'
        self.state=State.Idle.value
        self.calliper=Calliper()
        self.rect=myRect(myPoint(40,40),10,20,myPoint(1,0))
        self.src_img=None
        self.input_points = list()
        self.output_points=list()
        self.output_points_enable=0

    def init_output(self):
        pass

    def register_output(self):
        if self.src_img is None:
            self.reset_output()

    def reset_output(self):
        if self.output_points_enable==1:
            pass
    def exec_calliper(self):
        if self.calliper.gray is None:
            return State.Fail.value
        self.input_points.clear()
        self.input_points.append(self.rect.A)
        self.input_points.append(self.rect.B)
        self.input_points.append(self.rect.C)
        self.input_points.append(self.rect.D)
        self.calliper.src_img=self.src_img
        self.calliper.set_corePara()
        self.state=State.Running.value
        print(self.state)
        self.state=self.calliper.Exec(self.input_points,self.output_points)
        print(self.state)
        return self.state

if __name__=='__main__':
    operator=CalliperOperator()
    img=cv2.imread('../../image/test.jpg')
    operator.calliper.set_img(img)
    operator.exec_calliper()
