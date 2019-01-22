import numpy as np
from  numpy import linalg as LA
import math
import cv2

from Geometry.myPoint import myPoint


class Calliper:
    def __init__(self,rect_corners):
        self.src_img=None
        self.gray=None
        self.polar_property=0
        self.result_type=0
        self.threshold=0
        self.result=list()
        self.A = rect_corners[0]
        self.B = rect_corners[1]
        self.C = rect_corners[2]
        self.D = rect_corners[3]
        self.points_out=list()
        self.AB = np.array([[self.B.x - self.A.x], [self.B.y - self.A.y]])
        self.AD = np.array([[self.D.x - self.A.x], [self.D.y - self.A.y]])
        theta=math.atan2(self.AB[1],self.AB[0]) - math.atan2(self.AD[1],self.AD[0])
        #print((180/math.pi)*theta)
        if theta==0:
            print('in a line')
            return
        self.AB_count = int(LA.norm(self.AB))
        self.AD_count = int(LA.norm(self.AD))
        self.diff = np.zeros([self.AB_count-1, self.AD_count])
        self.temp_diff = np.zeros([self.AB_count-1, self.AD_count])
        self.set_img('../../image/test.jpg')
        if self.src_img.shape[2]!=1:
            self.img_to_gray()
        else:
            self.gray=self.src_img

        print('self.gray:',self.gray)
        for i in range (self.AD_count):
            unit_AD=(i*self.AD/self.AD_count)
            first_x = round(float(self.A.x + unit_AD[0]))
            first_y = round(float(self.A.y + unit_AD[1]))
            self.location_x=first_x
            self.location_y=first_y
            for j in range(self.AB_count-1):
                unit_AB=(j+1)*self.AB/self.AB_count
                next_x = round(float(first_x + unit_AB[0]))
                next_y = round(float(first_y + unit_AB[1]))
                print('gray:',float(self.gray[next_x][next_y]),float(self.gray[self.location_x][self.location_y]))
                self.temp_diff[j][i]=float(self.gray[next_x][next_y])-float(self.gray[self.location_x][self.location_y])

                if self.temp_diff[j][i]>self.threshold:
                    self.diff[j][i]=self.diff[j][i]+self.temp_diff[j][i]
                else:
                    self.diff[j][i]+=0
                self.location_x=next_x
                self.location_y=next_y
        print(self.diff)
        self.find_point(self.diff)
        # self.get_result()
    def set_img(self,path):
        self.src_img=cv2.imread(path)
    def img_to_gray(self):
        self.gray= cv2.cvtColor(self.src_img,cv2.COLOR_BGR2GRAY)
    def find_point(self,diff):
        col_sum=0
        count_num=0
        sort_x=0
        self.points_out.clear()
        for i in range(self.AB_count-1):
            col_sum = 0
            count_num = 0
            for j in range(self.AD_count):
                col_sum=diff[i][j]+col_sum
                diff_temp=diff[i][j]
                if diff_temp!=0:
                    count_num=count_num+1
            if count_num>self.AD_count/3 or col_sum>self.AD_count/5*self.threshold:
                sort_x=i
                break
        if count_num==0:
            pass
        else:
            self.points_out.append(myPoint(round(self.A.x+sort_x*self.AB[0][0]/LA.norm(self.AB)),
                                           round(self.A.y+sort_x*self.AB[1][0]/LA.norm(self.AB))))
            self.points_out.append(myPoint(round(self.D.x + sort_x * self.AB[0][0] / LA.norm(self.AB)),
                                           round(self.D.y + sort_x * self.AB[1][0] / LA.norm(self.AB))))
            self.points_out.append(myPoint(round(self.points_out[0].x+self.points_out[1].x)/2,
                                           round(self.points_out[0].y+self.points_out[1].y)/2))
            print(self.points_out[2].x,self.points_out[2].y)

if __name__=='__main__':
    rect_corn=list()
    rect_corn.append(myPoint(0,0))
    rect_corn.append(myPoint(5,0))
    rect_corn.append(myPoint(5, 5))
    rect_corn.append(myPoint(0, 5))
    calliper=Calliper(rect_corn)
    #print(calliper.diff)
