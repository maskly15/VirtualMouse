from HSVmodule import *
from HGmodule import *


cap = cv2.VideoCapture(2)

HSVmodule = HSV()

while True:
    # 0 , 38 , 0
    result, image= cap.read()
    image = cv2.flip(image,1)
    # image = cv2.rotate(image, cv2.ROTATE_180)
    window = image.copy()
    cv2.rectangle(window, (0, 0), (320, 320),(0, 255, 255), 2)  # draw Hand Box
    image = image[0:320,0:320]
    cv2.imshow("Cam",image)
    mask = HSVmodule.extractHand(image.copy())
    cv2.imshow("mask",mask)
    cv2.imshow("window",window)
    key= cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()