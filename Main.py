from tensorflow.python.ops.summary_ops_v2 import image

from HSVmodule import *
from HGmodule import *
import handTracking as htm
import cordinateTracker as ct
import autopy
import time
### set UP ##################
wCam,hCam = 640,480
wScr,hScr=autopy.screen.size()
frameR,start= (200,20)
cap = cv2.VideoCapture(3)
cap.set(3,wCam)
cap.set(4,hCam)
#############################
########## def###############

def fixOutRange(X, x, left, right):
    if X < left or X > right:
        if X < left:
            x += abs(X - left)
            X = left
        if X > right:
            x -= abs(X - right)
            X = right
    return X, x
def fixOutRange2(image,cX,cY):
    imageShape = image.shape()

def fps(img,cTime,pTime):
    fps = 1 / (cTime - pTime)
    colourMap=(122,239,64)
    if int(fps) >10:
        colourMap=(122,239,64) # green
    elif int(fps) <10 :
        colourMap=(65,239,227) # yellow
    # elif int(fps) < 10 :
    #     colourMap= (65,65,239) # red
    cv2.putText(img, str(int(fps)), (550, 50), cv2.FONT_HERSHEY_PLAIN, 3, colourMap, 2)

def checkinZone(index,zone):
    XZONE, YZONE, xzone, yzone = zone
    x1, y1 = index
    if x1 < XZONE or x1 > xzone or y1 < YZONE or y1 >yzone:
        return 0
    return 1

# xUp, yUP) = (x1 - 160, y1+160)
#         (xDown, yDown) = (x1 + 160, y1 + 160)

#############################
pTime=0
zoneSize= (wCam - frameR -start,hCam - frameR -start)
zone=(start,start,wCam-frameR,hCam-frameR)

############################# call Module
HSVmodule = HSV()
predictModule = HGmodule()
ctModule =  ct.transferModule(start,zoneSize)
count =0
while True:
    # 0 , 38 , 0
    result, image= cap.read()
    image = cv2.flip(image,1)
    image = cv2.rotate(image, cv2.ROTATE_180)
    cv2.rectangle(image, (start, start), (wCam - frameR, hCam - frameR), (0, 255, 255), 2)  # draw Zone
    predcitScr = image.copy()[start:int(hCam-frameR), start:int(wCam-frameR)]
    cTime = time.time()

    ############################################
    hsv,index=HSVmodule.extractHand(predcitScr)
    if index is not None:
        cv2.circle(predcitScr,index,5,[255,0,0],-1)
        x1,y1=index
        ctModule.transfer(x1,y1)
         #######
        hsv = cv2.resize(hsv,(320,320))
        # locate=r"D:\FPT\Project\BinaryData3\raw"
        # cv2.imwrite(locate+"\\"+str(count)+".jpg",hsv)
        # count+=1
        # print(count)
        result=predictModule.predictGesture(hsv)
        cv2.putText(image, str(result), (320, 320), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (255, 0, 0), 3)
    fps(image,cTime,pTime)
    pTime = cTime
    cv2.imshow("predictScrenn", predcitScr)
    cv2.imshow("window",image)
    cv2.imshow("HSV",hsv)
    key= cv2.waitKey(1)
    if (cv2.getWindowProperty("window",cv2.WND_PROP_VISIBLE) < 1 ) :
        break
cap.release()
cv2.destroyAllWindows()

############################################
# detectImage = detector.findHands(image,draw=False)
# index,lmList, bbox = detector.findPosition(image, Index=8,draw=False)

# if index is not None and checkinZone(index,zone):
#     x1, y1 = index
#     XZONE, YZONE, xzone, yzone = zone
#     (xUp, yUP) = (x1 - 160, YZONE)
#     (xDown, yDown) = (x1 + 160, yzone)
#     xUp, xDown = fixOutRange(xUp, xDown, XZONE, xzone)
#     xDown, xUp = fixOutRange(xDown, xUp, XZONE, xzone)
#     # move mouse
#     ctModule.transfer(x1,y1)
#     #######
#     cv2.rectangle(image, (xUp, yUP), (xDown, yDown), (255, 255, 0))
#     hsv = hsv[start:yDown, xUp:xDown]
#     mask = HSVmodule.extractHand(hsv)
#     # predictMask = mask
#     cv2.imshow("HSV", hsv)
#     cv2.imshow("Predict Mask", mask)
# #     resutl=predictModule.predictGesture(mask)
# #     if resutl == "left click":
# #         ctModule.leftClick()
# #
# #     cv2.putText(image, str(resutl), (320, 320), cv2.FONT_HERSHEY_PLAIN, 3,
# #                 (255, 0, 0), 3)
# #
# # else:
# #     cv2.putText(image, "Cant find Hand", (200, 320), cv2.FONT_HERSHEY_PLAIN, 2,
# #                 (255, 0, 0), 2)
#####################################################################################