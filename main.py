import cv2
# First, you need to load the previously downloaded classifier available in the openCV repository
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Here, the image is loaded for the test of correct operation
img = cv2.imread('test.jpg')

# In order for the algorithm to work properly, we need to present the image in shades of gray.
# CV2 processes images in BGR which means: Blue, Green and Red.
# We need to scale this image down to shades of gray.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# The function responsible for detecting the face.
# It accepts 3 arguments which in turn mean: the input image (gray scale), scaleFactor and minNeighbours.
# scaleFactor specifies how much the image size is reduced with each scale.
# minNeighbours specifies how many neighbors each candidate rectangle should have to retain it.
# Last to parameters could be different, you should try to find best for your case.
# --------------------------------------------------------------------------------------------------
# As we can read on the website listed on the bottom of this code,
# faces contains a list of coordinates for the rectangular regions where faces were found.
# We use these coordinates to draw the rectangles in our image.
faces = face_cascade.detectMultiScale(gray, 1.1, 6)


# Create a rectangle around a founded face.
# cv2.rectangle() Parameters:
# Image -> img: It is the image on which rectangle is to be drawn.
# Start_point -> (x, y): It is the starting coordinates of rectangle,
# the coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
# End_point -> (x+w, y+h): It is the ending coordinates of rectangle,
# the coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
# Color -> (255, 0, 0): It is the color of border line of rectangle to be drawn,
# for BGR, we pass a tuple. eg: (255, 0, 0) for blue color.
# Thickness -> 2: It is the thickness of the rectangle border line in px,
# thickness of -1 px will fill the rectangle shape by the specified color.
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
# Display the output
# cv2.imshow() takes 2 arguments: window_name, image.
cv2.imshow('Face Detection - try on regular photo', img)

# The function responsible for waiting for a key to be pressed in order not to close the window with the picture
cv2.waitKey()

# Additional information
# This is part of tutorial founded here:
# https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# Also I have founded useful info about cv2.rectangle() here:
# This is part of tutorial founded here:
# https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# As test photo we have used this photo:
# https://pixabay.com/photos/meeting-team-workplace-group-1245776/
