import cv2
import mediapipe as mp
import time

# From now we will be using mediapipe instead of haarcascade.

# Here the image is loaded for the test of correct operation
# VideoCapture() takes filename as argument or you can type device index.
captured_video = cv2.VideoCapture('test_video.mp4')

# Defining initial value for previousTIme (this is necessary for FPS)
previousTime = 0

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.8)
while True:
    # Getting frame from video.
    # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
    success, frame = captured_video.read()


    # In order for the algorithm to work properly, we need to present the frame in RGB model.
    # We are using cv2 function to scale img from BGR to RGB.
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    # In code below we are showing face's bounding box and also percentage certainty that a face has been detected.
    if results.detections:
        for id, detection in enumerate(results.detections):
            bounding_boxClass = detection.location_data.relative_bounding_box
            frame_height, frame_width, frame_channel = frame.shape
            bounding_box = int(bounding_boxClass.xmin * frame_width), int(bounding_boxClass.ymin * frame_height), \
                           int(bounding_boxClass.width * frame_width), int(bounding_boxClass.height * frame_height)

            cv2.rectangle(frame, bounding_box, (255, 0, 255), 2)
            cv2.putText(frame, f"{int(detection.score[0] * 100)}%", (bounding_box[0], bounding_box[1] - 20),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)


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


    # Calcute FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(frame, f"fps{int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)

    # Display the output
    # cv2.imshow() takes 2 arguments: window_name, frame.
    cv2.imshow('Face Detection - try on video', frame)

    # The function responsible for waiting for a key to be pressed in order not to close the window with the frame.
    # After the modifications compared to the previous version, press the ESC key to interrupt program execution.
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
captured_video.release()
cv2.destroyAllWindows()

# Additional information
# This is part of tutorial founded here:
# https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# Also I have founded useful info about cv2.rectangle() here:
# This is part of tutorial founded here:
# https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# As test video we have used this video:
# https://www.pexels.com/video/a-group-of-volunteers-setting-up-at-the-back-of-a-van-6646718/
