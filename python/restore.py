import os
import sys
import re


LAYER_STORAGE = '/home/ev/code/storecraft/.deploy/data/firebird/storage/'
ENGINE_STORAGE = '/home/ev/code/storecraft/.deploy/data/firebird/'


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

def create_sql_with_layer():
	engine_work = """~/code/storecraft/.deploy/data/firebird/engine_work.sql"""
	layer_work = """~/code/storecraft/.deploy/data/firebird/layer_work.sql"""
	if not os.path.exists(engine_work):
		os.chdir(ENGINE_STORAGE)
		os.system('touch engine_work.sql')
	if not os.path.exists(layer_work):
		os.chdir(ENGINE_STORAGE)
		os.system('touch {}'.format(layer_work))
	my_file = open(engine_work, 'w+')

	my_file.write(f"""CONNECT '/firebird/data/{engine_name}' USER 'SYSDBA' PASSWORD 'masterkey';
		update engine_users eu set eu.passwd='pbkdf2_sha256$200$XfwDobs6u49X$O6lr8NFZiuAHwrcBfe+sSJhDQcjOV+DGG6j1HCNCtxU=' 
		where eu.phonenumber = '{phone}';update engine_bases set db_ip='db/3050, db_pass=masterkey""")
     
	my_file.close()
	my_file = open(layer_work, 'w+')
	my_file.write(f"""CONNECT '/firebird/data/storage/{layer_name}' USER 'SYSDBA' PASSWORD 'masterkey';
		update profile pr set pr.status='-1' where pr.uid != 468 and pr.status='1';""")
	my_file.close()
			
	return [engine_work, layer_work]

def do_job_with_firebird():
	sql_paths = create_sql_with_layer()
	os.chdir('/home/evgesha/code/storecraft/.deploy/data/firebird')
	os.system('docker exec -it firebird isql -q -i firebird/data/engine_work.sql')
	os.system('docker exec -it firebird isql -q -i firebird/data/layer_work.sql')
	[os.remove(path) for path in sql_paths]

def main(filename):
    """rename firebird file if it need"""
    is_layer_file = False
    if find_in(filename, '.FBK'): 
        print(filename)

        if is_name_has_more_whan_one_dot(filename) and find_in(filename, 'ENGINE'):
            names_list = filename.split('.') 
            first_name = names_list[0]
            os.system(f'mv {filename} {first_name}.FBK')
            filename = first_name + '.FBK'
            print(filename)

        if find_in(filename, 'MYSHOP'):
            is_layer_file = True
            name_list = re.split('(_\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2})', filename, 1)
            print(name_list)
            name_without_date = name_list[0] + name_list[-1]
            os.system(f'mv {filename} {name_without_date}')
            filename = name_without_date
        print('jhere')
        converted_fdb_file =convert_from_fbk_to_fdb(filename)
        if is_layer_file:
            os.system(f'mv {converted_fdb_file} storage/')
        if not is_layer_file:
        
    
if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
