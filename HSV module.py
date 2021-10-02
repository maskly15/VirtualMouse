import cv2
import numpy as np
import os
import imutils
from HGmodule import *
def Nothing(x):
    pass
cap = cv2.VideoCapture(2)
cv2.namedWindow("HSV trackBar")
cv2.createTrackbar("L-H","HSV trackBar",0,179,Nothing)
cv2.createTrackbar("L-S","HSV trackBar",38,255,Nothing)
cv2.createTrackbar("L-V","HSV trackBar",215,255,Nothing)
cv2.createTrackbar("U-H","HSV trackBar",25,25,Nothing)
cv2.createTrackbar("U-S","HSV trackBar",255,255,Nothing)
cv2.createTrackbar("U-V","HSV trackBar",255,255,Nothing)
module = HGmodule()
num=0
while True:
    # 0 , 38 , 215
    result, image= cap.read()

    image = cv2.flip(image,1)
    # image = cv2.rotate(image, cv2.ROTATE_180)
    window = image.copy()
    cv2.rectangle(window, (0, 0), (320, 320),
                  (0, 255, 255), 2)  # draw Hand Box
    image = image[0:320,0:320]
    hsv= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H","HSV trackBar")
    l_s = cv2.getTrackbarPos("L-S", "HSV trackBar")
    l_v = cv2.getTrackbarPos("L-V", "HSV trackBar")
    u_h = cv2.getTrackbarPos("U-H", "HSV trackBar")
    u_s = cv2.getTrackbarPos("U-S", "HSV trackBar")
    u_v = cv2.getTrackbarPos("U-V", "HSV trackBar")
    LB = np.array([l_h,l_s,l_v])
    UB = np.array([u_h,u_s,u_v])
    mask = cv2.inRange(hsv,LB,UB)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print(cnts)
        # compute the center of the contour
    try:
        c = max(cnts, key = cv2.contourArea)
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    # draw the center of the shape on the image
        cv2.circle(window, (cX, cY), 7, (0, 0, 255), -1)
    except:
        pass



    result = cv2.bitwise_and(image,image,mask=mask)
    # gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # edged= cv2.Canny(gray,30,200)
    # paths =r"D:\FPT\Project\BinaryData\3"
    # name = str(num) + ".jpg"
    # path = os.path.join(paths,name)
    # cv2.imwrite(path,mask)
    # num +=1
    # print(num)
    # predict = module.predictGesture(result)
    # cv2.putText(image, str(predict), (40, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2)
    cv2.imshow("Cam",image)
    # contours, hierarchy = cv2.findContours(edged,
    #                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(window, contours, -1, (0, 255, 0), 3)
    cv2.imshow("mask",mask)
    cv2.imshow("window",window)
    cv2.imshow("mask2",result)
    key= cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
