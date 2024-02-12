# Demo for Motion Detection and conditional facial detection
# By Matthew Fitzgerald

import cv2
import dlib
import numpy as np

webcam_Capture = cv2.VideoCapture(0)
unused_tuple_var, webcam_frame1 = webcam_Capture.read()
unused_tuple_var2, webcame_frame2 = webcam_Capture.read()

face_detector = dlib.get_frontal_face_detector()

#saved regions of interest varr/arr

#this is a trained model provided from dlib that helps with facial detection
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
	# Motion Detection Section
	frame_difference = cv2.absdiff(webcam_frame1, webcame_frame2)
	convert_to_grayscale = cv2.cvtColor(frame_difference, cv2.COLOR_BGR2GRAY)
	#erosion operation on the image
	image_blur = cv2.GaussianBlur(convert_to_grayscale, (5, 5), 0)
	unused_tuple_var3, threshold = cv2.threshold(image_blur, 20, 255, cv2.THRESH_BINARY)
	image_dilation = cv2.dilate(threshold, None, iterations= 3)
	image_contours, unused_tuple_var4 = cv2.findContours(image_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


	for image_contour in image_contours:
		if cv2.contourArea(image_contour) < 2000:
			continue
		x, y, w, h = cv2.boundingRect(image_contour)
		cv2.rectangle(webcam_frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

		# Facial Detection in Detected Motion Region
		region_of_interest = webcam_frame1[y:y+h, x:x+w]
		possible_faces = face_detector(region_of_interest)
		for possible_face in possible_faces:
			facial_landmarks = shape_predictor(region_of_interest, possible_face)
			for n in range(0, 68):
				x = facial_landmarks.part(n).x
				y = facial_landmarks.part(n).y
				cv2.circle(region_of_interest, (x, y), 2, (255, 0, 0), -1)
		# then do something (if face stays within region of interest, then print face is staying)



	cv2.imshow("webcam_feed", webcam_frame1)
	webcam_frame1 = webcame_frame2
	unused_tuple_var_5, webcame_frame2 = webcam_Capture.read()
	# run through regions of interest

	if cv2.waitKey(1) & 0xFF == ord('q'):
		webcam_Capture.release()
		cv2.destroyAllWindows()
		break


		# temp array of possible faces if the absdif calculation didn't return anything
		# thread running for the facial analysis post-detection
		# find face (contours), grab next image, give next image to face tracker then break
		# array of facial coordinates, search in contours for the face if no face
		# if face detected stop searching for motion or handle both by keeping face in coordinates


		#erosion, non-moving face handling in face detected region
