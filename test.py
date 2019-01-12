import numpy
import scipy
import scipy.linalg
from scipy import optimize as optimize
# A=numpy.zeros([5,1])
# B=numpy.zeros([5,1])
# A[0][0]=0
# A[1][0]=1
# A[2][0]=2
# A[3][0]=3
# A[4][0]=4
# B[0][0]=1
# B[1][0]=2
# B[2][0]=3
# B[3][0]=4
# B[4][0]=5
A=[1,2,3,4,5,6]
B=[2,3,4,5,6,7]
def fun_1(x,A,B):
    return A*x+B
A1,B1 =optimize.curve_fit(fun_1,A, B)[0]
print('y=%dx+%d'%(A1,B1))
