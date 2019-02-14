# import cv2
#
# from PyQt5.QtGui import *
# qimg=QImage()
# qimg.load(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.png")
# print(qimg.width(),qimg.height())
#
# src=cv2.imread(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.png")
# print(src.shape)
from ctypes import *
print('a')
dll = CDLL(r'C:\Users\Administrator\Desktop\CV-Team\CV-Team\python_use_dll.dll')
print('b')
re=dll.dll.Initialization()
print(re)




