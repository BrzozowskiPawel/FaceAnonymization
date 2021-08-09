import glob
import os
import cv2
import time
import face_detection
from termcolor import colored
import datetime

def draw_blur(image, bboxes):
    # get width and height of the image
    h, w = image.shape[:2]
    # gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1

    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]

        # get the face image
        face = image[y0: y1, x0: x1]
        # apply gaussian blur to this face
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        # put the blurred face into the original image
        image[y0: y1, x0: x1] = face





def find_and_blur_faces(folder_path):
    print("Blurring started. Please keep in mind that due to different kinds of hardware there could be warnings.")
    impaths = folder_path+"/before"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        "DSFDDetector",
        max_resolution=1080
    )

    number_of_files_before = len(os.listdir(folder_path + "/before/"))
    for index in range(number_of_files_before-1):
        image_path = folder_path+"/before/"+str(index+1)+".jpg"

        img = cv2.imread(image_path)
        t = time.time()
        dets = detector.detect(img[:, :, ::-1])[:, :4]
        draw_blur(img, dets)

        image_name = os.path.basename(image_path).split(".")[0]
        output_path = folder_path + "/after/" + f"{image_name}_out.jpg"
        cv2.imwrite(output_path, img)

        number_of_files_after = len(os.listdir(folder_path + "/after/"))
        percentage_done = (round((number_of_files_after/number_of_files_before)*100, 2))
        print(f"File: {image_name}_out.jpg saved in {output_path}, detection time: {time.time() - t:.2f} seconds. {percentage_done}% done.")

    print(colored("All photos blurred :) ", 'green'))

