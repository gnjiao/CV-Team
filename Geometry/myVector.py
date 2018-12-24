import numpy
class myVector1x2:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vector=numpy.matrix([self.x,self.y])
    def __add__(self, other):
        return numpy.matrix([self.x + other.x,self.y + other.y])
    def __sub__(self, other):
        return numpy.matrix([self.x - other.x, self.y - other.y])
    def __mul__(self, other):
        return numpy.matrix([self.x * other, self.y * other.y])
    def __truediv__(self, other):
        return numpy.matrix([self.x / other, self.y / other.y])
class myVector2x1:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vector=numpy.matrix([[self.x][self.y]])

class myVector2x2:
    def __init__(self,m11,m12,m21,m22):
        self.m11=m11
        self.m12=m12
        self.m21=m21
        self.m22=m22
        self.vector=numpy.matrix([[m11,m12],[m21,m22]])
