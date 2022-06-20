import os
import sys

layer_dir = ''

def make_sql():
	path = layer_dir+'/'+'my_sql.sql'
	my_file = open(path, 'w')
	my_file.write(f"""update engine_users eu 
					  set eu.passwd=
					  'pbkdf2_sha256$200$gIdhBJC5WAgz$0q2L7V5WcuodEMI62ULACYVo/rA3JhX6qwsmi0leptk='
					  where eu.sa_uid={layer_uid}""")

	my_file.close()
	return path

def do_job_with_firebird():
	sql = make_sql()
	shutil.copy2(o, ENGINE_STORAGE)
	os.system('docker exec -it firebird isql -q -i firebird/data/my_sql.sql')

def change_password_on_layer():
	if len(sys.argv) > 1:
		layer_uid = sys.argv[1]
		do_job_with_firebird()


