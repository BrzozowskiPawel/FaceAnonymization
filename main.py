import divide_video
import find_and_blur_faces
import list_of_files
import warnings


warnings.simplefilter("ignore", UserWarning)
list_of_files = list_of_files.get_list_of_files()

for file in list_of_files:
    if '.mp4' in file:
        path_to_file = 'input/'+file
        folder_path = divide_video.divide_video_into_frames(path_to_file)
        # find_and_blur_faces.find_and_blur_faces(folder_path)









