import numpy as np
import cStringIO
import binascii
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	
#	print image
#	fi = cStringIO.StringIO(image)
#	print fi

img1 = cv2.imread('face.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray1, 1.3, 5)

centerFrame = (0,0)

for (x,y,w,h) in faces:
    cv2.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
    centerFrame = x+w/2,y+h/2
    cv2.rectangle(img1,(centerFrame[0],centerFrame[1]),(centerFrame[0],centerFrame[1]),(0,0,255),2)
    roi_gray = gray1[y:y+h, x:x+w]
    roi_color = img1[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imwrite('detect_image.png',img1)
print str(centerFrame)
