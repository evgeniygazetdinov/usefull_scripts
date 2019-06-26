import os
from delete_by_time import find_file_date_modification,delete_file


def comparer_dates(fir):
    #create dict where files older 2 weeks
    pass
    return older_filles

def find_files():
    #return list with full path
    path_ = os.getcwd()
    fil = os.listdir(path_+'/test_dir')
    files = map(os.path.abspath,fil)
    return files


def main():
    print(find_files())

if __name__ == "__main__":
    main()
