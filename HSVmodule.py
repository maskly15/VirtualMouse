import cv2
import numpy as np
import os
import imutils
from HGmodule import *
import math
class HSV:
    def __init__(self):
        # 0 , 40 , 0
        cv2.namedWindow("HSV trackBar")
        cv2.resizeWindow("HSV trackBar",320,320)
        cv2.createTrackbar("L-H", "HSV trackBar", 0, 179, self.Nothing)
        cv2.createTrackbar("L-S", "HSV trackBar", 40, 255, self.Nothing)
        cv2.createTrackbar("L-V", "HSV trackBar", 80, 255, self.Nothing)
        cv2.createTrackbar("U-H", "HSV trackBar", 20, 20, self.Nothing)
        cv2.createTrackbar("U-S", "HSV trackBar", 255, 255, self.Nothing)
        cv2.createTrackbar("U-V", "HSV trackBar", 255, 255, self.Nothing)
    def Nothing(self,x):
        pass
        return None
    def indexCon(self,cnts,index):
        minDist = 99999
        minCon = 0
        for contor in cnts:
            dist = cv2.pointPolygonTest(contor,(index),measureDist= False)
            if dist == 1 or dist ==0:
                return contor
        return max(cnts, key=cv2.contourArea)

    def fixOutRange(self,X,x,left,right):
        if X < left or X > right:
            if X < left:
                x += abs(X - left)
                X = left
            if X > right:
                x -= abs(X-right)
                X = right
        return X,x


    def extractHand(self,image,index=None,zone = None,origin =None):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if index is not None:
            XZONE,YZONE,xzone,yzone =zone
            (x1,y1) =index
            (xUp, yUP) = (x1 - 160, y1)
            (xDown, yDown) = (x1 + 160, y1 + 320)
            xUp,xDown =self.fixOutRange(xUp,xDown,XZONE,xzone)
            xDown,xUp = self.fixOutRange(xDown, xUp, XZONE, xzone)
            yUP, yDown = self.fixOutRange(yUP, yDown, YZONE, yzone)
            yDown, yUP = self.fixOutRange(yDown, yUP, YZONE, yzone)
            cv2.rectangle(origin,(xUp,yUP),(xDown,yDown),(255,255,0))
            hsv = hsv[0:320, xUp:xDown]
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
            # if index is not None:
            #     c= self.indexCon(cnts,index)
            # else:
            c = max(cnts, key=cv2.contourArea)
            # print("IndexLocate",index)
            # print('cnts:',c)
            mask2 = np.zeros((mask.shape))
            cv2.fillPoly(mask2, pts=[c], color=(255, 255, 255))
            mask = mask2
        else:
            return  np.zeros((mask.shape))
        return mask





