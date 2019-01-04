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

        AB = np.array([[self.B.x - self.A.x], [self.B.y - self.A.y]])
        AD = np.array([[self.D.x - self.A.x], [self.D.y - self.A.y]])
        theta=math.atan2(AB[1],AB[0]) - math.atan2(AD[1],AD[0])
        print((180/math.pi)*theta)
        if theta==0:
            print('in a line')
            return
        self.AB_count = int(LA.norm(AB))
        self.AD_count = int(LA.norm(AD))
        self.diff = np.zeros([self.AB_count-1, self.AD_count])
        self.temp_diff = np.zeros([self.AB_count-1, self.AD_count])
        self.set_img('./image/test.jpg')
        if self.src_img.shape[2]!=1:
            self.img_to_gray()
        else:
            self.gray=self.src_img

        for i in range (self.AD_count):
            unit_AD=(i*AD/self.AD_count)
            first_x = round(float(self.A.x + unit_AD[0]))
            first_y = round(float(self.A.y + unit_AD[1]))
            self.location_x=first_x
            self.location_y=first_y
            for j in range(self.AB_count-1):
                unit_AB=(j+1)*AB/self.AB_count
                next_x = round(float(first_x + unit_AB[0]))
                next_y = round(float(first_y + unit_AB[1]))
                #a=float(self.gray[51][30]) - float(self.gray[52][30])
                self.temp_diff[j][i]=float(self.gray[next_x][next_y])-float(self.gray[self.location_x][self.location_y])

                if self.temp_diff[j][i]>self.threshold:
                    self.diff[j][i]=self.diff[j][i]+self.temp_diff[j][i]
                self.location_x=next_x
                self.location_y=next_y
        # self.find_point()
        # self.get_result()
    def set_img(self,path):
        self.src_img=cv2.imread(path)
    def img_to_gray(self):
        self.gray= cv2.cvtColor(self.src_img,cv2.COLOR_BGR2GRAY)
    def find_point(self,diff):
        for i in range(self.AB_count-1):
            col_sum=0
            count_num=0
            for j in range(self.AD_count):
                col_sum=diff[i][j]+col_sum
                diff_temp=diff[i][j]
                if diff_temp!=0:
                    count_num=count_num+1
            if count_num>self.AD_count/3 or col_sum>self.AD_count/5*self.threshold:
                sort_x=i
                break
if __name__=='__main__':
    rect_corn=list()
    rect_corn.append(myPoint(50,30))
    rect_corn.append(myPoint(100,30))
    rect_corn.append(myPoint(100, 60))
    rect_corn.append(myPoint(50, 60))
    calliper=Calliper(rect_corn)
    print(calliper.temp_diff)