from Geometry.myPoint import myPoint
import math
class myLine:
    def __init__(self,start,end):
        self.start_point=start
        self.end_point=end
        self.mid_point=(self.start_point+self.end_point)/2
        self.direction=(self.end_point-self.start_point).normalized()
        self.length=(self.end_point-self.start_point).norm()
    def angle_to(self,other):
        x=self.direction.x*other.direction.y-other.direction.x*self.direction.y
        y=self.direction.x*other.direction.x+self.direction.y*other.direction.y
        a=abs(math.atan2(x,y))
        print('a=',(180/math.pi)*a)
        return (180/math.pi)*a

    def sign_angle_to(self,other,clock_wise=0,negative=0):#逆时针为0，允许负值为1，默认逆时针方向，不允许负值
        if clock_wise:
            sign=-1
        else:
            sign=1
        a1=math.atan2(self.direction.y,self.direction.x)
        if a1<0:
            a1=a1+2*math.pi
        a2=math.atan2(other.direction.y,other.direction.x)
        if a2<0:
            a2=a2+2*math.pi
        a=sign*(a2-a1)
        if a<0 and not negative:
            a=a+2*math.pi
        if a>math.pi and negative:
            a=a-2*math.pi
        #print('a=',(180/math.pi)*a)
        return (180/math.pi)*a
    def is_parallel_to(self,other,precision=0.0000000001):
        a=self.angle_to(other)
        if a<precision:
            return True
        else:
            return False
    def is_perpendicular_to(self,other,precision=0.0000000001):
        dp=self.direction.x*other.direction.x+self.direction.y*other.direction.y
        if abs(dp)<precision:
            return True
        else:
            return False
    def intersect_with(self,other):
        if self.is_parallel_to(other):
            print('两直线平行')
        v=other.start_point-self.start_point
        d1=v.x*other.direction.y-v.y*other.direction.x
        d2=self.direction.x*other.direction.y-self.direction.y*other.direction.x
        t=d1/d2
        return self.start_point+(self.direction*t)
    def closest_point(self,point,must_be_on_segment=False):
        v=(point-self.start_point).normalized()
        v_point=point.normalized()
        dot_product=v.x*v_point.x+v.y*v_point.y
        if must_be_on_segment:
            if dot_product<0:
                dot_product=0
            if dot_product>self.length:
                l=dot_product
        along_vector=self.direction*dot_product
        return self.start_point+along_vector
    def to_point(self,point):
        pass










if __name__=='__main__':
    point1=myPoint(-2,5)
    point2=myPoint(2,5)
    point3=myPoint(1,0)
    point4 = myPoint(2, 8)
    line1=myLine(point1,point2)
    line2=myLine(point3,point4)
    p=line1.closest_point(point3)
    print('p:',p.x,p.y)
    print(line1.is_perpendicular_to(line2))

