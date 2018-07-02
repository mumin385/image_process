import numpy as np
from matplotlib import pyplot as plt
import cv2

def myfunc(i):
    pass # do nothing

cv2.namedWindow('title') # create win with win name

#contrast trackbar
cv2.createTrackbar('contrast', # name of value
                   'title', # win name
                   0, # min
                   40, # max
                   myfunc) # callback func

#RGB trackbar
cv2.createTrackbar('R', 'title', 1, 5, myfunc)
cv2.createTrackbar('G', 'title', 1, 5, myfunc)
cv2.createTrackbar('B', 'title', 1, 5, myfunc)

#filterling trackbar
cv2.createTrackbar('gauss','title', 0, 10, myfunc)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while(True):

    ret, frame = cap.read()
    if not ret: continue


    v = cv2.getTrackbarPos('contrast',  # get the value
                           'title')  # of the win

#contrast process
    lookUpTable = np.zeros((256, 1), dtype = 'uint8')

    for i in range(256):
        if v == 0:
            lookUpTable[i][0] = 0
        else:
            lookUpTable[i][0] = 255 * pow(float(i) / 255, 1.0 / (v*0.1))

    frame = cv2.LUT(frame, lookUpTable)

#RGB process
    r = cv2.getTrackbarPos('R', 'title')
    g = cv2.getTrackbarPos('G', 'title')
    b = cv2.getTrackbarPos('B', 'title')

    frame[:,:,2] *= r
    frame[:,:,1] *= g
    frame[:,:,0] *= b

#filtering process
    x = cv2.getTrackbarPos('gauss','title')

    if x != 0:
        kernel = np.ones((x,x),np.float32)/(x**2)
        frame = cv2.filter2D(frame,-1,kernel)
    else:
        kernel = np.ones((1,1),np.float32)
        frame = cv2.filter2D(frame,-1,kernel)

    cv2.imshow('title', frame)  # show in the win

    k = cv2.waitKey(1)
    if k == ord('q') or k == 27:
        break



cap.release()
cv2.destroyAllWindows()
