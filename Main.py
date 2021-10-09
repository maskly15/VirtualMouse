from HSVmodule import *
from HGmodule import *
import handTracking as htm
import cordinateTracker as ct
import autopy
### set UP ##################
wCam,hCam = 640,480
frameR=100
wScr,hScr=autopy.screen.size()
print(wScr,hScr)
#############################

# print(wScr,hScr)
########## def###############
def fps(img,cTime,pTime):
    fps = 1 / (cTime - pTime)
    colourMap=(122,239,64)
    if int(fps) in range(61):
        colourMap=(122,239,64)
    elif int(fps) in range(100,200):
        colourMap=(65,239,227)
    elif int(fps) > 201 :
        colourMap= (65,65,239)
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, colourMap, 2)

#############################
detector= htm.handDetector(maxHands=1)
HSVmodule = HSV()
predictModule = HGmodule()
cap = cv2.VideoCapture(2)
cap.set(3,wCam)
cap.set(4,hCam)
ctModule =  ct.transferModule()
while True:
    # 0 , 38 , 0
    result, image= cap.read()
    image = cv2.flip(image,1)
    predcitScr = image.copy()[0:int(hCam-200), 0:int(wCam-200)]
    # image = cv2.rotate(image, cv2.ROTATE_180)
    # 1.Find Hand
    image = detector.findHands(image.copy(),draw=False)
    index,lmList, bbox = detector.findPosition(image, Index=8,draw=False)
    if index is not None:
        x1, y1 = index
        ctModule.transfer(image,x1,y1)
    ## Display###########
    mask = HSVmodule.extractHand(predcitScr)
    predictMask = mask
    resutl=predictModule.predictGesture(mask)
    cv2.putText(image, str(resutl), (320, 320), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cv2.imshow("predictScrenn", predcitScr)
    cv2.imshow("mask",mask)
    cv2.imshow("window",image)
    key= cv2.waitKey(1)
    if (cv2.getWindowProperty("window",cv2.WND_PROP_VISIBLE) < 1 ) :
        break
cap.release()
cv2.destroyAllWindows()