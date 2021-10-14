from HSVmodule import *
from HGmodule import *
import handTracking as htm
import cordinateTracker as ct
import autopy
import time
### set UP ##################
wCam,hCam = 640,480
frameR=200
wScr,hScr=autopy.screen.size()

print(wScr,hScr)
start = 0
#############################
########## def###############

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

#############################
pTime=0
detector= htm.handDetector(maxHands=1)
HSVmodule = HSV()
predictModule = HGmodule()
cap = cv2.VideoCapture(2)
cap.set(3,wCam)
cap.set(4,hCam)
ctModule =  ct.transferModule()
zone=(0,0,wCam-frameR,hCam-frameR)

count =0
while True:
    # 0 , 38 , 0
    result, image= cap.read()
    image = cv2.flip(image,1)
    predcitScr = image.copy()[0:int(hCam-frameR), 0:int(wCam-frameR)]
    # image = cv2.rotate(image, cv2.ROTATE_180)
    # 1.Find Hand

    cTime = time.time()
    image = detector.findHands(image,draw=False)
    index,lmList, bbox = detector.findPosition(image, Index=8,draw=False)
    if index is not None and checkinZone(index,zone):
        x1, y1 = index
        ctModule.transfer(image,x1,y1)
        mask = HSVmodule.extractHand(predcitScr,index,zone=zone,origin=image,name=count)
        predictMask = mask
        cv2.imshow("Predict Mask", mask)
        # print(count)
        # count+=1
        resutl=predictModule.predictGesture(mask)
        if resutl == "left click":
            ctModule.leftClick()
        else:
            ctModule.relaseKey()

        cv2.putText(image, str(resutl), (320, 320), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

    else:
        cv2.putText(image, "Cant find Hand", (320, 320), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

    fps(image,cTime,pTime)
    pTime = cTime
    # cv2.imshow("predictScrenn", predcitScr)
    cv2.rectangle(image, (start, start), (wCam - frameR, hCam - frameR), (0, 255, 255), 2)
    cv2.imshow("window",image)
    key= cv2.waitKey(1)
    if (cv2.getWindowProperty("window",cv2.WND_PROP_VISIBLE) < 1 ) :
        break
cap.release()
cv2.destroyAllWindows()