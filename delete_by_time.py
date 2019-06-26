import os

requeried_space = 1
limit = 2

def find_free_space():
    result=os.statvfs('/')
    block_size=result.f_frsize
    total_blocks=result.f_blocks
    total_size=total_blocks*block_size/giga
    free_blocks=result.f_bfree
    free_size=free_blocks*block_size/giga
    return free_size

def find_list():
    path_ = os.getcwd()
    files = os.listdir(path_)
    return files(path_)


def find_file_date_modification(path_to_file):
    time_modification = os.stat(path_to_file)
    date_modification = time.ctime(time_modification.st_mtime)
    return date_modification


def sorting_by_time():
    pass


def find_older_files():
    pass

def delete_by_category():
    pass


def delete_file(filename):
    os.remove(filename)




