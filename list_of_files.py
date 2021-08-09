from os import walk

def get_list_of_files():
    filenames = next(walk("input/"), (None, None, []))[2]  # [] if no file
    return filenames