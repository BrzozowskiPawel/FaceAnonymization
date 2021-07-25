# This file SSD model for face detection.
# To find out more about this visit: https://arxiv.org/abs/1512.02325
import cv2
import numpy as np
import time

# https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
prototxt_path = "weights/deploy.prototxt.txt"
# https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
# Loading model, method that takes the model architecture and weights as arguments:
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

MINIMUM_CONFIDENCE = 0.4
SHOW_CONFIDENCE = True
SHOW_FPS = True
BLUR_FACE = False

# Here the image is loaded for the test of correct operation
# VideoCapture() takes filename as argument or you can type device index.
captured_video = cv2.VideoCapture(0)

# Defining initial value for previousTIme (this is necessary for FPS)
previousTime = 0
while True:
    # Getting frame from video.
    # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
    success, frame = captured_video.read()

    # Getting width and height of the image (as we are working on video, image is just a frame from video).
    h, w = frame.shape[:2]
    # Gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1
    # Preprocess the image: resize and performs mean subtraction
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # Set the image into the input of the neural network
    model.setInput(blob)
    # Perform inference and get the result
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        # Getting confidence value
        confidence = output[i, 2]

        # Get the surrounding box cordinates and upscale them to original image
        box = output[i, 3:7] * np.array([w, h, w, h])
        # convert to integers
        start_x, start_y, end_x, end_y = box.astype(np.int32)
        # get the face image
        face = frame[start_y: end_y, start_x: end_x]

        # If confidence is above value set on the beginning,
        # then blur the bounding box (face) apply gaussian blur to this face
        if confidence > MINIMUM_CONFIDENCE and BLUR_FACE:
            # Applying rectangular on detected face
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 255), 2)
            # Blurring
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 50)
            if SHOW_CONFIDENCE:
                cv2.putText(frame, f"{int(confidence*100)}%", (start_x, start_y-20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        elif confidence > MINIMUM_CONFIDENCE and not BLUR_FACE:
            # Applying rectangular on detected face
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 255), 2)
            if SHOW_CONFIDENCE:
                cv2.putText(frame, f"{int(confidence * 100)}%", (start_x, start_y - 20), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 255), 2)

        # put the blurred face into the original image
        frame[start_y: end_y, start_x: end_x] = face

    # Calcute FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    if SHOW_FPS:
        cv2.putText(frame, f"fps{int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

    cv2.imshow('Face Anonymization', frame)

    # The function responsible for waiting for a key to be pressed in order not to close the window with the frame.
    # After the modifications compared to the previous version, press the ESC key to interrupt program execution.
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
captured_video.release()
cv2.destroyAllWindows()

# Code above was made with help of this website:
# https://www.thepythoncode.com/article/blur-faces-in-images-using-opencv-in-python