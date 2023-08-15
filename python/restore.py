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

def is_engine_file(name):
    """check is engine file"""
    res = False
    if 'ENGINE' in name:
        res = True
    return res

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


def main(filename):
    """rename firebird file if it need"""
    if is_fbk_file(filename): 
        if is_name_has_more_whan_one_dot(filename) and is_engine_file:
            names_list = filename.split('.') 
            first_name = names_list[0]
            os.system(f'mv {filename} {first_name}.FBK')
            filename = first_name + '.FBK'
        
        convert_from_fbk_to_fdb(filename)
        
    
if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    main(filename)
