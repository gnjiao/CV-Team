import numpy as np
from numpy import linalg as LA
import cv2

gray_lwpImg=cv2.imread('./image/cv_team.jpg',cv2.COLOR_BGR2GRAY)
a=gray_lwpImg[100][100]
print(a)
