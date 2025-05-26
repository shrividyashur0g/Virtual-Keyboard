import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(mode=False, maxHands=2,detectionCon= 1)

keys=[["Q","W","E","R","T","Y","U","I","O","P"],
     ["A","S","D","F","G","H","J","K","L",";"],
     ["Z","X","C","V","B","N","M",",",".","/"]]

ClickedText=""
keyboard=Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos , (x+w, y+h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text,(x+25,y+71), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img



class Button():
    def __init__(self, pos,text,size=[91,91]):
        self.pos = pos
        self.text = text
        self.size = size

#myButton= Button([100,100],'Q',)
#myButton1= Button([200,100],'W',)
#myButton2= Button([300,100],'E',)
#myButton3= Button([400,100],'R',)
buttonList=[]

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key, ))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y=button.pos
            w, h = button.size
            if x<lmList[8][0]<x+w and y<lmList[8][1]< y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 128), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 71), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l,_,_=detector.findDistance(8,12, img)
                if l<50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 71), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    ClickedText+=button.text
                    sleep(0.8)

    cv2.rectangle(img, (55,345),(700,450), (128, 0, 128), cv2.FILLED)
    cv2.putText(img, ClickedText, (60,425), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

   #myButton= Button([100,100],'Q',)

    #cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), cv2.FILLED)
    #cv2.putText(img, 'Q', (125, 180), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)

    #img= myButton.draw(img)
    #img = myButton1.draw(img)
    #img = myButton2.draw(img)
    #img=myButton3.draw(img)



    cv2.imshow('Camera', img)
    cv2.waitKey(1)