import numpy
from Geometry.myPoint import myPoint
from Geometry.myLine import myLine

class FittingLine:
    def __init__(self,points_in):
        self.points=points_in
        self.iter=100
        self.thresh=1
        self.delete_count=0
        self.min_count=8       #拟合直线需要的最少点数
        self.k=self.iter
        self.line=None
        self.temp_line=None
        self.dist=100
        self.temp_dist=0
        self.ok_points=list()
        self.ng_points=list()
        self.temp_ok_points=list()
        self.temp_ng_points=list()
        self.i=0
    def Ransac(self):
        iter=0
        while iter<self.iter:
            choosed_index1 = numpy.random.randint(0, len(self.points))
            choosed_index2 = numpy.random.randint(0, len(self.points))
            # if self.points[choosed_index1].x==self.points[choosed_index2].x and self.points[choosed_index1].y==self.points[choosed_index2].y:
            #     continue

            # if self.points[choosed_index1].distance_to(self.points[choosed_index2])<2:
            #     self.i=self.i-1
            #     continue
            self.temp_line = myLine(self.points[choosed_index1], self.points[choosed_index2])
            self.temp_ok_points.clear()
            self.temp_ng_points.clear()
            self.temp_dist = 0
            for j in range(len(self.points)):
                dist=self.temp_line.to_point(self.points[j])
                self.temp_dist=dist+self.temp_dist
                if dist<self.thresh:
                    self.temp_ok_points.append(self.points[j])
                else:
                    self.temp_ng_points.append(self.points[j])

            if len(self.temp_ok_points)==len(self.ok_points):
                if self.temp_dist<self.dist:
                    self.dist=self.temp_dist
                    print(self.dist)
                    self.ok_points.clear()
                    self.ng_points.clear()
                    self.line=self.temp_line
                    self.ok_points = self.temp_ok_points.copy()
                    self.ng_points = self.temp_ng_points.copy()
            if len(self.temp_ok_points) > len(self.ok_points):
                #self.k=math.log(0.0001)/math.log(1-pow(len(self.ok_points)/len(self.points),2))
                self.ok_points.clear()
                self.ng_points.clear()
                self.line = self.temp_line
                self.ok_points=self.temp_ok_points.copy()
                self.ng_points=self.temp_ng_points.copy()
            #if self.i<self.k:
            #   break
            if len(self.ng_points)<self.delete_count:
                temp_count=self.delete_count-len(self.ng_points)
                #self.Delete_Points(self.ok_points,self.ng_points,temp_count)
            iter+=1
        print('dist:', self.temp_dist)
        #print(len(self.ok_points))
        if len(self.ok_points)>self.min_count:
            #if self.delete_count>len(self.ng_points):
            self.Delete_Points(self.ok_points,self.ng_points,self.delete_count)
            return self.ok_points,self.ng_points,self.line
        else:
            print('not enough points')
    @staticmethod
    def Delete_Points(ok_points,ng_points,delete_count):
        X=[]
        Y=[]
        for i in range(len(ok_points)):
            X.append(ok_points[i].x)
            Y.append(ok_points[i].y)
        a=numpy.polyfit(X,Y,1)
        print(a)


if __name__=='__main__':
    points=list()
    points.append(myPoint(1, 2.5))
    points.append(myPoint(2, 3.34))
    points.append(myPoint(3, 4.18))
    points.append(myPoint(4, 5.87))
    points.append(myPoint(5, 6.97))
    points.append(myPoint(6, 7.35))
    points.append(myPoint(7, 8.17))
    points.append(myPoint(8, 9.46))
    points.append(myPoint(9, 10.65))
    points.append(myPoint(10, 15.98))
    points.append(myPoint(11, 11.67))
    points.append(myPoint(12, 18))
    fit=FittingLine(points)
    ok,ng,line=fit.Ransac()
    print(len(ok))
    print(len(ng))
    print(line.start_point.x,line.start_point.y,line.end_point.x,line.end_point.y)










