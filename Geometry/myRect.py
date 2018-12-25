from Geometry.myPoint import myPoint
import math

class myRect:
    def __init__(self,center,width,height,direction=myPoint(1,0)):
        self.center=center
        self.width=width
        self.height=height
        self.direction=direction.normalized()
        vwidth=self.direction*self.width
        self.direction_w=myPoint(-self.direction.y,self.direction.x)
        vheight=self.direction_w*self.height
        self.A = self.center - vwidth / 2 - vheight / 2     #width是x方向       ab,x方向为正方向
        self.B = self.center + vwidth / 2 - vheight / 2     #
        self.C = self.center + vwidth / 2 + vheight / 2
        self.D = self.center - vwidth / 2 + vheight / 2
    def resize_by_A(self,point):
        diagonal_vec=self.C-point
        diagonal=diagonal_vec.norm()
        cosTheta=self.direction.x*diagonal_vec.normalized().x+self.direction.y*diagonal_vec.normalized().y
        sinTheta=math.sqrt(abs(1-cosTheta*cosTheta))
        return myRect((point+self.C)*0.5,abs(diagonal*cosTheta),abs(diagonal*sinTheta),self.direction)
    def resize_by_B(self,point):
        diagonal_vec=self.D-point
        diagonal=diagonal_vec.norm()
        cosTheta=self.direction.x*diagonal_vec.normalized().x+self.direction.y*diagonal_vec.normalized().y
        sinTheta=math.sqrt(1-cosTheta*cosTheta)
        return myRect((point+self.D)*0.5,abs(diagonal*cosTheta),abs(diagonal*sinTheta),self.direction)
    def resize_by_C(self,point):
        diagonal_vec=self.A-point
        diagonal=diagonal_vec.norm()
        cosTheta=self.direction.x*diagonal_vec.normalized().x+self.direction.y*diagonal_vec.normalized().y
        sinTheta=math.sqrt(1-cosTheta*cosTheta)
        return myRect((point+self.A)*0.5,abs(diagonal*cosTheta),abs(diagonal*sinTheta),self.direction)
    def resize_by_D(self,point):
        diagonal_vec=self.B-point
        diagonal=diagonal_vec.norm()
        cosTheta=self.direction.x*diagonal_vec.normalized().x+self.direction.y*diagonal_vec.normalized().y
        sinTheta=math.sqrt(1-cosTheta*cosTheta)
        return myRect((point+self.B)*0.5,abs(diagonal*cosTheta),abs(diagonal*sinTheta),self.direction)
    def rotate(self,alpha):
        new_direction_point=self.direction.rotate_by(self.center,alpha)
        new_direction=(new_direction_point-self.center).normalized()
        return myRect(self.center,self.width,self.height,new_direction)
    def rotate_to(self,point):
        new_direction=(point-self.center).normalized()
        return myRect(self.center,self.width,self.height,new_direction)
    def rotate_by(self,center,alpha):
        pass

    def scaling(self,other):
        pass





if __name__=='__main__':
    center=myPoint(1,1)
    height=2
    width=2
    dir=myPoint(-1,0)
    point2=myPoint(4,4)
    rect=myRect(center,height,width,dir)
    rect1=rect.resize_by_A(point2)
    print('rect1:',rect1.A,rect1.B,rect1.C,rect1.D)



    #rect.resize_by_A(point2)



