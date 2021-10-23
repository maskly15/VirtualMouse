import autopy
import numpy as np
# from autopy.mouse import LEFT_BUTTON, RIGHT_BUTTON
# from autopy.key import *
# from autopy import *
# import cv2
# from matplotlib.widgets import Button
# from sklearn.linear_model import Lars
import  pyautogui as auto


class transferModule():
    def __init__(self,start,zoneSize,smothing =10):
        self.wCam, self.hCam= zoneSize
        self.wScr,self.hScr= autopy.screen.size()
        self.start = start
        self.smothing = smothing
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
    def transfer(self,xIndex,yIndex):
        xTrans = np.interp(xIndex,(self.start,self.wCam  ),(0,self.wScr))
        yTrans = np.interp(yIndex,(self.start,self.hCam  ),(0,self.hScr))
        self.clocX = self.plocX + (xTrans - self.plocX) / self.smothing
        self.clocY = self.plocY + (yTrans - self.plocY) / self.smothing
        try:
            autopy.mouse.move(self.clocX,self.clocY)
            self.plocX,self.plocY = self.clocX , self.clocY
        except:
            pass
    def leftClick(self):
        autopy.mouse.click()

