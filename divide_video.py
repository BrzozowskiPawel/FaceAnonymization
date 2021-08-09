import time
import cv2
import os
from termcolor import colored


def create_folder_for_frames(path):
    # Cutting .mp4 as folder should be only name of file.
    tmp = path.replace("input/","")
    folder_path = tmp.replace(".mp4", "")

    # Declaration of constants that are paths.
    MYDIR = "output/"+folder_path
    MYDIR_before = "output/"+folder_path+"/before"
    MYDIR_after = "output/"+folder_path+"/after"
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it (and subfolders).
    if not CHECK_FOLDER:
        if not os.path.isdir(MYDIR_before):
            os.makedirs(MYDIR_before)
        if not os.path.isdir(MYDIR_after):
            os.makedirs(MYDIR_after)
        return MYDIR

    else:
        message = "folder already exists! -> Delete 'output' folder or single one that already exists: "+MYDIR
        print(colored(message, 'red'))
        # If folder already exist we are exiting program with code 10.
        exit(10)


def divide_video_into_frames(path):
    # Start counting the time it took to complete this function
    start_time = time.time()

    # Creating variable that contain path to the folder
    folder_path = create_folder_for_frames(path)

    # Variables responsible for counting frames in the video.
    number_of_frame = 1

    # Here the image is loaded for the test of correct operation
    # VideoCapture() takes filename as argument or you can type device index.
    captured_video = cv2.VideoCapture(path)

    while True:
        # Getting frame from video.
        # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
        success, frame = captured_video.read()

        # Save the photo as consecutive numbers.
        if success:
            cv2.imwrite(folder_path+"/before/"+str(number_of_frame)+".jpg", frame)
            number_of_frame += 1
        elif not success:
            final_info = f"Process done (this took {round((time.time() - start_time), 2)} seconds), created {number_of_frame} frames from video in folder: {folder_path+'/before/'}"
            print(colored(final_info, 'green'))
            break
    return folder_path