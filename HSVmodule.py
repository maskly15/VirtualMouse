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
        cv2.resizeWindow("HSV trackBar",320,160)
        cv2.createTrackbar("L-H", "HSV trackBar", 0, 179, self.Nothing)
        cv2.createTrackbar("L-S", "HSV trackBar", 40, 255, self.Nothing)
        cv2.createTrackbar("L-V", "HSV trackBar", 80, 255, self.Nothing)
        # cv2.createTrackbar("U-H", "HSV trackBar", 20, 20, self.Nothing)
        # cv2.createTrackbar("U-S", "HSV trackBar", 255, 255, self.Nothing)
        # cv2.createTrackbar("U-V", "HSV trackBar", 255, 255, self.Nothing)
    def Nothing(self,x):
        pass
        return None

    def fixOutRange(self,X,x,left,right):
        if X < left or X > right:
            if X < left:
                x += abs(X - left)
                X = left
            if X > right:
                x -= abs(X-right)
                X = right
        return X,x

    def centroid(self,max_contour):
        moment = cv2.moments(max_contour)
        if moment['m00'] != 0:
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])
            return cx, cy
        else:
            return None
    def cacultDistance(self,A,B):
        point1 = np.array(A)
        point2 = np.array(B)
        return np.linalg.norm(point1-point2)

    def draw_circles(self,frame, traverse_point):
        if traverse_point is not None:
            for i in range(len(traverse_point)):
                cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)
    def farthest_point(self,defects, contour, centroid):
        if defects is not None and centroid is not None:
            s = defects[:, 0][:, 0]
            s2=[]
            cx, cy = centroid
            for i in range(len(s)):
                yCheck = contour[s[i]][0][1]
                if yCheck <= cy:
                    s2.append(s[i])
            s =s2
            x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
            y = np.array(contour[s][:, 0][:, 1], dtype=np.float)
            xp = cv2.pow(cv2.subtract(x, cx), 2)
            yp = cv2.pow(cv2.subtract(y, cy), 2)
            dist = cv2.sqrt(cv2.add(xp, yp))
            dist_max_i = np.argmax(dist)


            if dist_max_i < len(s):
                farthest_defect = s[dist_max_i]
                farthest_point = tuple(contour[farthest_defect][0])
                return farthest_point
            else:
                return None
    def findIndex(self,c,palm):
        far_point = None
        if c is not None:
            max_cont = c
            hull = cv2.convexHull(max_cont, returnPoints=False)
            defects = cv2.convexityDefects(max_cont, hull)
            far_point = self.farthest_point(defects, max_cont, palm)
            # cv2.circle(image, far_point, 5, [0, 0, 255], -1)
        return far_point
            # self.draw_circles(image, self.traverse_point)
    def extractHand(self,image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        l_h = cv2.getTrackbarPos("L-H", "HSV trackBar")
        l_s = cv2.getTrackbarPos("L-S", "HSV trackBar")
        l_v = cv2.getTrackbarPos("L-V", "HSV trackBar")
        u_h = 20
        u_s = 255
        u_v = 255
        LB = np.array([l_h, l_s, l_v])
        UB = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, LB, UB)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        maxPoint =None
        index=None
        if len(cnts) != 0:
            c = max(cnts, key=cv2.contourArea)
            palm =self.centroid(c)
            cv2.circle(image, palm, 5, [255, 0, 255], -1)
            mask2 = np.zeros((mask.shape))
            cv2.fillPoly(mask2, pts=[c], color=(255, 255, 255))
            mask = mask2
            ###########################################################Find Index
            try:
                index =self.findIndex(c,palm)
            except:
                return np.zeros((mask.shape)),None
        else:
            return  np.zeros((mask.shape)),None
        # locate=r"D:\FPT\Project\BinaryData3\raw"
        # cv2.imwrite(locate+"\\"+str(name)+".jpg",mask)
        return mask,index





