import math
import numpy as np
from  numpy import random as nr
from  Geometry.myPoint import  myPoint

class FittingCircle:
    def __init__(self,points_input):
        self.points_OK=None
        self.points_NG=None
        self.points_input=points_input
        self.iter=2000
        self.dist_thresh=1
        self.delete_count=0
        self.select_point_ok=list()
        self.select_point_ng=list()
        self.temp_point_ok=list()
        self.temp_point_ng=list()
        self.k=0

    def Ransac(self):
        for i in range(self.iter):
            #产生随机数
            chosed_point0=nr.randint(0,len(self.points_input))
            chosed_point1=nr.randint(0,len(self.points_input))
            if chosed_point0==chosed_point1:
                i=i-1
                continue
            a=self.points_input[chosed_point1].y-self.points_input[chosed_point0].y
            b=self.points_input[chosed_point0].x-self.points_input[chosed_point1].x
            c=self.points_input[chosed_point1].x*self.points_input[chosed_point0].y - \
              self.points_input[chosed_point0].x*self.points_input[chosed_point1].y
            self.temp_point_ok.clear()
            self.temp_point_ng.clear()
            for j in range(len(self.points_input)):
                dist=abs(a*self.points_input[j].x+b*self.points_input[j].y+c)/math.sqrt(a*a+b*b)
                if dist<self.dist_thresh:
                    self.temp_point_ok.append(self.points_input[j])
                else:
                    self.temp_point_ng.append(self.points_input[j])
            if len(self.temp_point_ok) > len(self.select_point_ok):
                self.k=math.log10(0.0001)/math.log10(1-pow(len(self.temp_point_ok)/len(self.points_input),2))
                self.select_point_ok.clear()
                self.select_point_ng.clear()
                self.select_point_ok=self.temp_point_ok
                self.select_point_ng=self.temp_point_ng
            if i< self.k:
                break
        if len(self.select_point_ng)<self.delete_count:
            temp_num=self.delete_count-len(self.select_point_ng)
            self.delete_points(self.select_point_ok,self.select_point_ng,temp_num)
    def delete_points(self,points_ok,points_ng,delete_count):


    def Huber(self):
        pass


if __name__=='__main__':
    point1=myPoint(0,0)
    point2=myPoint(0,5)
    point3=myPoint(0,7)
    point4=myPoint(0,8)
    point5=myPoint(0,4)
    point6=myPoint(0,9)
    points=list()
    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)
    points.append(point5)
    points.append(point6)
    print(points[2].y)
    print(len(points))


