from Geometry.myPoint import myPoint
from Geometry.myLine import myLine

import math

class myCircle:
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius
        self.area=self.radius*self.radius*math.pi
        self.circumference=2*self.radius*math.pi

class my3Circle:
    def __init__(self,point1,point2,point3):
        line12=myLine(point1,point2)
        line23=myLine(point2,point3)
        if line12.is_parallel_to(line23):
            print('3 points in one line')
            return
        mid_point12 = (point1 + point2) * 0.5
        mid_point23 = (point2 + point3) * 0.5
        gradient12 = (point2.y - point1.y) / (point2.x - point1.x)
        gradient23 = (point3.y - point2.y) / (point3.x - point2.x)
        gradient1=-1/gradient12
        gradient2=-1/gradient23
        denominator=gradient2-gradient1
        nominator=mid_point12.y-(gradient1*mid_point12.x)+(gradient2*mid_point23.x)-mid_point23.y
        center_x=nominator/denominator
        center_y=gradient1*(center_x-mid_point12.x)+mid_point12.y
        self.center=myPoint(center_x,center_y)
        self.radius=self.center.distance_to(point1)
        self.area = self.radius* self.radius * math.pi
        self.circumference = 2 * self.radius * math.pi

if __name__=='__main__':
    p1=myPoint(2,0)
    p2=myPoint(0,2)
    p3=myPoint(-2,0)
    circle=my3Circle(p1,p2,p3)
    print(circle.center.x,circle.center.y,circle.radius)
