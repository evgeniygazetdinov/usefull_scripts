import os
import sys

def is_fbk_file(name):
    """find is fbk file"""
    res = False
    if '.FBK' in name:
        res = True
    return res

def is_name_has_more_whan_one_dot(name):
    """counting dots inside string"""
    return name.count('.') > 1

def main(filename):
    """rename firebird file if it need"""
    if is_fbk_file(filename) and is_name_has_more_whan_one_dot(filename):
        names_list = filename.split('.') 
        first_name = names_list[0]
        os.system(f'mv {filename} {first_name}.FBK')
    
if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    main(filename)
