import cv2
import numpy as np
import pygame
pygame.init()
cap=cv2.VideoCapture(0)

while True:
    _ ,frame = cap.read()
    frame = frame.astype('uint8')
    
    #color space conversion
    gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #draw rectangles
    x1=103
    x2=241
    x3=391
    x4=529
    y1=y4=411
    y2=y3=306
    y4=y1
    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)

    #applyblur and remove noise
    gs = cv2.GaussianBlur(gs,(9,9), 0)
    gs = cv2.medianBlur(gs,5)

    #circle detction
    gray = cv2.adaptiveThreshold(gs,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=35,
                               minRadius=0, maxRadius=150)

    #play audio and plot circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            if (i[0]>x1 and i[0]<x2) and (i[1]>y1 and i[1]<y2):
                snare=pygame.mixer.Sound('snare.wav')
                snare.play()
            elif (i[0]>x3 and i[0]<x4) and (i[1]>y3 and i[1]<y4):
                drum=pygame.mixer.Sound('drum.wav')
                drum.play()
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),3)
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),1)

    #flip image
    gray=cv2.flip(gray,1)
    frame=cv2.flip(frame,1)

    #show frames and mask
    cv2.imshow('mask', gray)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
