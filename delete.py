import os
import datetime
import re

def generate_limit():
    #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    limit = datetime.timedelta(hour = 1)
    return limit


def find_files():
    #return list with full path
    path_ = os.getcwd()
    fil = os.listdir(path_+'/test_dir')
    files = map(os.path.abspath,fil)
    return files


def return_name(path):
    filename = os.path.splitext(path)[0]
    name = filename.split('/')[-1]
    return name

def create_name_path(list_direct):
    #name-key is time of creation
    name_path ={}
    names_list = map(return_name,list_direct)
    for i in len(list_direct):
        name_path = {'{}'.format(names_list[i]):list_direct[i])}
    return name_path


def convert_name_to_datetime(name):
    #delete mp4 extens
    file = re.findall(r"[\w']+", name)
    #broke by digit
    w_ext = file[0].split('_')
    #CONVERT!!!!
    time_creation = datetime.time(year =int(w_ext[3]),month=int(w_ext[2]),day =int(w_ext[1]),
                                  hour = int(w_ext[6]),min = int(w_ext[7]),sec = int(month[8])
    #fix datetime
    return time_creation


def find_older_files(limit,name_path):
    older_files = []
    for name,path in name_path.items():
        time_creation = convert_name_to_datetime(name)
        if time_creation <= limit:
            older_files.append(path)
    return older_files

def delete_file(filename):
    os.remove(filename)


def main():
    list_direct =find_files()
    limit = generate_limit()
    name_path = create_name_path(list_direct)
    #convert_to_datetime inside find_older_files
    older_files = find_older_files(limit,name_path)
    delete_older_files = map(delete_file,older_files)


if __name__ == '__main__':
    main()
