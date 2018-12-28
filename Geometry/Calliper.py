import numpy as np
from  numpy import linalg as LA
import math
import cv2

from Geometry.myPoint import myPoint


class Calliper:
    def __init__(self,rect_corners):

        self.src_img=None

        print(image1[100][100])
        #self.gray=None
        cv2.namedWindow('this')
        cv2.imshow('this',self.src_img)
        #self.gray= cv2.cvtColor(self.src_img,cv2.COLOR_BGR2GRAY)

        #print(self.gray.shape)
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
        AB_count = int(LA.norm(AB))
        AD_count = int(LA.norm(AD))
        # diff=np.array((AB_count-1)*AD_count)
        # diff=diff.reshape(AB_count,AD_count)
        for i in range (AD_count):
            unit_AD=(i*AD/AD_count)
            first_x = round(float(self.A.x + unit_AD[0]))
            first_y = round(float(self.A.y + unit_AD[1]))
            self.location_x=first_x
            self.location_y=first_y
            for j in range(AB_count-1):
                unit_AB=(j+1)*AB/AB_count
                next_x = round(float(first_x + unit_AB[0]))
                next_y = round(float(first_y + unit_AB[1]))
                a=float(self.gray[51][30]) - float(self.gray[52][30])
                #temp_diff=float(self.src_img[next_x][next_y])-float(self.src_img[first_x][first_y])
                print('a',a)
                #if temp_diff>self.threshold:
                   # pass
                   # diff[j][i]=diff[j][i]+temp_diff[j][i]
                self.location_x=next_x
                self.location_y=next_y
        # self.find_point()
        # self.get_result()



    def find_point(self,other):
        pass

        return 0
    def set_threshold(self,value):
        self.threshold=value
    def set_result_type(self,type):
        self.result_type=type
    def set_polar_property(self,property):
        self.polar_property=property

if __name__=='__main__':
    rect_corn=list()
    rect_corn.append(myPoint(50,30))
    rect_corn.append(myPoint(100,30))
    rect_corn.append(myPoint(100, 60))
    rect_corn.append(myPoint(50, 60))
    calliper=Calliper(rect_corn)
