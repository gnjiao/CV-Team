import matplotlib.pyplot as plt
import numpy as np
from Geometry.myPoint import myPoint
import random

class FittingPolynomial:
    def __init__(self,points_input,order):
        self.order=order
        self.xa=[]
        self.ya=[]
        self.matAA=[]
        for i in range(len(points_input)):
            self.xa.append(points_input[i].x)
            self.ya.append(points_input[i].y)
    def execute(self):
        matA=[]
        for i in range(0, self.order + 1):
            matA1=[]
            #self.matA1.clear()
            for j in range(0, self.order + 1):
                tx = 0.0
                for k in range(0, len(self.xa)):
                    dx = 1.0
                    for l in range(0, j + i):
                        dx = dx * self.xa[k]
                    tx += dx
                matA1.append(tx)
            matA.append(matA1)
        matA=np.array(matA)

        matB=[]
        for i in range(0, self.order + 1):
            ty = 0.0
            for k in range(0, len(self.xa)):
                dy = 1.0
                for l in range(0, i):
                    dy = dy * self.xa[k]
                ty += self.ya[k] * dy
            matB.append(ty)
        matB = np.array(matB)
        self.matAA = np.linalg.solve(matA, matB)
        print(self.matAA)


if __name__=='__main__':
    # 手动输入点拟合
    point1=myPoint(1,0)
    point2=myPoint(2,5)
    point3=myPoint(3,7)
    point4=myPoint(4,8)
    point5=myPoint(5,9)
    point6=myPoint(6,12)
    xa=[]
    xa.append(point1.x)
    xa.append(point2.x)
    xa.append(point3.x)
    xa.append(point4.x)
    xa.append(point5.x)
    xa.append(point6.x)
    yaa=[]
    yaa.append(point1.y)
    yaa.append(point2.y)
    yaa.append(point3.y)
    yaa.append(point4.y)
    yaa.append(point5.y)
    yaa.append(point6.y)
    points=list()
    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)
    points.append(point5)
    points.append(point6)

    #生成随机点拟合

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xa, yaa, color='r', linestyle='', marker='*')
    fit=FittingPolynomial(points,15)
    fit.execute()
    xxa = np.arange(1, 6, 0.01)
    yya = []
    for i in range(0, len(xxa)):
        yy = 0.0
        for j in range(0, 15 + 1):
            dy = 1.0
            for k in range(0, j):
                dy *= xxa[i]
            dy *= fit.matAA[j]
            yy += dy
        yya.append(yy)
    ax.plot(xxa, yya, color='r', linestyle='-', marker='')
    ax.legend()
    plt.show()
    # print(points[2].y)
    # print(len(points))