# TODO before final release delete all unnecessary modules
import cv2
import divide_video
import find_and_blur_faces

folder_path = divide_video.divide_video_into_frames("test_video.mp4")
find_and_blur_faces.find_and_blur_faces(folder_path=folder_path)








