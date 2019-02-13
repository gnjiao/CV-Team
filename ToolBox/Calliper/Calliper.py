import numpy as np
from  numpy import linalg as LA
import math
import cv2

from Geometry.myPoint import myPoint
from AuxiliaryFile.State import State

class Calliper:
    def __init__(self):
        self.src_img=None
        self.gray=None
        self.polar_property=0
        self.result_type=0
        self.threshold=120
        self.compensate=0
        self.result=list()
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.AB = None
        self.AD = None
        self.AB_count=None
        self.AD_count=None
        self.diff = None
        self.temp_diff=None
        self.points_out=list()
        self.location_x=0
        self.location_y=0


    def set_corePara(self):
        self.polar_property=0
        self.result_type=0
        self.threshold=20
        self.compensate=0.5
    def set_img(self,src_img):
        if src_img.shape[2]==1:
            self.gray=src_img
        else:
            self.gray=cv2.cvtColor(src_img,cv2.COLOR_BGR2GRAY)
    def Exec(self,in_points,out_points):
        self.A = in_points[0]
        self.B = in_points[1]
        self.C = in_points[2]
        self.D = in_points[3]
        self.AB = np.array([[self.B.x - self.A.x], [self.B.y - self.A.y]])
        self.AD = np.array([[self.D.x - self.A.x], [self.D.y - self.A.y]])
        theta=math.atan2(self.AB[1],self.AB[0]) - math.atan2(self.AD[1],self.AD[0])
        if theta==0:
            return State.Fail.value
        self.AB_count = int(LA.norm(self.AB))
        self.AD_count = int(LA.norm(self.AD))
        self.diff = np.zeros([self.AD_count-1, self.AB_count])
        self.temp_diff = np.zeros([self.AD_count-1, self.AB_count])
        for i in range (self.AB_count):
            unit_AB=(i*self.AB/self.AB_count)
            first_x = round(float(self.A.x + unit_AB[0]))
            first_y = round(float(self.A.y + unit_AB[1]))
            self.location_x=first_x
            self.location_y=first_y
            for j in range(self.AD_count-1):
                unit_AD=(j+1)*self.AD/self.AD_count
                next_x = round(float(first_x + unit_AD[0]))
                next_y = round(float(first_y + unit_AD[1]))
                self.temp_diff[j][i]=float(self.gray[next_y][next_x])-float(self.gray[self.location_y][self.location_x])
                if self.temp_diff[j][i]>self.threshold:
                    self.diff[j][i] =  self.temp_diff[j][i] 
                else:
                    self.diff[j][i]+=0
                self.location_x=next_x
                self.location_y=next_y
        #print('self.diff',self.diff)
        return self.find_point(self.diff)
    def find_point(self,diff):
        col_num=0
        sort_x=0
        self.points_out.clear()
        for i in range(self.AD_count-1):
            col_sum = 0
            col_num = 0
            for j in range(self.AB_count):
                col_sum=diff[i][j]+col_sum
                diff_temp=diff[i][j]
                if diff_temp!=0:
                    col_num=col_num+1
            if col_num>2*self.AB_count/3 or col_sum>self.AB_count/5*self.threshold:
                sort_x=i+self.compensate
                break
            # else:
            #     return State.Fail.value
        if sort_x==0:
            return State.Fail.value
        self.points_out.append(myPoint(round(self.A.x+sort_x*self.AD[0][0]/LA.norm(self.AD)),
                                       round(self.A.y+sort_x*self.AD[1][0]/LA.norm(self.AD))))
        self.points_out.append(myPoint(round(self.B.x + sort_x * self.AD[0][0] / LA.norm(self.AD)),
                                       round(self.B.y + sort_x * self.AD[1][0] / LA.norm(self.AD))))
        self.points_out.append(myPoint(round(self.points_out[0].x+self.points_out[1].x)/2,
                                       round(self.points_out[0].y+self.points_out[1].y)/2))
        print(self.points_out[2].x,self.points_out[2].y)
        return State.Success.value
if __name__=='__main__':
    rect_corn=list()
    rect_corn.append(myPoint(10,18))
    rect_corn.append(myPoint(30,18))
    rect_corn.append(myPoint(30, 61))
    rect_corn.append(myPoint(10, 61))
    calliper=Calliper()
    #print(calliper.diff)
