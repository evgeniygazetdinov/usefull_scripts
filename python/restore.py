import os
import sys
import re


def find_in(name, specific):
    """check is by patern in  file"""
    res = False
    if specific in name:
        res = True
    return res

def is_name_has_more_whan_one_dot(name):
    """counting dots inside string"""
    return name.count('.') > 1

def check_fdb_exist_already(fdb_file):
    """rm already converted file for run without errors"""
    if os.path.isfile(os.getcwd() + '/' + fdb_file):
        os.system(f'rm {fdb_file}')


def convert_from_fbk_to_fdb(fbk_file):
    """main operation for converting"""
    file_without_extension = os.path.splitext(fbk_file)[0]
    FDB = f'{file_without_extension}.FDB'
    FBK = fbk_file
    print("""\n CONVERTER \n\n; "Convert from : {FBK}\n to: {FDB}\n\n""")
    check_fdb_exist_already(FDB)
    command=f"docker exec -it firebird gbak -user SYSDBA -password masterkey -C /firebird/data/{FBK} /firebird/data/{FDB};"
    print(command)
    os.system(command)
    return FDB


def main(filename):
    """rename firebird file if it need"""
    is_layer_file = False
    if find_in(filename, '.FBK'): 
        if is_name_has_more_whan_one_dot(filename) and find_in(filename, 'ENGINE'):
            names_list = filename.split('.') 
            first_name = names_list[0]
            os.system(f'mv {filename} {first_name}.FBK')
            filename = first_name + '.FBK'
        if find_in(filename, 'MYSHOP'):
            is_layer_file = True
            name_list = re.split('(_\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2})', filename, 1)
            name_without_date = name_list[0] + name_list[-1]
            os.system(f'mv {filename} {name_without_date}')
            filename = name_without_date
        converted_fdb_file =convert_from_fbk_to_fdb(filename)
        if is_layer_file:
            os.system(f'mv {converted_fdb_file} storage/')
        
    
if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    main(filename)
