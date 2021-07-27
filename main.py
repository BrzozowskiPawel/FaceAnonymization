# TODO before final release delete all unnecessary modules
import cv2
import autoblur_ssd_model_save_as_video
import divide_video


#find_and_autoblur_faces.blur_faces_using_ssd_model_save_as_video(path="test_video.mp4")
folder_path = divide_video.divide_video_into_frames("test_video.mp4")
# for frame in frames:
#     cv2.imshow("TEST", frame)
#     input("Press Enter to continue...")






