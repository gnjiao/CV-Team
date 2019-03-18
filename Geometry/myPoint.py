import math
class myPoint:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self, other):
        return myPoint(other.x+self.x,other.y+self.y)
    def __sub__(self, other):
        return myPoint(self.x-other.x,self.y-other.y)
    def __mul__(self, other):
        return myPoint(self.x*other,self.y*other)
    def __truediv__(self, other):
        return myPoint(self.x/other,self.y/other)
    def norm(self):
        return math.sqrt(self.x*self.x+self.y*self.y)
    def distance_to(self,other):
        return math.sqrt(pow(other.x-self.x,2)+pow(other.y-self.y,2))
    @staticmethod
    def translate_to(other):
        return other
    def rotate_by(self,other,alpha):
        v=self-other
        v_1=myPoint(math.cos(math.pi/180*alpha)*v.x-math.sin(math.pi/180*alpha)*v.y,math.sin(math.pi/180*alpha)*v.x+math.cos(math.pi/180*alpha)*v.y)
        return other+v_1
    def rotate_of(self,other,alpha):
        pass
    def normalized(self):
        mod=self.norm()
        if mod == 0:
            return myPoint(0,0)
        return myPoint(float(self.x/mod),float(self.y/mod))



if __name__=='__main__':
    point1=myPoint(2,0)
    point2=myPoint(0,0)

    print(point1.rotate_by(point2,90).x,point1.rotate_by(point2,90).y)