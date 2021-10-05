import cv2
import numpy as np
import os
import imutils
from HGmodule import *

class HSV:
    def __init__(self):
        # 0 , 38 , 0
        cv2.namedWindow("HSV trackBar")
        cv2.createTrackbar("L-H", "HSV trackBar", 0, 179, self.Nothing)
        cv2.createTrackbar("L-S", "HSV trackBar", 38, 255, self.Nothing)
        cv2.createTrackbar("L-V", "HSV trackBar", 0, 255, self.Nothing)
        cv2.createTrackbar("U-H", "HSV trackBar", 25, 25, self.Nothing)
        cv2.createTrackbar("U-S", "HSV trackBar", 255, 255, self.Nothing)
        cv2.createTrackbar("U-V", "HSV trackBar", 255, 255, self.Nothing)

    def Nothing(self,x):
        pass
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
            # hull = cv2.convexHull(c,returnPoints=False)
            # defects = cv2.convexityDefects(c,hull)
            # cX,cY = centroid(c) # cordinate of center
            # cv2.circle(window, (cX, cY), 7, (0, 0, 255), -1)
            mask2 = np.zeros((mask.shape))
            cv2.fillPoly(mask2, pts=[c], color=(255, 255, 255))
            mask = mask2
        else:
            return  np.zeros((mask.shape))
        return mask





# cap = cv2.VideoCapture(3)
# cv2.namedWindow("HSV trackBar")
# cv2.createTrackbar("L-H","HSV trackBar",0,179,Nothing)
# cv2.createTrackbar("L-S","HSV trackBar",38,255,Nothing)
# cv2.createTrackbar("L-V","HSV trackBar",0,255,Nothing)
# cv2.createTrackbar("U-H","HSV trackBar",25,25,Nothing)
# cv2.createTrackbar("U-S","HSV trackBar",255,255,Nothing)
# cv2.createTrackbar("U-V","HSV trackBar",255,255,Nothing)
# module = HGmodule()
# num=0
HSVmodule = HSV()

# while True:
#     # 0 , 38 , 0
#     result, image= cap.read()
#     image = cv2.flip(image,1)
#     image = cv2.rotate(image, cv2.ROTATE_180)
#     window = image.copy()
#     cv2.rectangle(window, (0, 0), (320, 320),(0, 255, 255), 2)  # draw Hand Box
#     image = image[0:320,0:320]
#     cv2.imshow("Cam",image)
#     mask =HSVmodule.extractHand(image.copy())
#     cv2.imshow("mask",mask)
#     cv2.imshow("window",window)
#     # cv2.imshow("mask2",result)
#     key= cv2.waitKey(1)
#     if key == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()
