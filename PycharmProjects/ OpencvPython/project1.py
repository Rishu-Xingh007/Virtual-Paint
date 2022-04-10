import cv2
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

mycolor=[[15,142,116,179,255,255],[21,76,69,74,247,255]]
mypoints=[]
mycolorvalues=[[246,0,0],[2,205,0]]

def findcolor(img,mycolor,mycolorvalues):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newpoints=[]
    for col in mycolor:
        lower = np.array(col[0:3])
        upper = np.array(col[3:6])
        mask = cv2.inRange(imghsv, lower, upper)
        cv2.imshow("mask",mask)
        x,y=contours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorvalues[count],cv2.FILLED)
        if(x!=0 and y!=0):
            newpoints.append([x,y,count])
        count+=1
    return newpoints
        # cv2.imshow(str(col[0]), mask)

def contours(img):
    contour, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            point = cv2.approxPolyDP(cnt, 0.022 * peri, True)
            x, y, w, h = cv2.boundingRect(point)
    return x+w//2, y

def drawOncanvas(mypoints,mycolorvalues):
    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, mycolorvalues[point[2]], cv2.FILLED)


while True:
    success,img = cap.read()
    imgResult = img.copy()
    newpoints=findcolor(img,mycolor,mycolorvalues)
    if len(newpoints)!=0:
        for newP in newpoints:
            mypoints.append(newP)
    if(len(mypoints)!=0):
        drawOncanvas(mypoints,mycolorvalues)
    cv2.imshow("Result",imgResult )
    # cap.release()
    # cv2.destroyAllWindows()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break