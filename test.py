import numpy as np
from numpy import linalg as LA
import cv2
import os

src_img = cv2.imread('./image/gray_cat.jpg')
print(src_img[6][7])
temp_diff = np.zeros([6, 8])
img_arr=np.array(src_img)
a=float(src_img[4][4])-float(src_img[5][5])
print(a)



"""
gray_lwpImg=cv2.imread('./image/cat.jpg')
img=cv2.cvtColor(gray_lwpImg,cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray_cat.jpg",img)
img_arr=np.array(img)
aa=float(img_arr[100][100])-float(img_arr[99][99])




a=float(img[100][100])-float(img[99][99])
print(img.shape)
print(a,aa)


cv2.namedWindow('img')
cv2.imshow('img',img)

cv2.waitKey(0)
"""

# a = bytearray(os.urandom(2000))
# print(a)
# b = np.array(a)
# c=np
# print(b)
# b=b.reshape(40,50)
#
# aa=(float(b[0][1])-float(b[0][0]))
# print(aa)
# cv2.namedWindow('img')
# cv2.imshow('img',b)
#
# cv2.waitKey(0)



a=np.zeros([50,40])
print(a)

