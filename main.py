import divide_video
import find_and_blur_faces
import list_of_files
import time
import warnings


warnings.simplefilter("ignore", UserWarning)
print(f'Program started {time.strftime("%H:%M:%S", time.localtime())}')
list_of_files = list_of_files.get_list_of_files()
print(f'Total {len(list_of_files)} to blur faces and slice into frames')
for file in list_of_files:
    if '.mp4' in file:
        path_to_file = 'input/'+file
        print(path_to_file)
        folder_path = divide_video.divide_video_into_frames(path_to_file)
        print(folder_path)
        find_and_blur_faces.find_and_blur_faces(folder_path)

print(f'Program ended {time.strftime("%H:%M:%S", time.localtime())}')









