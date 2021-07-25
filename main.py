# This file uses mediapipe for face detection.
import cv2
import mediapipe as mp
import time

# Setting for all parameters
SHOW_CONFIDENCE = True
SHOW_FPS = True
BLUR_FACE = True
MINIMUM_CERTANITY = 0.5

# Here the image is loaded for the test of correct operation
# VideoCapture() takes filename as argument or you can type device index.
captured_video = cv2.VideoCapture(0)

# Defining initial value for previousTIme (this is necessary for FPS)
previousTime = 0
while True:
    # Getting frame from video.
    # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
    success, frame = captured_video.read()

    # In order for the algorithm to work properly, we need to present the frame in RGB model.
    # We are using cv2 function to scale img from BGR to RGB.
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp.solutions.face_detection.FaceDetection(MINIMUM_CERTANITY).process(imgRGB)

    # In code below we are showing face's bounding box and also percentage certainty that a face has been detected.
    if results.detections:

        for id, detection in enumerate(results.detections):
            # Getting all data about frame
            frame_height, frame_width, frame_channel = frame.shape

            # Getting basic data for box around face. All of it is inside of detection.
            x = int(detection.location_data.relative_bounding_box.xmin * frame_width)
            y = int(detection.location_data.relative_bounding_box.ymin * frame_height)
            w = int(detection.location_data.relative_bounding_box.width * frame_width)
            h = int(detection.location_data.relative_bounding_box.height * frame_height)


            if BLUR_FACE:
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
                # Also it's returning face.
                face = (cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 2))
                # Now we are blurring face using medianBlur
                face[y:y + h, x:x + h] = cv2.medianBlur(face[y:y + h, x:x + h], 35)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

            if SHOW_CONFIDENCE:
                cv2.putText(frame, f"{int(detection.score[0]*100)}%", (x, y-20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    # Calcute FPS
    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime
    if SHOW_FPS:
        cv2.putText(frame,f"fps{int(fps)}", (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,0),2)
    cv2.imshow('Face Anonymization', frame)

    # The function responsible for waiting for a key to be pressed in order not to close the window with the frame.
    # After the modifications compared to the previous version, press the ESC key to interrupt program execution.
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
captured_video.release()
cv2.destroyAllWindows()