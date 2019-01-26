import cv2
from enum import Enum
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
qimg=QImage()
qimg.load(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.png")
print(qimg.width(),qimg.height())

src=cv2.imread(r"C:\\Users\\Administrator\\Desktop\\CV-Team\\CV-Team\\image\\cv_team.png")
print(src.shape)

this is test for my gihub





