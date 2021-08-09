import divide_video
import find_and_blur_faces
import list_of_files
import time
from termcolor import colored
import warnings


warnings.simplefilter("ignore", UserWarning)
message = f'Program started {time.strftime("%H:%M:%S", time.localtime())}'
print(colored(message,'blue'))

list_of_files = list_of_files.get_list_of_files()
message_how_many_files = f'{len(list_of_files)} new files to blur faces and slice into frames.'
print(colored(message_how_many_files,'yellow'))

if len(list_of_files) > 0:
    for file in list_of_files:
        path_to_file = 'input/'+file
        folder_path = divide_video.divide_video_into_frames(path_to_file)
        find_and_blur_faces.find_and_blur_faces(folder_path)
elif len(list_of_files) == 0:
    print(colored("There is no new videos (mp4) to blur and slice.", 'red'))
    # If there is no new videos, code 20.
    exit(20)

message = f'Program ended {time.strftime("%H:%M:%S", time.localtime())}'
print(colored(message,'blue'))








