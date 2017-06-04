import numpy as np
import os
import cv2

dirname = 'data/images'
# img1 = cv2.imread('C:\Users\danielfelixkim\Documents\hi_2people.jpg')
face_filter = cv2.imread('dog_filter.png')
rows,cols,channels = face_filter.shape



def facedetect(image):
	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')
	with open('face.jpg', 'wb') as f:
		f.write(image)	
#	print image
#	fi = cStringIO.StringIO(image)
#	print fi
	img1 = cv2.imread('face.jpg')
	image_rows,image_cols,image_channels = img1.shape
#	img1 = convertToJpg(image)
	gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
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

		# #Add Filters
		
		# face_filter_height  = int(round(h * 1.2))
		# face_filter_width  = int(round(face_filter_height * orig_filter_width / orig_filter_height))

		x1 = x 
		x2 = x + w
		y1 = y-50 
		y2 = rows+y-50

		# Check for clipping
		if x1 < 0:
			x1 = 0
		if y1 < 0:
			y1 = 0
		if x2 > image_rows:
			x2 = image_rows
		if y2 > image_rows:
			y2 = image_rows

		# Re-calculate the width and height of the mustache image
		filterWidth = x2 - x1
		filterHeight = y2 - y1
		# # Re-size the original image and the masks to the mustache sizes
		# # calcualted above


		# Now create a mask of logo and create its inverse mask also
		img2gray = cv2.cvtColor(face_filter,cv2.COLOR_BGR2GRAY)
		ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
		mask_inv = cv2.bitwise_not(mask)

		filter_apply = cv2.resize(face_filter, (filterWidth,filterHeight), interpolation = cv2.INTER_AREA)
		mask = cv2.resize(mask, (filterWidth,filterHeight), interpolation = cv2.INTER_AREA)
		mask_inv = cv2.resize(mask_inv, (filterWidth,filterHeight), interpolation = cv2.INTER_AREA)

		# I want to put logo on top-left corner, So I create a ROI
		roi = img1[y1:y2,x1:x2]
		# Now black-out the area of logo in ROI
		img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
		# Take only region of logo from logo image.
		img2_fg = cv2.bitwise_and(filter_apply,filter_apply,mask = mask)
		# Put logo in ROI and modify the main image
		dst = cv2.add(img1_bg,img2_fg)
		img1[y1:y2,x1:x2] = dst

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
	


# facedetect(img1)
# r = 600.0 / img1.shape[1]
# dim = (600, int(img1.shape[0] * r))
# img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow('res',img1)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
