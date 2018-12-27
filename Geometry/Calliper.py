import numpy as np
from  numpy import linalg as LA
import math
import cv2

class Calliper:
    def __init__(self,rect_corners):
        self.src_img=cv2.imread('./image/cv_team.jpg',cv2.COLOR_BGR2GRAY)
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
        if theta==0:
            print('in a line')
            return
        AB_count = int(LA.norm(AB))
        AD_count = int(LA.norm(AD))
        diff=np.zeros(AB_count,AD_count)
        for i in range (AD_count):
            unit_AD=i*AD/AD_count
            first_x = round(self.A.x + unit_AD[0])
            first_y = round(self.A.y + unit_AD[1])
            self.location_x=first_x
            self.location_y=first_y
            for j in range(AB_count-1):
                unit_AB=(j+1)*AB/AB_count
                next_x = round(first_x + unit_AB[0])
                next_y = round(first_y + unit_AB[1])
                temp_diff=self.src_img[next_x][next_y]-self.src_img[first_x][first_y]
                if temp_diff>self.threshold:
                    diff[j][i]=diff[j][i]+temp_diff[j][i]
                self.location_x=next_x
                self.location_y=next_y
        self.find_point()
        self.get_result()



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
    pass