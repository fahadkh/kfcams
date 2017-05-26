import numpy as np
import os
import cv2

dirname = 'data/images'
img1 = cv2.imread('C:\Users\danielfelixkim\Documents\dfk.jpg')


dog_filter = cv2.imread('dog_filter.png')



def facedetect(image):
	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')
	with open('face.jpg', 'wb') as f:
		f.write(image)	
#	print image
#	fi = cStringIO.StringIO(image)
#	print fi

	img1 = cv2.imread('face.jpg')
	img1 = convertToJpg(image)
	gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray1, 1.3, 5)

	centerFrame = (0,0)
	centerImage = (320,240)
	offsetImage = (106, 50)
	command = [0,0,0,0]

	#Detect Faces
	for (x,y,w,h) in faces:
		cv2.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
		centerFrame = x+w/2,y+h/2			
		cv2.rectangle(img1,(centerFrame[0],centerFrame[1]),(centerFrame[0],centerFrame[1]),(0,0,255),2)
		roi_gray = gray1[y:y+h, x:x+w]
		roi_color = img1[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		
	#Check if webcam should move
	if (not centerFrame[0] == 0 and not centerFrame[1] == 0):
		if (centerFrame[0] < centerImage[0]-offsetImage[0]):
			command[0] = 1
			command[2] = 0
		elif (centerFrame[0] > centerImage[0] + offsetImage[0]):
			command[0] = 1
			command[2] = 1
		if (centerFrame[1] < centerImage[1] - offsetImage[1]):
			command[1] = 1
			command[3] = 1
		elif (centerFrame[1] > centerImage[1] + offsetImage[1]):
			command[1] = 1
			command[3] = 0

	cv2.imwrite(os.path.join(dirname, 'img.png'),img1)
	return "cmd=" + "".join(str(x) for x in command)
	