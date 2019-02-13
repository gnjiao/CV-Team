from ToolBox.Calliper.Calliper import Calliper
from ToolBox.FittingLine.FittingLineAlgorithm import FittingLine
from Geometry.myPoint import myPoint
from Geometry.myRect import myRect
from AuxiliaryFile.State import State

import cv2

class FittingLineOperator:
    def __init__(self):
        self.name='FittingLine'
        self.state=State.Idle.value
        self.calliper=Calliper()
        self.fitting_points=list()    #拟合直线的点
        self.rects=list()             #直线查找的item上的矩形
        self.src_img=None
        self.input_points=list()      #卡尺的输入点
        self.output_points=list()     #卡尺的输出点
        self.fitting_line=None
        self.result=None
        self.output_points_enable=0

    def init_output(self):
        pass

    def register_output(self):
        if self.src_img is None:
            self.reset_output()

    def reset_output(self):
        if self.output_points_enable==1:
            pass
    def exec_fitting(self):
        if self.calliper.gray is None:
            return State.Fail.value
        self.calliper.src_img = self.src_img
        self.calliper.set_corePara()
        self.state=State.Running.value
        for i in range(len(self.rects)):
            self.input_points.clear()
            self.input_points.append(self.rects[i].A)
            self.input_points.append(self.rects[i].B)
            self.input_points.append(self.rects[i].C)
            self.input_points.append(self.rects[i].D)
            self.state = self.calliper.Exec(self.input_points, self.output_points)
            self.fitting_points.append(self.output_points[1])
        self.fitting_line=FittingLine(self.fitting_points)
        ok,ng,line=self.fitting_line.Ransac()
        print(ok,ng,line)
        print(self.state)
        return self.state

if __name__=='__main__':
    fit=FittingLineOperator()
    img=cv2.imread('../../image/test.jpg')
    fit.calliper.set_img(img)
    fit.exec_fitting()
