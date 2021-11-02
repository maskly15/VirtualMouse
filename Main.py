from tensorflow.python.ops.summary_ops_v2 import image

from Library import *

### set UP ##################
wCam,hCam = 640,480
wScr,hScr=autopy.screen.size()
frameR,start= (200,20)
cameraNum = 3
cap = cv2.VideoCapture(cameraNum) # This varibles depent what Camera will be used
cap.set(3,wCam)
cap.set(4,hCam)
labelList = [ "nothing","move", "Left", "Right"]
labelList2 = ["background","index","two","three"]
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


def Nothing(x):
    pass
    return None
#############################
pTime=0
zoneSize= (wCam - frameR -start,hCam - frameR -start)
zone=(start,start,wCam-frameR,hCam-frameR)

############################# call Module
HSVmodule = HSV()
predictModule = HGmodule()
ctModule =  ct.transferModule(start,zoneSize)
frameTake = 0
delay = 30 # the delay between command
countFrame =0
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
    hsv = cv2.resize(hsv,(320,320))
    rPredict = predictModule.predictGesture(hsv)
    rShow =  labelList2[rPredict] +": "+labelList[rPredict]
    cv2.putText(image, rShow, (100, 320), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    if frameTake >= delay and (rPredict == 2 ) :
        ctModule.leftClick()
        frameTake = 0
    if frameTake >= delay and (rPredict == 3) :
        ctModule.leftClick()
        ctModule.leftClick()
        frameTake = 0
    # if rPredict =="Right":
    #     ctModule.leftClick()
    #     ctModule.leftClick()
    #     time.sleep(1)
    if index is not None and rPredict is not "nothing":
        cv2.circle(predcitScr,index,5,[255,0,0],-1)
        x1,y1=index
        ctModule.transfer(x1,y1)
         ####################################################
    # save =hsv.copy()
    # locate=r"D:\FPT\Project\BinaryData\4"
    # cv2.imwrite(locate+"\\"+str(count)+".jpg",save)
    # count+=1
    # cv2.imwrite(locate+"\\"+str(count)+".jpg",cv2.rotate(save, cv2.ROTATE_180))
    # count += 1
    # cv2.imwrite(locate+"\\"+str(count)+".jpg",cv2.rotate(save, cv2.ROTATE_90_CLOCKWISE))
    # count +=1
    # cv2.imwrite(locate + "\\" + str(count) + ".jpg", cv2.flip(save,1))
    # count += 1
    # print(count)
#############################################################################################

    if frameTake <= delay:
        frameTake += 1
    fps(image,cTime,pTime)
    pTime = cTime
    cv2.putText(predcitScr, str(rPredict), (30, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)
    cv2.imshow("mousezone",predcitScr)
    cv2.imshow("window",image)
    cv2.imshow("HSV",cv2.resize(hsv,(320,320)))
    key= cv2.waitKey(1)
    if (cv2.getWindowProperty("window",cv2.WND_PROP_VISIBLE) < 1 ) :
        break
cap.release()
cv2.destroyAllWindows()

