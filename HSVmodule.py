import cv2
import numpy as np
import os
import imutils
from HGmodule import *

class HSV:
    def __init__(self):
        # 0 , 38 , 0
        cv2.namedWindow("HSV trackBar")
        cv2.resizeWindow("HSV trackBar",320,320)
        cv2.createTrackbar("L-H", "HSV trackBar", 0, 179, self.Nothing)
        cv2.createTrackbar("L-S", "HSV trackBar", 38, 255, self.Nothing)
        cv2.createTrackbar("L-V", "HSV trackBar", 0, 255, self.Nothing)
        cv2.createTrackbar("U-H", "HSV trackBar", 25, 25, self.Nothing)
        cv2.createTrackbar("U-S", "HSV trackBar", 255, 255, self.Nothing)
        cv2.createTrackbar("U-V", "HSV trackBar", 255, 255, self.Nothing)
    def Nothing(self,x):
        pass


        return None
    def extractHand(self,image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        l_h = cv2.getTrackbarPos("L-H", "HSV trackBar")
        l_s = cv2.getTrackbarPos("L-S", "HSV trackBar")
        l_v = cv2.getTrackbarPos("L-V", "HSV trackBar")
        u_h = cv2.getTrackbarPos("U-H", "HSV trackBar")
        u_s = cv2.getTrackbarPos("U-S", "HSV trackBar")
        u_v = cv2.getTrackbarPos("U-V", "HSV trackBar")
        LB = np.array([l_h, l_s, l_v])
        UB = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, LB, UB)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) != 0:
            c = max(cnts, key=cv2.contourArea)
            mask2 = np.zeros((mask.shape))
            cv2.fillPoly(mask2, pts=[c], color=(255, 255, 255))
            mask = mask2
        else:
            return  np.zeros((mask.shape))
        return mask





