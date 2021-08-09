import os

def get_list_of_files():
    filenames = next(os.walk("input/"), (None, None, []))[2]  # [] if no file
    tmp_list = []

    for file in filenames:
        if '.mp4' in file:
            folder_path_exist_check = file.replace(".mp4", "")
            CHECK_FOLDER = os.path.isdir("output/" + folder_path_exist_check+"/")
            if not CHECK_FOLDER:
                tmp_list.append(file)
    return tmp_list