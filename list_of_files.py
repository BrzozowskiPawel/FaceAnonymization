import os


# Function responsible for obtaining a list of files (with the .mp4 extension),
# that have not yet been subjected to obliteration.
# Thanks to this, you can send new files to the input directory without deleting the previously used ones.


def get_list_of_files():
    # Get all the files (their names) in the input folder
    filenames = next(os.walk("input/"), (None, None, []))[2]  # [] if no file
    tmp_list = []
    # Filtering whether a given file is in .mp4 format and also,
    # whether the folder for a given name has not been previously created.
    # When both conditions are true the filename (which actually is its path)
    # are added to the list which will be returned last.
    for file in filenames:
        if '.mp4' in file:
            folder_path_exist_check = file.replace(".mp4", "")
            CHECK_FOLDER = os.path.isdir("output/" + folder_path_exist_check + "/")
            if not CHECK_FOLDER:
                tmp_list.append('input/' + file)
    return tmp_list
