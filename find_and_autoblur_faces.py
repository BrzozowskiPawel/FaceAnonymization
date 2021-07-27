# This file SSD model for face detection.
# To find out more about this visit: https://arxiv.org/abs/1512.02325
import cv2
import numpy as np
import time
from termcolor import colored
import save_video_functions

def get_preprocessed_frames(path=0,min_confidence = 0.4, show_confidence = True, show_fps = True, blur_face = True, show_video = True):
    # Start counting the time it took to complete this function
    start_time = time.time()

    # The most important variables regarding the output video
    filename = "autoblur.mp4"
    frames_per_second = 24
    res = '1080p'

    # Variables responsible for counting frames in the video.
    number_of_frames = 0

    if show_fps or show_confidence:
        print(colored('CAUTION! In the final version, it is recommended to set the show fps and show confidence flags to false.', 'red'))
    print('Starting to find and blur faces (automatically)')

    # https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
    prototxt_path = "weights/deploy.prototxt.txt"
    # https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
    model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    # Loading model, method that takes the model architecture and weights as arguments:
    model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    # Create a variable that holds all the frames. It will be returned from this function.

    # Here the image is loaded for the test of correct operation
    # VideoCapture() takes filename as argument or you can type device index.
    captured_video = cv2.VideoCapture('test_video.mp4')

    out = cv2.VideoWriter(filename, save_video_functions.get_video_type(filename), frames_per_second, save_video_functions.get_dims(captured_video, res))

    # Defining initial value for previousTIme (this is necessary for FPS)
    previousTime = 0

    while True:
        # Getting frame from video.
        # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
        success, frame = captured_video.read()

        number_of_frames += 1
        # Getting width and height of the image (as we are working on video, image is just a frame from video).
        try:
            h, w = frame.shape[:2]
        except AttributeError:
            print("There is no more frames (caught an exception)")
            break
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

            # Get the surrounding box coordinates and upscale them to original image
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int32)
            # get the face image
            face = frame[start_y: end_y, start_x: end_x]

            # If confidence is above value set on the beginning,
            # then blur the bounding box (face) apply gaussian blur to this face
            if confidence > min_confidence and blur_face:
                # Applying rectangular on detected face
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
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 255), 2)
                # Blurring
                face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 50)
                if show_confidence:
                    cv2.putText(frame, f"{int(confidence*100)}%", (start_x, start_y-20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

            elif confidence > min_confidence and not blur_face:
                # Applying rectangular on detected face
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 255), 2)
                if show_confidence:
                    cv2.putText(frame, f"{int(confidence * 100)}%", (start_x, start_y - 20), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 255), 2)

            # put the blurred face into the original image
            frame[start_y: end_y, start_x: end_x] = face

        if show_fps:
            # Calculate FPS
            currentTime = time.time()
            fps = 1 / (currentTime - previousTime)
            previousTime = currentTime
            cv2.putText(frame, f"fps{int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

        out.write(frame)

        if show_video:
            cv2.imshow('Face Anonymization (Auto process)', frame)

        # The function responsible for waiting for a key to be pressed in order not to close the window with the frame.
        # After the modifications compared to the previous version, press the ESC key to interrupt program execution.
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    # Release the VideoCapture object
    captured_video.release()
    # out.release()
    if show_video:
        cv2.destroyAllWindows()

    final_info = f"Process done, founded {number_of_frames} frames (this took {round((time.time() - start_time),2)} seconds)"
    file_save_info = f"File saved as {filename}"
    print(colored(final_info, 'green'))
    print(colored(file_save_info, 'blue'))
# Code above was made with help of this website:
# https://www.thepythoncode.com/article/blur-faces-in-images-using-opencv-in-python