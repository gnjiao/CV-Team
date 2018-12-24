from Geometry.myPoint import myPoint
import math
class myCircle:
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius
        self.area=self.radius*self.radius*math.pi
        self.circumference=2*self.radius*math.pi

