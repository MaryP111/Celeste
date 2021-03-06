import numpy as np
import cv2
lego_cascade = cv2.CascadeClassifier('increased_lots/cascade.xml')
for i in range(1,19):	
	img = cv2.imread('tests/{0}.jpg'.format(i))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	legos = lego_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in legos:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
