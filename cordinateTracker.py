import autopy
import numpy as np
import cv2
class transferModule():
    def __init__(self,wCam=640,hCam=480,start=0,frameR=200,smothing =10):
        self.wCam=wCam
        self.hCam= hCam
        self.wScr,self.hScr= autopy.screen.size()
        self.start =start
        self.frameR = frameR
        self.smothing = smothing
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
    def transfer(self,image,xIndex,yIndex):
        xTrans = np.interp(xIndex,(self.start,self.wCam - self.frameR ),(0,self.wScr))
        yTrans = np.interp(yIndex,(self.start,self.hCam - self.frameR ),(0,self.hScr))
        self.clocX = self.plocX + (xTrans - self.plocX) / self.smothing
        self.clocY = self.plocY + (yTrans - self.plocY) / self.smothing
        try:
            autopy.mouse.move(self.clocX,self.clocY)
            self.plocX,self.plocY = self.clocX , self.clocY
        except:
            pass
    def leftClick(self):
        autopy.mouse.click()