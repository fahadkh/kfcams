import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('C:\Users\danie\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\Users\danie\Downloads\opencv\sources\data\haarcascades\haarcascade_eye.xml')

img1 = cv2.imread('dfk.jpg')
img2 = cv2.imread('harambe.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray1, 1.3, 5)
face2 = face_cascade.detectMultiScale(gray2, 1.3, 5)

faces = np.concatenate((faces, face2), axis=0)
print faces
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    centerFrame = x+w/2,y+h/2
    cv2.rectangle(img,(centerFrame[0],centerFrame[1]),(centerFrame[0],centerFrame[1]),(0,0,255),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()