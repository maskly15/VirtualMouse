from HSVmodule import *
from HGmodule import *
import handTracking as htm
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
cap = cv2.VideoCapture(2)
detector= htm.handDetector(maxHands=1)
HSVmodule = HSV()

while True:
    # 0 , 38 , 0
    result, image= cap.read()
    image = cv2.flip(image,1)
    # image = cv2.rotate(image, cv2.ROTATE_180)
    # 1.Find Hand
    window = detector.findHands(image.copy(),draw=False)
    index,lmList, bbox = detector.findPosition(window, Index=8,draw=False)
    cv2.rectangle(window, (0, 0), (320, 320),(0, 255, 255), 2)  # draw Hand Box
    image = image[0:320,0:320]
    print(index)
    ## Display###########
    cv2.imshow("Cam",image)
    mask = HSVmodule.extractHand(image.copy())
    cv2.imshow("mask",mask)
    cv2.imshow("window",window)
    key= cv2.waitKey(1)
    if (cv2.getWindowProperty("window",cv2.WND_PROP_VISIBLE) < 1 ) :
        break
cap.release()
cv2.destroyAllWindows()