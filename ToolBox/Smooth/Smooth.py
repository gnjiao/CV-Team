import cv2
from matplotlib import pyplot as plt
class Smooth:
    def __init__(self):
        self.src_img=None
        self.kernel_size=5
        self.dst=None
    def Blur(self):
        if self.src_img is None:
            return -1
        blur=cv2.blur(self.src_img,(self.kernel_size,self.kernel_size))
        self.dst=blur
        # cv2.namedWindow('blur')
        # cv2.imshow('blur',blur)
        # cv2.waitKey()

    def GaussianBlur(self):
        if self.src_img is None:
            return -1
        blur=cv2.GaussianBlur(self.src_img,(self.kernel_size,self.kernel_size),0)
        self.dst = blur

    def MedianBlur(self):
        if self.src_img is None:
            return -1
        blur=cv2.medianBlur(self.src_img,self.kernel_size)
        self.dst = blur
    def BilateralFilter(self):
        if self.src_img is None:
            return -1
        blur=cv2.bilateralFilter(self.src_img,self.kernel_size,75,75)
        self.dst = blur



if __name__=='__main__':
    img = cv2.imread('../../image/CV_Team.jpg')
    smooth=Smooth()
    smooth.src_img=img
    smooth.Blur()